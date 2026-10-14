#!/usr/bin/env python3
"""Build lab.pkt for the CS124 "Packet Trail" Packet Tracer lab.

Packet Tracer files are zlib-compressed XML inside an obfuscation + Twofish/EAX
wrapper (see ptcrypt.js). We start from Cisco's bundled example
"DNS-A-and-AAAA-records.pkt" (it already holds every device model we need:
3x PC-PT, 2x Server-PT, a 2960-24TT and an ISR4331), rewire it into the lab
network, and re-encode it.

    cd tools && npm install
    python3 build_lab.py --base "<PT>/saves/01 Networking/IPv6/DNS-A-and-AAAA-records.pkt"

Writes ../lab.pkt (and ../build/lab.xml for inspection).
"""
import argparse
import copy
import html
import itertools
import pathlib
import random
import subprocess
import uuid
import xml.etree.ElementTree as ET

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
rng = random.Random(124)  # deterministic builds

# ---------------------------------------------------------------- lab design
DOMAIN = "cs124.lab"
CLIENT_GW, SERVER_GW, MASK = "192.168.10.1", "10.124.0.1", "255.255.255.0"
DNS_IP = "10.124.0.10"
R1_CLIENT_MAC = "00C5.1240.BEEF"  # Flag 5 depends on this

FLAGS = {
    1: "CS124{knock_knock_its_the_gateway}",
    2: "CS124{dns_is_the_internets_phonebook}",
    3: "CS124{postcards_travel_on_port_80}",
    4: "CS124{sealed_envelopes_use_port_443}",
    5: "CS124{osi_layer_cake_complete}",
}

DNS_RECORDS = [
    ("library." + DOMAIN, "10.124.0.20"),
    ("www." + DOMAIN, "10.124.0.20"),
    ("vault." + DOMAIN, "10.124.0.30"),
    ("dns." + DOMAIN, DNS_IP),
]

# Switch ports: Fa0/1-10 + Gig0/1 = VLAN 10 (clients); Fa0/11-20 + Gig0/2 = VLAN 20 (servers)
PCS = [  # base device name -> new device
    ("PC0", "STUDENT-PC", "192.168.10.10", "00C5.1240.0010", "FastEthernet0/1", (120, 430)),
    ("PC1", "PC-2", "192.168.10.11", None, "FastEthernet0/2", (230, 470)),
    ("PC2", "PC-3", "192.168.10.12", None, "FastEthernet0/3", (340, 470)),
]
SERVERS = [  # (base, name, ip, mac, switch port, xy, http, https, dns)
    ("DNS Server", "DNS-SERVER", DNS_IP, "00C5.1240.0053", "FastEthernet0/11", (500, 470), False, False, True),
    ("Server", "WEB-SERVER", "10.124.0.20", "00C5.1240.0020", "FastEthernet0/12", (610, 470), True, False, False),
    ("Server", "VAULT", "10.124.0.30", "00C5.1240.0030", "FastEthernet0/13", (720, 470), False, True, False),
    ("Server", "GATE-WEB", "10.124.0.40", "00C5.1240.0040", "FastEthernet0/14", (830, 430), True, False, False),
]
SWITCH_XY, ROUTER_XY = (470, 280), (470, 110)

# ---------------------------------------------------------------- web pages


def ent(s):
    """Write text as HTML numeric entities: renders normally in the PT browser,
    but is unreadable at a glance in the server's HTML editor."""
    return "".join(f"&#{ord(c)};" for c in s)


def page(title, body):
    return (f"<html>\n<head><title>{title}</title></head>\n<body>\n"
            f"<h1>{title}</h1>\n{body.strip()}\n</body>\n</html>")


def flag_box(n):
    return (f"<hr>\n<h2>Flag {n}</h2>\n<p>Copy this exactly into your submission:</p>\n"
            f"<p><font size='+1'><b>{ent(FLAGS[n])}</b></font></p>\n<hr>")


GATE_PAGES = {
    "index.html": page("You found the front door!", f"""
<p>You typed your <b>default gateway</b>'s address into the browser, and something answered.</p>
<p>Your default gateway is <b>R1</b>, the router. It's the door out of your neighborhood
(192.168.10.x). Any time STUDENT-PC wants to talk to a computer that is <i>not</i> in
its own neighborhood, it hands the message to the gateway and lets the router pass it on.</p>
<p><b>Secret:</b> routers don't normally host websites. R1 quietly <b>forwarded</b> your
request to a server hiding behind it (GATE-WEB, 10.124.0.40). This trick is called
<b>port forwarding</b>, and your home Wi-Fi router can do it too.</p>
{flag_box(1)}
<p>Next: go back to your handout and start <b>Flag 2 (DNS)</b>.</p>
"""),
}

WWW_PAGES = {
    "index.html": page("Welcome to the CS124 Library", f"""
<p>You reached this site by its <b>name</b>. But computers don't send data to names.
They send it to <b>IP addresses</b>.</p>
<p>Before your browser could load this page, STUDENT-PC asked the <b>DNS server</b>
({DNS_IP}): <i>"What's the IP address of this name?"</i> DNS answered, and only then
did your browser connect. That answer is exactly what <b>nslookup</b> showed you.</p>
<p>Fun fact: <b>www.{DOMAIN}</b> and <b>library.{DOMAIN}</b> are two names for the
<b>same</b> IP address. Try nslookup on both. One building can have two street names.</p>
{flag_box(2)}
<p>Next: go back to your handout and start <b>Flag 3 (HTTP)</b>.</p>
"""),
    "postcard.html": page("The Postcard (HTTP)", f"""
<p>This page came to you over <b>HTTP</b>, the language browsers and web servers use.
Plain HTTP is like a <b>postcard</b>: anyone who handles it along the way can read it.</p>
<p>Every message also carries a <b>port number</b>. If the IP address is the building,
the port is the apartment number: it says <i>which program</i> on the server should get it.</p>
<h2>Your mission</h2>
<ol>
<li>Switch to <b>Simulation Mode</b> and load this page again
(http://www.{DOMAIN}/postcard.html).</li>
<li>Click the first <b>HTTP</b> packet that leaves STUDENT-PC.</li>
<li>Under <b>Layer 4</b>, find the <b>destination port</b> (written "Dst Port").</li>
<li>Go back to Realtime mode and visit:<br>
<b>http://www.{DOMAIN}/port-NUMBER.html</b><br>
replacing NUMBER with the destination port you found.</li>
</ol>
<p>The right number unlocks Flag 3. A wrong number will tell you what you probably mixed up.</p>
"""),
    "osi.html": page("The Layer Cake (OSI model)", f"""
<p>Every packet is wrapped in layers, like a gift in a box in a shipping box.
Each layer has its own job and its own label.</p>
<table border='1' cellpadding='4'>
<tr><th>Layer</th><th>Name</th><th>Label you'll see</th><th>Job</th></tr>
<tr><td>7</td><td>Application</td><td>HTTP, HTTPS, DNS</td><td>What the apps are saying</td></tr>
<tr><td>4</td><td>Transport</td><td>TCP + port numbers</td><td>Which program on the computer</td></tr>
<tr><td>3</td><td>Network</td><td>IP addresses + TTL</td><td>Which computer, anywhere</td></tr>
<tr><td>2</td><td>Data Link</td><td>MAC addresses</td><td>Which device on this wire, for the next hop</td></tr>
</table>
<h2>Final mission</h2>
<p>In Simulation Mode, load this page again and click the <b>first HTTP packet
while it is still at STUDENT-PC</b>. Write down:</p>
<ul>
<li><b>MAC</b>: last 4 characters of the Layer 2 <b>destination</b> MAC (lowercase)</li>
<li><b>TTL</b>: the Layer 3 TTL number (look in the <b>Outbound PDU Details</b> tab)</li>
<li><b>PORT</b>: the Layer 4 <b>destination</b> port</li>
<li><b>PROTO</b>: the Layer 7 protocol name (lowercase)</li>
</ul>
<p>Then, in Realtime mode, visit:<br>
<b>http://www.{DOMAIN}/osi-MAC-TTL-PORT-PROTO.html</b></p>
<p>Example of the format only: osi-1a2b-64-8080-ftp.html</p>
<p>If you get a "not found" error, check for typos, dashes and lowercase.</p>
"""),
}

VAULT_PAGES = {
    "index.html": page("The Vault (HTTPS)", f"""
<p>Look at the address bar: <b>https://</b>. The "s" means <b>secure</b>. This page came
to you inside a sealed, locked <b>envelope</b> (that's <b>encryption</b>). Routers and
switches can still read the outside of the envelope (where it's from and where it's
going) but not the letter inside.</p>
<p>The vault doesn't answer plain http:// at all. If you tried that first, you saw it fail.</p>
<h2>Your mission</h2>
<ol>
<li>In <b>Simulation Mode</b>, load https://vault.{DOMAIN} again.</li>
<li>Click the first <b>HTTPS</b> packet leaving STUDENT-PC and find its Layer 4
<b>destination port</b>.</li>
<li>In Realtime mode, visit <b>https://vault.{DOMAIN}/port-NUMBER.html</b></li>
</ol>
"""),
}


def port_feedback(n, correct, scheme):
    if n == correct:
        return None
    if n >= 1024:
        why = (f"{n} is the <b>source</b> port, the temporary 'return address' apartment "
               "STUDENT-PC picked for itself. Look for the <b>destination</b> port instead.")
    elif n == 53:
        why = "53 is the <b>DNS</b> port. You clicked the DNS lookup, not the web request."
    elif n == 80:
        why = "80 is the port for plain <b>HTTP</b> (the postcard). This was an <b>HTTPS</b> packet."
    elif n == 443:
        why = "443 is the port for <b>HTTPS</b>. This page asked about a plain <b>HTTP</b> packet."
    else:
        why = "That's not the port this packet used."
    return page("Not quite!", f"<p>{why}</p><p>Go back and look at Layer 4 again.</p>"
                f"<p><a href='{scheme}'>Back to the start</a></p>")


WRONG_PORTS = [53, 80, 443] + list(range(1024, 1031))
for p in WRONG_PORTS:
    if (fb := port_feedback(p, 80, "postcard.html")):
        WWW_PAGES[f"port-{p}.html"] = fb
    if (fb := port_feedback(p, 443, "index.html")):
        VAULT_PAGES[f"port-{p}.html"] = fb

WWW_PAGES["port-80.html"] = page("Port 80: correct!", f"""
<p>Web servers listen for plain HTTP on port <b>80</b>. Your packet was addressed to
10.124.0.20 (the building), <b>port 80</b> (the HTTP apartment).</p>
{flag_box(3)}
<p><b>But there's a second site.</b> The vault, <b>vault.{DOMAIN}</b>, only opens
sealed envelopes. Try <b>http://vault.{DOMAIN}</b> first and watch it fail. Then try
<b>https://vault.{DOMAIN}</b>. Your handout has the details for Flag 4.</p>
""")

VAULT_PAGES["port-443.html"] = page("Port 443: correct!", f"""
<p>HTTPS uses port <b>443</b>. Compare with Flag 3: plain HTTP used port <b>80</b>.</p>
<p>Same idea, different apartment: the port tells the server which program (and which
rules) should handle your message. The 443 program only speaks encrypted.</p>
{flag_box(4)}
<p>Next: your handout's <b>Flag 5 (OSI)</b>. Start at <b>http://www.{DOMAIN}/osi.html</b>.</p>
""")

# Flag 5: the file name IS the answer. Wrong-but-plausible combos get targeted hints.
OSI_ANSWER = ("beef", "128", "80", "http")
OSI_HINTS = {
    "mac": {"0010": "<b>0010</b> is STUDENT-PC's own MAC. That's the <b>source</b>. You want the <b>destination</b>.",
            "0020": "<b>0020</b> is the web server's MAC. But the frame leaving STUDENT-PC isn't addressed to the server. "
                    "The server is in a different neighborhood, so whose MAC goes on the frame? (Hint: the door out.)"},
    "ttl": {"127": "TTL <b>127</b> means you looked at the packet <b>after</b> it passed through R1 "
                   "(each router subtracts 1). Click it while it's still at STUDENT-PC."},
    "port": {p: f"Port <b>{p}</b> is the <b>source</b> port. You want the <b>destination</b> port." for p in
             ["1024", "1025", "1026", "1027", "1028", "1029", "1030"]} | {
             "443": "Port <b>443</b> is HTTPS. This page was loaded over plain HTTP."},
    "proto": {"tcp": "<b>TCP</b> is the Layer 4 protocol. Layer 7 is the application's language.",
              "https": "This page was loaded with plain HTTP, not HTTPS."},
}
for mac, ttl, port, proto in itertools.product(
        ["beef", "0010", "0020"], ["128", "127"], ["80", "443", "1025", "1026", "1027"], ["http", "tcp", "https"]):
    combo = (mac, ttl, port, proto)
    name = f"osi-{mac}-{ttl}-{port}-{proto}.html"
    if combo == OSI_ANSWER:
        WWW_PAGES[name] = page("You read every layer!", f"""
<table border='1' cellpadding='4'>
<tr><th>Layer</th><th>You found</th><th>What it means</th></tr>
<tr><td>2 Data Link</td><td>dest MAC ...{mac.upper()}</td><td>The frame goes to <b>R1</b> (your gateway), not the web server. MAC addresses only get you to the next hop.</td></tr>
<tr><td>3 Network</td><td>TTL {ttl}</td><td>The packet's "hops left" counter. Each router subtracts 1, so lost packets can't loop forever.</td></tr>
<tr><td>4 Transport</td><td>dest port {port}</td><td>Which program on the server gets it: the web server, HTTP.</td></tr>
<tr><td>7 Application</td><td>{proto.upper()}</td><td>The actual request: "please send me osi.html".</td></tr>
</table>
<p>The IP addresses stay the same for the whole trip. The MAC addresses get rewritten at every hop.
That is the key idea behind how the internet works.</p>
{flag_box(5)}
<p>That's the final flag. Congratulations, detective!</p>
""")
        continue
    wrong = [OSI_HINTS[k][v] for k, v, good in zip(("mac", "ttl", "port", "proto"), combo, OSI_ANSWER)
             if v != good]
    WWW_PAGES[name] = page("Close, but not yet", "<p>Some layers are right. These ones aren't:</p>\n<ul>\n"
                           + "\n".join(f"<li>{w}</li>" for w in wrong)
                           + "\n</ul>\n<p><a href='osi.html'>Back to the Layer Cake</a></p>")

PAGES = {"WEB-SERVER": WWW_PAGES, "VAULT": VAULT_PAGES, "GATE-WEB": GATE_PAGES}

WELCOME_NOTE = f"""THE PACKET TRAIL - CS124 Network Detective Lab
Start on STUDENT-PC (bottom left). Click it, then open the Desktop tab.
You never need to change any settings. Just explore, click, and read.
Follow your handout for the 5 flags."""
LEFT_NOTE = "Client neighborhood\n192.168.10.0/24 (VLAN 10)"
RIGHT_NOTE = "Server neighborhood\n10.124.0.0/24 (VLAN 20)"

# ---------------------------------------------------------------- XML helpers


def setx(el, path, value):
    node = el.find(path)
    if node is None:
        raise KeyError(path)
    node.text = value


def eui64_ll(mac):
    b = bytes.fromhex(mac.replace(".", ""))
    b = bytes([b[0] ^ 2]) + b[1:3] + b"\xff\xfe" + b[3:]
    groups = [f"{(b[i] << 8) | b[i + 1]:X}" for i in range(0, 8, 2)]
    return "FE80::" + ":".join(groups)


def set_mac(port, mac):
    setx(port, "MACADDRESS", mac)
    setx(port, "BIA", mac)
    for tag in ("IPV6_LINK_LOCAL", "IPV6_DEFAULT_LINK_LOCAL"):
        if port.find(tag) is not None and port.findtext(tag):
            setx(port, tag, eui64_ll(mac))


def rand_mac():
    return "00E0.%02X%02X.%02X%02X" % tuple(rng.randrange(256) for _ in range(4))


def clear_ipv6(port):
    ips = port.find("IPV6_ADDRESSES")
    if ips is not None:
        for c in list(ips):
            ips.remove(c)
    for tag in ("IPV6_PORT_GATEWAY", "IPV6_PORT_DNS"):
        if port.find(tag) is not None:
            port.find(tag).text = None


def host_port(dev):
    return next(dev.find("ENGINE/MODULE").iter("PORT"))


def set_host_ip(dev, ip, gw, dns):
    e = dev.find("ENGINE")
    p = host_port(dev)
    setx(p, "IP", ip)
    setx(p, "SUBNET", MASK)
    setx(p, "PORT_GATEWAY", gw)
    setx(p, "PORT_DNS", dns)
    setx(p, "PORT_DHCP_ENABLE", "false")
    setx(p, "IPV6_PORT_DHCP_ENABLED", "false")
    setx(p, "IPV6_ADDRESS_AUTOCONFIG", "false")
    clear_ipv6(p)
    setx(e, "GATEWAY", gw)
    setx(e, "DNS_CLIENT/SERVER_IP", dns)
    if e.find("DNS_CLIENT/SERVER_IPV6") is not None:
        e.find("DNS_CLIENT/SERVER_IPV6").text = None
    if e.find("GATEWAYV6") is not None:
        e.find("GATEWAYV6").text = None


def rename(dev, name, phys_nodes):
    setx(dev, "ENGINE/NAME", name)
    if dev.find("ENGINE/SYS_NAME") is not None:
        dev.find("ENGINE/SYS_NAME").text = name
    own = dev.findtext("WORKSPACE/PHYSICAL").split(",")[-1]
    phys_nodes[own][0].find("NAME").text = name


def place(dev, xy):
    setx(dev, "WORKSPACE/LOGICAL/X", str(xy[0]))
    setx(dev, "WORKSPACE/LOGICAL/Y", str(xy[1]))


def set_config(dev, lines):
    rc = dev.find("ENGINE/RUNNINGCONFIG")
    for c in list(rc):
        rc.remove(c)
    for line in lines:
        ET.SubElement(rc, "LINE").text = line


def http_dir(dev):
    for f in dev.find("ENGINE/FILE_MANAGER").iter("FILE"):
        if f.get("class") == "CFileSystem" and f.findtext("NAME") == "http:":
            return f
    raise KeyError("http: filesystem")


def set_http_files(dev, pages):
    d = http_dir(dev)
    files = d.find("FILES")
    for c in list(files):
        files.remove(c)
    for i, (name, text) in enumerate(sorted(pages.items()), start=1):
        f = ET.SubElement(files, "FILE", {"class": "CFile"})
        ET.SubElement(f, "FILE_NUMBER").text = str(i)
        ET.SubElement(f, "NAME").text = name
        ET.SubElement(f, "DATE_TIME").text = "0"
        ET.SubElement(f, "PERMISSION").text = "6"
        content = ET.SubElement(f, "FILE_CONTENT", {"class": "CHttpPage"})
        ET.SubElement(content, "TEXT").text = text
    setx(d, "FILE_COUNTER", str(len(pages)))


def set_services(dev, http, https, dns):
    e = dev.find("ENGINE")
    setx(e, "HTTP_SERVER/ENABLED", "1" if http else "0")
    setx(e, "HTTPS_SERVER/HTTPSENABLED", "1" if https else "0")
    setx(e, "DNS_SERVER/ENABLED", "1" if dns else "0")
    db = e.find("DNS_SERVER/NAMESERVER-DATABASE")
    for c in list(db):
        db.remove(c)
    if dns:
        for name, ip in DNS_RECORDS:
            rr = ET.SubElement(db, "RESOURCE-RECORD")
            ET.SubElement(rr, "TYPE").text = "A-REC"
            ET.SubElement(rr, "NAME").text = name
            ET.SubElement(rr, "TTL").text = "86400"
            ET.SubElement(rr, "IPADDRESS").text = ip
    # Everything else off, so the Services tab only shows what matters.
    for path in ("FTP_SERVER/ENABLED", "SYSLOG_SERVER/ENABLED", "NTP_SERVER/ENABLED",
                 "TFTP_SERVER/ENABLED", "EMAIL_SERVER/SMTP_ENABLED", "EMAIL_SERVER/POP3_ENABLED",
                 "ACS_SERVER/ENABLED", "IOX_SEVICE/HTTPSENABLED"):
        if e.find(path) is not None:
            setx(e, path, "0")
    for en in e.iterfind("DHCP_SERVERS/ASSOCIATED_PORTS/ASSOCIATED_PORT/DHCP_SERVER/ENABLED"):
        en.text = "0"


# ---------------------------------------------------------------- build


def run_codec(mode, src, dst):
    subprocess.run(["node", str(HERE / "ptcrypt.js"), mode, str(src), str(dst)], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="path to DNS-A-and-AAAA-records.pkt from the PT install")
    ap.add_argument("--out", default=str(ROOT / "lab.pkt"))
    args = ap.parse_args()

    build = ROOT / "build"
    build.mkdir(exist_ok=True)
    run_codec("d", args.base, build / "base.xml")
    tree = ET.parse(build / "base.xml")
    root = tree.getroot()
    net = root.find("NETWORK")
    devices_el, links_el = net.find("DEVICES"), net.find("LINKS")
    devs = {d.findtext("ENGINE/NAME"): d for d in devices_el}

    # uuid -> (physical NODE, parent CHILDREN element)
    phys_nodes = {}
    for parent in root.find("PHYSICALWORKSPACE").iter("CHILDREN"):
        for node in parent.findall("NODE"):
            phys_nodes[node.findtext("UUID_STR")] = (node, parent)

    def clone(base_name):
        src = devs[base_name]
        dev = copy.deepcopy(src)
        old_uuid = src.findtext("WORKSPACE/PHYSICAL").split(",")[-1]
        new_uuid = "{%s}" % uuid.UUID(int=rng.getrandbits(128), version=4)
        node, parent = phys_nodes[old_uuid]
        new_node = copy.deepcopy(node)
        new_node.find("UUID_STR").text = new_uuid
        parent.append(new_node)
        phys_nodes[new_uuid] = (new_node, parent)
        setx(dev, "WORKSPACE/PHYSICAL", dev.findtext("WORKSPACE/PHYSICAL").replace(old_uuid, new_uuid))
        setx(dev, "ENGINE/SAVE_REF_ID", "save-ref-id:%d" % rng.getrandbits(63))
        setx(dev, "ENGINE/SERIALNUMBER", "PTT%08X" % rng.getrandbits(32))
        setx(dev, "WORKSPACE/LOGICAL/MEM_ADDR", str(rng.getrandbits(40)))
        setx(dev, "WORKSPACE/LOGICAL/DEV_ADDR", str(rng.getrandbits(40)))
        duid = dev.find("ENGINE/DHCPV6_MAIN/PARTIAL_DUID")
        if duid is not None:
            duid.text = "-".join("%02X" % rng.randrange(256) for _ in range(4)) + "-"
        for p in dev.find("ENGINE/MODULE").iter("PORT"):
            set_mac(p, rand_mac())
        devices_el.append(dev)
        return dev

    final = {}  # new name -> (device element, switch port, own port name)

    for base, name, ip, mac, swport, xy in PCS:
        dev = devs[base]
        rename(dev, name, phys_nodes)
        set_host_ip(dev, ip, CLIENT_GW, DNS_IP)
        if mac:
            set_mac(host_port(dev), mac)
        place(dev, xy)
        final[name] = (dev, swport, "FastEthernet0")

    used_base_server = False
    for base, name, ip, mac, swport, xy, http, https, dns in SERVERS:
        if base == "Server" and used_base_server:
            dev = clone("Server")
        else:
            dev = devs[base]
            used_base_server |= base == "Server"
        rename(dev, name, phys_nodes)
        set_host_ip(dev, ip, SERVER_GW, DNS_IP)
        set_mac(host_port(dev), mac)
        set_services(dev, http, https, dns)
        set_http_files(dev, PAGES.get(name, {}))
        place(dev, xy)
        final[name] = (dev, swport, "FastEthernet0")

    # ---- switch
    sw = devs["Switch0"]
    rename(sw, "SW1", phys_nodes)
    place(sw, SWITCH_XY)
    cfg = ["!", "version 15.0", "no service timestamps log datetime msec",
           "no service timestamps debug datetime msec", "no service password-encryption", "!",
           "hostname SW1", "!", "spanning-tree mode pvst", "spanning-tree extend system-id", "!"]
    for i in range(1, 25):
        cfg.append(f"interface FastEthernet0/{i}")
        if i <= 20:
            vlan = 10 if i <= 10 else 20
            cfg += [f" switchport access vlan {vlan}", " switchport mode access", " spanning-tree portfast"]
        cfg.append("!")
    for i, vlan in ((1, 10), (2, 20)):
        cfg += [f"interface GigabitEthernet0/{i}", f" switchport access vlan {vlan}",
                " switchport mode access", " spanning-tree portfast", "!"]
    cfg += ["interface Vlan1", " no ip address", " shutdown", "!",
            "line con 0", "!", "line vty 0 4", " login", "line vty 5 15", " login", "!", "end"]
    set_config(sw, cfg)
    vlans = sw.find("ENGINE/VLANS")
    for v in list(vlans):
        if v.get("number") in ("10", "20"):
            vlans.remove(v)
    vlans.insert(1, ET.Element("VLAN", {"name": "CLIENTS", "number": "10", "rspan": "0"}))
    vlans.insert(2, ET.Element("VLAN", {"name": "SERVERS", "number": "20", "rspan": "0"}))

    # ---- router
    r1 = devs["Router0"]
    rename(r1, "R1", phys_nodes)
    place(r1, ROUTER_XY)
    rports = list(r1.find("ENGINE/MODULE").iter("PORT"))  # G0/0/0, G0/0/1, G0/0/2
    for p, ip in ((rports[0], CLIENT_GW), (rports[1], SERVER_GW)):
        setx(p, "IP", ip)
        setx(p, "SUBNET", MASK)
        setx(p, "POWER", "true")
        clear_ipv6(p)
    set_mac(rports[0], R1_CLIENT_MAC)
    set_mac(rports[1], "00C5.1240.0001")
    setx(rports[2], "IP", "")
    clear_ipv6(rports[2])
    set_config(r1, [
        "!", "version 15.4", "no service timestamps log datetime msec",
        "no service timestamps debug datetime msec", "no service password-encryption", "!",
        "hostname R1", "!", "ip cef", "no ipv6 cef", "!", "no ip domain-lookup", "!",
        "spanning-tree mode pvst", "!",
        "interface GigabitEthernet0/0/0", " description Client neighborhood (VLAN 10)",
        f" ip address {CLIENT_GW} {MASK}", " ip nat outside", " duplex auto", " speed auto", "!",
        "interface GigabitEthernet0/0/1", " description Server neighborhood (VLAN 20)",
        f" ip address {SERVER_GW} {MASK}", " ip nat inside", " duplex auto", " speed auto", "!",
        "interface GigabitEthernet0/0/2", " no ip address", " duplex auto", " speed auto", " shutdown", "!",
        "interface Vlan1", " no ip address", " shutdown", "!",
        # Flag 1: http://<gateway> is forwarded to GATE-WEB
        f"ip nat inside source static tcp 10.124.0.40 80 {CLIENT_GW} 80 ",
        "ip classless", "!", "ip flow-export version 9", "!",
        "line con 0", "!", "line aux 0", "!", "line vty 0 4", " login", "!", "end"])

    # ---- links
    template = copy.deepcopy(links_el[0])
    for l in list(links_el):
        links_el.remove(l)

    def link(a_dev, a_port, b_dev, b_port):
        l = copy.deepcopy(template)
        c = l.find("CABLE")
        setx(c, "FROM", a_dev.findtext("ENGINE/SAVE_REF_ID"))
        setx(c, "TO", b_dev.findtext("ENGINE/SAVE_REF_ID"))
        ports = c.findall("PORT")
        ports[0].text, ports[1].text = a_port, b_port
        setx(c, "FROM_DEVICE_MEM_ADDR", a_dev.findtext("WORKSPACE/LOGICAL/DEV_ADDR"))
        setx(c, "TO_DEVICE_MEM_ADDR", b_dev.findtext("WORKSPACE/LOGICAL/DEV_ADDR"))
        setx(c, "FROM_PORT_MEM_ADDR", str(rng.getrandbits(40)))
        setx(c, "TO_PORT_MEM_ADDR", str(rng.getrandbits(40)))
        links_el.append(l)

    for name, (dev, swport, own) in final.items():
        link(dev, own, sw, swport)
    link(r1, "GigabitEthernet0/0/0", sw, "GigabitEthernet0/1")
    link(r1, "GigabitEthernet0/0/1", sw, "GigabitEthernet0/2")

    # ---- workspace notes
    notes = root.find("PHYSICALWORKSPACE/NOTES")
    if notes is None:
        notes = ET.SubElement(root.find("PHYSICALWORKSPACE"), "NOTES")
    for n in list(notes):
        notes.remove(n)
    for (x, y), text in (((40, -20), WELCOME_NOTE), ((90, 540), LEFT_NOTE), ((560, 540), RIGHT_NOTE)):
        n = ET.SubElement(notes, "NOTE")
        ET.SubElement(n, "X").text = str(x)
        ET.SubElement(n, "Y").text = str(y)
        ET.SubElement(n, "Z").text = "40001"
        ET.SubElement(n, "TEXT", {"translate": "true"}).text = text
        ET.SubElement(n, "NOTECLUSTERID").text = "1-1"

    # ---- simulation filters: only what the lab needs
    show = {"HTTP", "HTTPS", "DNS", "ARP", "ICMP"}
    filt = root.find("FILTERS")
    for k in filt.attrib:
        filt.set(k, "yes" if k in show else "no")

    # ---- options: students explore, they don't configure routers/switches
    opts = root.find("OPTIONS")
    setx(opts, "HIDECLIOFROUTERANDSWITCH", "true")

    net.find("DESCRIPTION").text = WELCOME_NOTE

    ET.indent(tree, space=" ")
    tree.write(build / "lab.xml", encoding="utf-8", xml_declaration=False)
    run_codec("e", build / "lab.xml", args.out)
    run_codec("d", args.out, build / "roundtrip.xml")
    assert (build / "roundtrip.xml").read_bytes() == (build / "lab.xml").read_bytes(), "round-trip mismatch"
    print(f"wrote {args.out}  ({len(final) + 2} devices, {len(links_el)} links, "
          f"{sum(len(p) for p in PAGES.values())} web pages)")


if __name__ == "__main__":
    main()

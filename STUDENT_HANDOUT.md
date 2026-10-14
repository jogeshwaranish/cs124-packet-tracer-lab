# The Packet Trail: a Packet Tracer flag hunt

**CS124 Honors · about 1.5–2 hours · no networking experience needed**

You've just joined the **CS124 Network Detective Agency**. Your job: figure out exactly what happens between typing a web address and seeing the page. The network is already built and working. You won't configure anything. You'll **explore, click, and read**.

There are **5 flags**. A flag looks like `CS124{some_words_here}`. Copy each one exactly (copy-paste is best) and submit it at: **[instructor: submission link]**.

---

## Before you start (do this at home)

1. **Make a free Cisco Networking Academy account** at https://www.netacad.com. Packet Tracer asks you to log in with it.
2. **Install Cisco Packet Tracer** (version 8.2 or newer) from the "Download Packet Tracer" page on netacad.com. It's available for Windows, macOS, and Ubuntu Linux.
3. **Watch a short intro video on IP addresses.** NetworkChuck's IP address video is a good one: **[instructor: video link]**.
4. **Skim the glossary** at the bottom of this page. You don't need to memorize it.
5. Download **`lab.pkt`** and open it (File → Open).

### How to get around Packet Tracer

- **Click a device** to open its window. The **Desktop** tab has apps (Command Prompt, Web Browser). The **Config** tab shows settings. On servers, the **Services** tab shows what the server offers.
- Bottom-right corner: **Realtime** vs. **Simulation** mode. Realtime is normal speed. Simulation pauses the network so you can watch each packet. You'll use it in Flags 3–5.
- **You always work from `STUDENT-PC`** (bottom left).

> **Copy-paste tip:** in Packet Tracer's Command Prompt, type commands exactly as shown, then press Enter.
> **"Request timed out" on the first try?** Totally normal. The network is still learning who's who. Just try again.

---

## Flag 1: "Who am I?"

*Learn: IP address, subnet mask, MAC address, default gateway, router.*

1. Click **STUDENT-PC** → **Desktop** → **Command Prompt**.
2. Run:
   ```
   ipconfig /all
   ```
3. Write these down (you'll need them later):

   | What | Your value |
   |---|---|
   | IPv4 Address | |
   | Subnet Mask | |
   | Default Gateway | |
   | Physical Address (that's your MAC address) | |

4. Your **default gateway** is the router, the "door" out of your neighborhood. Check that it's there:
   ```
   ping <your default gateway>
   ```
5. Now close the Command Prompt, open **Web Browser** (also on the Desktop tab), type `http://<your default gateway>` into the URL bar, and press **Go**.

🚩 The flag is on that page. The page also explains a surprise about how it got there.

**Think about it:** Click **PC-2** and look at its IP and gateway (Config tab or `ipconfig` on PC-2). What's the same as yours, and what's different?

---

## Flag 2: DNS, the internet's phonebook

*Learn: hostnames, DNS, what happens when you type a URL.*

Our club library lives at **`library.cs124.lab`**. But computers only send data to **IP addresses**, so who turns that name into a number?

1. On STUDENT-PC → **Command Prompt**:
   ```
   nslookup library.cs124.lab
   ```
   - The `Server:` line is the DNS server that answered.
   - The `Address:` line under `Name:` is the library's IP address. Write it down.
2. Open the **Web Browser** and go to `http://library.cs124.lab`.

🚩 The flag is on the page.

**Think about it:**
- Run `nslookup www.cs124.lab`. What do you notice?
- Run `tracert library.cs124.lab`. Each numbered line is one "hop", a device that passed your packet along. Which hop is your default gateway?
- Click the **DNS-SERVER** → **Services** → **DNS** to see its whole phonebook.

---

## Flag 3: HTTP and port 80

*Learn: HTTP, ports, Simulation Mode, Layer 4.*

1. In the Web Browser, visit `http://www.cs124.lab/postcard.html` and read the page.
2. Now watch that same visit in slow motion:
   1. Click **Simulation** (bottom-right corner, or press Shift+S). An **Event List** panel appears.
   2. The filters are already set to show just the interesting packets (DNS, HTTP, HTTPS, ARP, ICMP). If you don't see packets later, click **Edit Filters** and make sure **HTTP** and **HTTPS** are ticked.
   3. Back in STUDENT-PC's Web Browser, click **Go** again on the same URL.
   4. Press **Play** (▶) in the Simulation panel, or press **Capture/Forward** repeatedly. Watch the little envelopes move across the network.
   5. In the Event List, find the first row with Type **HTTP** where "At Device" is **STUDENT-PC**. Click the colored square in its **Info** column.
   6. In the window that opens, stay on the **OSI Model** tab. Look at **Layer 4**. Find **Dst Port** (the destination port).
3. Switch back to **Realtime**. In the browser, visit:
   ```
   http://www.cs124.lab/port-<the destination port>.html
   ```

🚩 The right port unlocks Flag 3. A wrong port gives you a hint about what you mixed up. The flag page also points you to a second site.

---

## Flag 4: HTTPS and port 443

*Learn: HTTPS, encryption, why the port changes.*

1. In the browser, try `http://vault.cs124.lab`. It should fail. That's on purpose.
2. Now try `https://vault.cs124.lab` (note the **s**). Read the page.
3. Repeat the Simulation Mode steps from Flag 3, but this time for `https://vault.cs124.lab`, and click the first **HTTPS** packet at STUDENT-PC. Find its **Layer 4 destination port**.
4. Back in Realtime, visit:
   ```
   https://vault.cs124.lab/port-<the destination port>.html
   ```

🚩 The flag is on that HTTPS page.

**Think about it:** Same kind of request, different port. Compare with Flag 3. Why would a server use two different ports?

---

## Flag 5: The OSI model (final flag)

*Learn: the layers of a packet: Layer 2 (MAC), Layer 3 (IP, TTL), Layer 4 (ports), Layer 7 (application).*

1. In Realtime, visit `http://www.cs124.lab/osi.html` and read the table.
2. Switch to **Simulation**, click **Go** on that same page again, and press Play.
3. Click the **first HTTP packet while it is still at STUDENT-PC**. Fill in:

   | Layer | Where to look | Value |
   |---|---|---|
   | 2: Data Link | OSI Model tab → Layer 2 → **Dest. MAC**: last 4 characters, lowercase | |
   | 3: Network | **Outbound PDU Details** tab → IP section → **TTL** | |
   | 4: Transport | OSI Model tab → Layer 4 → **Dst Port** | |
   | 7: Application | OSI Model tab → Layer 7: the protocol name, lowercase | |

4. Back in Realtime, visit:
   ```
   http://www.cs124.lab/osi-MAC-TTL-PORT-PROTO.html
   ```
   (Use your four values. Example format only: `osi-1a2b-64-8080-ftp.html`.)

🚩 Correct values reveal the final flag. Close-but-wrong values give you a hint about which layer to recheck.

**Big puzzle:** The Layer 2 destination MAC is **not** the web server's MAC. Whose is it? Check by clicking devices and comparing MAC addresses. Why does that make sense?

---

## Glossary

| Term | Plain-English meaning |
|---|---|
| **Network** | Computers connected so they can send each other data. |
| **Packet** | One small chunk of data traveling across a network, with addressing info wrapped around it. |
| **IP address** | A computer's address on a network, like `192.168.10.10`. Used to reach any computer, near or far. |
| **Subnet mask** | Says which part of an IP address is the "neighborhood". With `255.255.255.0`, everyone whose address starts with the same first three numbers is a neighbor. |
| **MAC address** | A hardware ID burned into a network card, like `00C5.1240.0010`. Used only to reach the next device on the same wire. |
| **Switch** | Connects devices in the same neighborhood and delivers frames using MAC addresses. |
| **Router** | Connects different neighborhoods (networks) and forwards packets using IP addresses. |
| **Default gateway** | The router your computer sends things to when the destination is outside its own neighborhood. |
| **DNS** | Domain Name System: the phonebook that turns names (`library.cs124.lab`) into IP addresses. |
| **Hostname** | A human-friendly name for a computer, like `www.cs124.lab`. |
| **HTTP** | HyperText Transfer Protocol: the language browsers and web servers use. Not encrypted. |
| **HTTPS** | HTTP inside an encrypted, sealed connection. |
| **Encryption** | Scrambling data so only the intended receiver can read it. |
| **Port** | A number that says which program on a computer should get a message. Web servers listen on port 80 (HTTP) and 443 (HTTPS). |
| **Source / destination** | Where a packet came from / where it's going. |
| **TCP** | A Layer 4 protocol that makes sure data arrives complete and in order. Carries the port numbers. |
| **TTL** | Time To Live: a counter in every IP packet. Each router subtracts 1; at 0 the packet is thrown away, so lost packets can't loop forever. |
| **OSI model** | A 7-layer way of describing how network communication is organized. Today we used layers 2, 3, 4, and 7. |
| **Port forwarding** | A router rule that sends traffic arriving at the router's own address to a different computer behind it. |
| **ping** | Sends a tiny "are you there?" message and waits for a reply. |
| **ipconfig** | Shows your computer's network settings. Add `/all` for more detail. |
| **nslookup** | Asks a DNS server to look up a name. |
| **tracert** | Lists every hop (router) between you and a destination. |
| **Simulation Mode** | Packet Tracer's slow-motion mode for watching and inspecting packets one step at a time. |

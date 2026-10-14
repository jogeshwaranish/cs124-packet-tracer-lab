# The Packet Trail: a Packet Tracer flag hunt

**CS124 Honors MP · about 1.5–2 hours · no networking experience needed**

## Introduction

Every time you type a web address and press Enter, your computer kicks off a long chain of events. In a few milliseconds it:

- looks up where the website actually lives,
- picks the right "door" on that server to knock on,
- wraps your request in layer after layer of addressing, and
- hands it to a series of devices that pass it along until it arrives.

Then the server does the whole thing in reverse to send the page back. You never see any of it.

In this MP you will see all of it. You've just joined the **CS124 Network Detective Agency**. Your case file is a small campus network built in **Cisco Packet Tracer**, a free network simulator used to teach networking. The network has three PCs, a switch, a router, a DNS server, and three web servers. It's already built and working. You won't configure anything. Your job is to **explore, click, inspect, and read**.

Hidden in the network are **5 flags**. A flag looks like `CS124{some_words_here}`. Each flag is locked behind one idea, and each flag page gives you the lead for the next one, so do them in order. You'll unlock each one by running a real command or by catching a real packet in slow motion and reading what's inside.

You're welcome to use Google, classmates, or an LLM to explain a concept you're stuck on. But the answers come from *your* network. An LLM can tell you what a default gateway is, but it can't tell you what's inside the packet on your screen.

## Learning goals

By the end of this MP you should be able to:

1. **Find your way around a network simulator.** Open devices, use their command prompt and web browser, and switch between Realtime and Simulation mode.
2. **Read a computer's network identity.** Explain what an IP address, subnet mask, MAC address, and default gateway are, and why a computer needs each one.
3. **Explain what happens when you open a website.** Name each step in order: DNS lookup, finding the gateway, opening a connection, the HTTP request, and the response coming back.
4. **Tell HTTP and HTTPS apart.** Say what each protocol does, why HTTPS exists, and which port each one uses.
5. **Use the OSI model as a map of a real packet.** Point to where the MAC address, IP address, TTL, port, and application protocol live inside one packet.

## Prerequisites

- **No networking background needed.** If you can install an app and follow steps, you're set.
- **Watch** NetworkChuck's video on IP addresses: **[instructor: video link]**. It takes about 10 minutes and makes Flag 1 click.
- **Skim** the [glossary](#glossary) at the bottom. You don't need to memorize it. Just recognize the words when you see them.
- **Install Packet Tracer before the lab** (below). The download needs an account, so don't leave it to the last minute.
- **Curiosity.** Click on things. Open every tab. If you break something, just reopen `lab.pkt`.

## Setup

Packet Tracer is free, but Cisco requires a free **Cisco Networking Academy (NetAcad)** account to download it and to log in the first time you run it.

### Step 1: Make a NetAcad account

1. Go to <https://www.netacad.com> and sign up. A personal or school email both work.
2. Find the **Download Packet Tracer** page. Search "Packet Tracer" on the site, or look under Resources. If you only see a course page, enroll in the free self-paced **Getting Started with Cisco Packet Tracer** course. The download links are in its resources.
3. Download **version 8.2 or newer** for your operating system.

### Step 2: Install

<details open><summary><b>Windows</b></summary>

1. Download the **64-bit Windows** installer (`.exe`).
2. Run it, accept the license, and keep the default options.
3. Launch **Cisco Packet Tracer** from the Start menu and log in with your NetAcad account.

</details>

<details><summary><b>macOS</b></summary>

1. Download the **macOS** installer (`.dmg`).
2. Open it and run the installer inside.
3. If macOS says the app "can't be opened," go to **System Settings → Privacy & Security**, scroll down, and click **Open Anyway**.
4. Launch Packet Tracer from Applications and log in with your NetAcad account.

</details>

<details><summary><b>Linux</b></summary>

Cisco officially supports **Ubuntu** (and other Debian-based distros).

1. Download the **Ubuntu** installer (`.deb`).
2. In a terminal, in the folder you downloaded it to, run:
   ```bash
   sudo apt install ./CiscoPacketTracer_*.deb
   ```
   Using `apt install ./file.deb` instead of `dpkg -i` installs any missing dependencies for you.
3. Launch it from your app menu, or run `packettracer` in a terminal, and log in.
4. On Fedora, Arch, or anything else? There's no official package. The easiest route is usually an Ubuntu VM. Ask on the course forum if you get stuck.

</details>

### Step 3: Open the lab

1. Download **`lab.pkt`**: **[instructor: download link]**.
2. In Packet Tracer, choose **File → Open** and pick `lab.pkt`.
3. You should see the campus network. If Packet Tracer says the file is from a newer version, update Packet Tracer.
4. Wait about 10 seconds for all the link lights to turn green. Or click **Fast Forward Time** at the bottom of the window.

### Packet Tracer in 60 seconds

| You want to... | Do this |
|---|---|
| Use a computer | Click it → **Desktop** tab → **Command Prompt** or **Web Browser** |
| See a device's settings | Click it → **Config** tab |
| See what a server offers | Click it → **Services** tab |
| Watch packets move one step at a time | Bottom-right corner: switch **Realtime** to **Simulation** (or press Shift+S) |
| Look inside a packet | In Simulation mode, click the colored square in a row's **Info** column → **OSI Model** and **Outbound PDU Details** tabs |
| Start over | Reopen `lab.pkt` |

**You always work from `STUDENT-PC`** (bottom left).

> **"Request timed out" on the first try?** That's normal. The network is still learning who's who. Try again.

## The big picture (read this first)

You don't need to understand all of this yet. Each flag zooms in on one piece.

**Addresses.** Every computer on a network has an **IP address**, which works like a street address. It also has a **MAC address**, which works like the name on a specific mailbox. IP addresses get your data to the right *building* anywhere in the world. MAC addresses only get it to the next mailbox on your own street.

**Neighborhoods and the gateway.** Computers on the same network can talk directly. To reach anything outside, a computer hands its data to a **router**, called its **default gateway**. The router is the door out of the neighborhood.

**Names.** People type names like `library.cs124.lab`, but computers can only send to IP addresses. A **DNS server** works like a phonebook: you ask it for a name, and it gives back a number.

**Ports.** One server can run several programs at once, such as a website, a phonebook, and a secure vault. A **port** number says *which program* a message is for, the way an apartment number picks out one door in a building. Web traffic uses well-known ports, and you'll find out which ones in Flags 3 and 4.

**HTTP vs HTTPS.** **HTTP** is how browsers ask for web pages. It's like sending a **postcard**: anyone who handles it along the way can read it. **HTTPS** is HTTP sealed in an encrypted **envelope**. Everyone handling it can still see where it's going, but only the receiver can open it.

**Layers.** A packet is like a set of nested envelopes. The **OSI model** names the layers:

| Layer | Name | Its job | Example in this lab |
|---|---|---|---|
| 7 | Application | The actual conversation | "Please send me `osi.html`" |
| 6 | Presentation | Formatting and encryption | The HTTPS seal |
| 5 | Session | Keeping a conversation going | (Packet Tracer folds this into 4 and 7) |
| 4 | Transport | Which program, and reliable delivery | Port numbers |
| 3 | Network | Getting across networks | IP addresses, TTL |
| 2 | Data Link | Getting to the next device | MAC addresses |
| 1 | Physical | Bits on a wire | The cables you see on screen |

When your PC sends something, each layer wraps it in its own header on the way down (**encapsulation**). The receiver unwraps them on the way up. In Flag 5 you'll open one real packet and read four of those layers yourself.

---

## Flag 1: "Who am I?"

*Learn: IP address, subnet mask, MAC address, default gateway, router.*

1. Click **STUDENT-PC** → **Desktop** → **Command Prompt**.
2. Run:
   ```
   ipconfig /all
   ```
3. Write these down. You'll need them later.

   | What | Your value |
   |---|---|
   | IPv4 Address | |
   | Subnet Mask | |
   | Default Gateway | |
   | Physical Address (that's your MAC address) | |
   | DNS Servers | |

4. Your **default gateway** is the router, the door out of your neighborhood. Check that it's there:
   ```
   ping <your default gateway>
   ```
5. Close the Command Prompt and open **Web Browser** (also on the Desktop tab). Type `http://<your default gateway>` into the URL bar and press **Go**.

🚩 The flag is on that page. The page also explains a surprise about how it got there.

**Think about it:** Click **PC-2** and look at its IP address and gateway (Config tab, or `ipconfig` on PC-2). What's the same as yours, and what's different? Why?

---

## Flag 2: The internet's phonebook

*Learn: hostnames, DNS, what happens when you type a URL.*

The club library lives at **`library.cs124.lab`**. But computers only send data to **IP addresses**, so who turns that name into a number?

1. On STUDENT-PC → **Command Prompt**:
   ```
   nslookup library.cs124.lab
   ```
   - The `Server:` line is the DNS server that answered. Does it match the DNS server from your Flag 1 table?
   - The `Address:` line under `Name:` is the library's IP address. Write it down.
2. Open the **Web Browser** and go to `http://library.cs124.lab`.

🚩 The flag is on the page.

**Think about it:**
- Run `nslookup www.cs124.lab`. What do you notice?
- Run `tracert library.cs124.lab`. Each numbered line is one **hop**, a device that passed your packet along. Which hop is your default gateway?

---

## Flag 3: The postcard

*Learn: HTTP, ports, Simulation mode, Layers 2 and 4.*

1. The Flag 2 page left you a lead: the address of a postcard. Visit it in the Web Browser and read the page.
2. Now watch that same visit in slow motion:
   1. Click **Simulation** (bottom-right corner, or press Shift+S). An **Event List** panel appears.
   2. The filters are already set to show just the interesting packets (DNS, HTTP, HTTPS, ARP, ICMP). If you don't see packets later, click **Edit Filters** and make sure **HTTP** and **HTTPS** are ticked.
   3. Back in STUDENT-PC's Web Browser, click **Go** again on the same URL.
   4. Press **Play** (▶) in the Simulation panel, or press **Capture/Forward** repeatedly. Watch the little envelopes move across the network.
   5. Follow your request all the way to the server. In the Event List, find the first row with Type **HTTP** where "At Device" is **WEB-SERVER**. Click the colored square in its **Info** column.
   6. In the window that opens, stay on the **OSI Model** tab and write down two values:
      - **PORT:** Layer 4 → **Dst Port** (the destination port)
      - **MAC:** Layer 2 → **Src. MAC** (the source MAC address): last 4 characters, lowercase
3. Switch back to **Realtime**. In the browser, visit:
   ```
   http://www.cs124.lab/port-PORT-MAC.html
   ```
   This example only shows the format: `port-8080-a1b2.html`.

🚩 The right pair unlocks Flag 3. A wrong pair tells you which value to recheck. The flag page also gives you your next lead.

**Think about it:**
- Before HTTP showed up in the Event List, what other protocol did you see, and why did it have to come first?
- STUDENT-PC sent this request, so why isn't STUDENT-PC's MAC the source MAC when it arrives at WEB-SERVER? Whose MAC is it?

---

## Flag 4: The sealed envelope

*Learn: HTTPS, encryption, why the port changes, TTL.*

The Flag 3 page told you about a second site: the vault.

1. In the browser, try the vault's address with `http://`. It should fail. That's on purpose.
2. Now try it with `https://` (note the **s**). Read the page.
3. Repeat the Simulation mode steps from Flag 3, but this time for the `https://` address. Follow the request all the way to the vault: click the first **HTTPS** event where "At Device" is **VAULT**, and write down two values:
   - **PORT:** OSI Model tab → Layer 4 → **Dst Port**
   - **TTL:** **Inbound PDU Details** tab → IP section → **TTL**
4. Back in Realtime, visit:
   ```
   https://<the vault's name>/port-PORT-TTL.html
   ```
   This example only shows the format: `port-8080-64.html`.

🚩 The flag is on that HTTPS page, along with your final lead.

**Think about it:**
- It's the same kind of request, but to a different port. Compare it with Flag 3. Why would a server use two different ports? Why did the `http://` address fail?
- Every IP packet starts with a TTL. Why is the number you found what it is?

---

## Flag 5: The layer cake (final flag)

*Learn: the layers of a packet: Layer 2 (MAC), Layer 3 (IP, TTL), Layer 4 (ports), Layer 7 (application).*

1. In Realtime, visit the page the Flag 4 page sent you to, and read the table.
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
   Use your four values. This example only shows the format: `osi-1a2b-64-8080-ftp.html`.

🚩 Correct values reveal the final flag. Close-but-wrong values tell you which layer to recheck.

**Big puzzle:** The Layer 2 destination MAC is **not** the web server's MAC. Whose is it? Check by clicking devices and comparing MAC addresses. Why does that make sense? (Hint: think back to Flags 1 and 3.)

---

## What to submit

Submit at **[instructor: submission link]**:

1. **All 5 flags**, copied exactly.
2. **Short answers** (a sentence or two each) to every **Think about it** and the **Big puzzle**.
3. **One screenshot** of the PDU window from Flag 5, with the OSI Model tab open on the packet at STUDENT-PC.

The flags show you got there. The answers and screenshot show you understood the trail.

## Wrap-up: the whole trail in one picture

<details><summary><b>Spoilers: open this after Flag 5</b></summary>

Here's everything that happened when you loaded `http://www.cs124.lab/osi.html`, in order:

1. **DNS.** STUDENT-PC didn't know `www.cs124.lab`'s IP address, so it asked the DNS server. The DNS server is on a *different* network, so even this question went through the gateway.
2. **ARP.** To hand anything to the gateway, STUDENT-PC needed the gateway's MAC address, so it asked: "Who has the gateway's IP? Tell me your MAC." That's why the first try sometimes times out.
3. **TCP connection.** STUDENT-PC opened a connection to the web server on **port 80**, the well-known port for HTTP. (HTTPS uses **port 443**.)
4. **HTTP request.** The browser sent "GET /osi.html". Because it's plain HTTP, every device along the way *could* read it, like a postcard.
5. **Through the switch.** The switch looked at the **Layer 2** destination MAC, which was the gateway's, and sent the frame out the right port.
6. **Through the router.** The router kept the **Layer 3** source and destination IPs the same, lowered the **TTL** by 1, and wrapped the packet in a *new* **Layer 2** header addressed to the web server's MAC. MAC addresses only cover one hop. IP addresses cover the whole trip.
7. **The response.** The web server sent the page back the same way, with the source and destination swapped.
8. **The browser** displayed the page.

For HTTPS (Flag 4), step 3 goes to port 443, and the two sides agree on encryption before step 4. After that, devices in the middle can still see the IPs and ports, but not the page.

</details>

## Glossary

| Term | Plain-English meaning |
|---|---|
| **Network** | Computers connected so they can send each other data. |
| **Packet** | One small chunk of data traveling across a network, with addressing info wrapped around it. |
| **IP address** | A computer's address on a network, like `192.168.10.10`. Used to reach any computer, near or far. |
| **Subnet mask** | Says which part of an IP address is the "neighborhood." With `255.255.255.0`, everyone whose address starts with the same first three numbers is a neighbor. |
| **MAC address** | A hardware ID burned into a network card, like `00C5.1240.0010`. Used only to reach the next device on the same wire. |
| **Switch** | Connects devices in the same neighborhood and delivers frames using MAC addresses. |
| **Router** | Connects different neighborhoods (networks) and forwards packets using IP addresses. |
| **Default gateway** | The router your computer sends things to when the destination is outside its own neighborhood. |
| **DNS** | Domain Name System: the phonebook that turns names (`library.cs124.lab`) into IP addresses. |
| **Hostname** | A human-friendly name for a computer, like `www.cs124.lab`. |
| **HTTP** | HyperText Transfer Protocol: the language browsers and web servers use. Not encrypted. |
| **HTTPS** | HTTP inside an encrypted, sealed connection. |
| **Encryption** | Scrambling data so only the intended receiver can read it. |
| **Port** | A number that says which program on a computer should get a message. Web servers listen on well-known ports, and Flags 3 and 4 have you find them. |
| **Source / destination** | Where a packet came from / where it's going. |
| **TCP** | A Layer 4 protocol that makes sure data arrives complete and in order. Carries the port numbers. |
| **TTL** | Time To Live: a counter in every IP packet. Each router subtracts 1, and at 0 the packet is thrown away, so lost packets can't loop forever. |
| **OSI model** | A 7-layer way of describing how network communication is organized. This lab uses layers 2, 3, 4, and 7. |
| **Encapsulation** | Wrapping data in a new header at each layer on the way down. |
| **Port forwarding** | A router rule that sends traffic arriving at the router's own address to a different computer behind it. |
| **ping** | Sends a tiny "are you there?" message and waits for a reply. |
| **ipconfig** | Shows your computer's network settings. Add `/all` for more detail. |
| **nslookup** | Asks a DNS server to look up a name. |
| **tracert** | Lists every hop (router) between you and a destination. |
| **Simulation mode** | Packet Tracer's slow-motion mode for watching and inspecting packets one step at a time. |

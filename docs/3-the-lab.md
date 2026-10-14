# Step 3: The lab

Five flags, in order. Each flag page gives you the lead for the next one.

- **Always work from `STUDENT-PC`** (bottom left).
- **"Request timed out" on the first try?** That's normal. Try again.
- Don't know a word? Check the [glossary](glossary.md). Forgot how Packet Tracer works? See [Packet Tracer in 60 seconds](1-setup.md#packet-tracer-in-60-seconds).
- Keep notes as you go. You'll submit the flags *and* your answers to every **Think about it** ([what to submit](../writeup.md#what-to-submit)).

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

Done? Read the [wrap-up](wrap-up.md) to see the whole trail in one picture.

---

[1. Setup](1-setup.md) · [2. Big picture](2-big-picture.md) · **3. The lab** · [Glossary](glossary.md) · [Back to the start](../writeup.md)

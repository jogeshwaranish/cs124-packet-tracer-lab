# Step 2: The big picture

You don't need to understand all of this yet. Each flag zooms in on one piece. Come back here whenever a flag mentions an idea you don't recognize.

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

Next: [the lab](3-the-lab.md).

---

[1. Setup](1-setup.md) · **2. Big picture** · [3. The lab](3-the-lab.md) · [Glossary](glossary.md) · [Back to the start](../writeup.md)

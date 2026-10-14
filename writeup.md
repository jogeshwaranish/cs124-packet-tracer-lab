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
- **Watch** NetworkChuck's video on IP addresses: **[instructor: video link]**. It makes Flag 1 click.
- **Skim** the [glossary](docs/glossary.md). You don't need to memorize it. Just recognize the words when you see them.
- **Install Packet Tracer before the lab** ([setup guide](docs/1-setup.md)). The download needs an account, so don't leave it to the last minute.
- **Curiosity.** Click on things. Open every tab. If you break something, just reopen `lab.pkt`.

## How to do this MP

Work through these in order. Each one is short.

| Step | Read | What it's for | Time |
|---|---|---|---|
| 1 | [Setup](docs/1-setup.md) | Install Packet Tracer and open the lab | Do this at home, before the lab |
| 2 | [The big picture](docs/2-big-picture.md) | The ideas behind the flags, in plain English | ~10 min |
| 3 | [The lab](docs/3-the-lab.md) | The 5 flags, step by step | ~1.5 h |
| | [Glossary](docs/glossary.md) | Look up any word you don't know | As needed |
| After | [Wrap-up](docs/wrap-up.md) | The whole trail explained (spoilers) | After Flag 5 |

## What to submit

Submit at **[instructor: submission link]**:

1. **All 5 flags**, copied exactly.
2. **Short answers** (a sentence or two each) to every **Think about it** and the **Big puzzle**.
3. **One screenshot** of the PDU window from Flag 5, with the OSI Model tab open on the packet at STUDENT-PC.

The flags show you got there. The answers and screenshot show you understood the trail.

# Glossary

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

---

[1. Setup](1-setup.md) · [2. Big picture](2-big-picture.md) · [3. The lab](3-the-lab.md) · **Glossary** · [Back to the start](../writeup.md)

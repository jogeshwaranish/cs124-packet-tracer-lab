# Wrap-up: the whole trail in one picture

> **Spoilers.** Read this after you've finished Flag 5.

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

---

[1. Setup](1-setup.md) · [2. Big picture](2-big-picture.md) · [3. The lab](3-the-lab.md) · [Glossary](glossary.md) · [Back to the start](../writeup.md)

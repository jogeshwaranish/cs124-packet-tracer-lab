# ANSWER KEY (instructors only, do not share)

## Network

```
                     R1 (ISR4331)
          G0/0/0 192.168.10.1      G0/0/1 10.124.0.1
          MAC 00C5.1240.BEEF       MAC 00C5.1240.0001
          ip nat outside           ip nat inside
                 |                        |
            Gig0/1 (VLAN 10)        Gig0/2 (VLAN 20)
          +------------------ SW1 (2960-24TT) ------------------+
          Fa0/1    Fa0/2   Fa0/3     Fa0/11    Fa0/12   Fa0/13   Fa0/14
            |        |       |         |         |        |        |
       STUDENT-PC  PC-2    PC-3   DNS-SERVER WEB-SERVER  VAULT   GATE-WEB
          .10       .11     .12     .10        .20       .30      .40
       192.168.10.0/24 (clients)    10.124.0.0/24 (servers)
```

| Device | IP / mask | Gateway | DNS | MAC | Services |
|---|---|---|---|---|---|
| STUDENT-PC | 192.168.10.10 /24 | 192.168.10.1 | 10.124.0.10 | 00C5.1240.0010 | n/a |
| PC-2 | 192.168.10.11 /24 | 192.168.10.1 | 10.124.0.10 | 0090.2190.B085 | n/a |
| PC-3 | 192.168.10.12 /24 | 192.168.10.1 | 10.124.0.10 | 0002.4AB6.5352 | n/a |
| DNS-SERVER | 10.124.0.10 /24 | 10.124.0.1 | 10.124.0.10 | 00C5.1240.0053 | DNS only |
| WEB-SERVER | 10.124.0.20 /24 | 10.124.0.1 | 10.124.0.10 | 00C5.1240.0020 | HTTP only (port 80) |
| VAULT | 10.124.0.30 /24 | 10.124.0.1 | 10.124.0.10 | 00C5.1240.0030 | HTTPS only (port 443) |
| GATE-WEB | 10.124.0.40 /24 | 10.124.0.1 | 10.124.0.10 | 00C5.1240.0040 | HTTP only |
| R1 | G0/0/0 192.168.10.1, G0/0/1 10.124.0.1 | n/a | n/a | BEEF / 0001 | static NAT `tcp 10.124.0.40:80 ↔ 192.168.10.1:80` |

DNS A records: `library.cs124.lab` → 10.124.0.20, `www.cs124.lab` → 10.124.0.20, `vault.cs124.lab` → 10.124.0.30, `dns.cs124.lab` → 10.124.0.10.

## Flags

| # | Flag | How students reach it |
|---|---|---|
| 1 | `CS124{knock_knock_its_the_gateway}` | `ipconfig /all` → gateway 192.168.10.1 → browser `http://192.168.10.1` (R1 port-forwards to GATE-WEB) |
| 2 | `CS124{dns_is_the_internets_phonebook}` | `nslookup library.cs124.lab` → 10.124.0.20 → `http://library.cs124.lab` |
| 3 | `CS124{postcards_travel_on_port_80}` | Flag 2 page reveals `postcard.html` → Sim mode, first HTTP event **at WEB-SERVER** → Dst Port 80, L2 Src MAC …0001 (R1 server side) → `http://www.cs124.lab/port-80-0001.html` |
| 4 | `CS124{sealed_envelopes_use_port_443}` | Flag 3 page reveals the vault → Sim mode, first HTTPS event **at VAULT** → Dst Port 443, inbound TTL 127 → `https://vault.cs124.lab/port-443-127.html` |
| 5 | `CS124{osi_layer_cake_complete}` | Flag 4 page reveals `osi.html` → Sim mode → `http://www.cs124.lab/osi-beef-128-80-http.html` |

### Expected observations

- **Flag 1 `ipconfig /all`:** IPv4 192.168.10.10, mask 255.255.255.0, gateway 192.168.10.1, Physical Address 00C5.1240.0010, DNS server 10.124.0.10.
- **Flag 2 `nslookup`:** Server 10.124.0.10; library.cs124.lab → 10.124.0.20 (same as www). `tracert library.cs124.lab` → hop 1 192.168.10.1, hop 2 10.124.0.20.
- **Flag 3 packet (first HTTP event at WEB-SERVER):** L2 **src 00C5.1240.0001** (R1 G0/0/1) → dst 00C5.1240.0020; L4 **dst 80**.
- **Flag 4 packet (first HTTPS event at VAULT):** L3 **TTL 127** (128 minus one hop); L4 **dst 443**.
- **Flag 5 packet (first HTTP event at STUDENT-PC):** L2 src 00C5.1240.0010 → **dst 00C5.1240.BEEF** (R1, the gateway, not the server); L3 192.168.10.10 → 10.124.0.20, **TTL 128**; L4 TCP src ~1025 → **dst 80**; L7 **HTTP**.

### How the "answer pages" work

PT's browser can't run JavaScript or submit forms, so **the URL is the answer**. Each correct page exists only under the right file name. Common wrong answers have their own pages that explain the specific mistake:

- Flags 3 and 4 take two values: `port-PORT-MAC.html` on WEB-SERVER (MAC ∈ {0001 correct, 0020 = server's own/dst, 0010 = STUDENT-PC, beef = R1 client side}) and `port-PORT-TTL.html` on VAULT (TTL ∈ {127 correct, 128 = before R1, 126}). PORT ∈ {53, 80, 443, 1024–1030}. Every wrong pair lists which half is off. The old one-value `port-N.html` pages now say "you need two values", so guessing 80/443 alone gets nothing.
- `osi-{mac}-{ttl}-{port}-{proto}.html`, with every combination of mac ∈ {beef, 0010 = own MAC, 0020 = server MAC}, ttl ∈ {128, 127 = after the router}, port ∈ {80, 443, 1025–1027}, proto ∈ {http, tcp, https}. That's 89 hint pages plus 1 correct page. Wrong pages list exactly which layers are off.
- Anything else gives PT's normal "file not found."

Flags inside pages are written as HTML numeric entities (`&#67;&#83;...`). They show normally in the browser but are hard to read in the Services → HTTP editor.

## Test checklist (do this once in Packet Tracer before release)

Open `lab.pkt`, wait ~10 seconds in Realtime, then work from STUDENT-PC:

- [ ] All link lights are green (no red triangles).
- [ ] `ipconfig /all` matches the values above.
- [ ] `ping 192.168.10.1` succeeds (the first reply may time out).
- [ ] `ping 10.124.0.20` succeeds.
- [ ] `nslookup library.cs124.lab` returns 10.124.0.20.
- [ ] Browser `http://192.168.10.1` → Flag 1 page. **(Riskiest item: depends on PT's NAT emulation. See below.)**
- [ ] Browser `http://library.cs124.lab` → Flag 2 page; flag text is readable, not `&#67;...`.
- [ ] Flag 2 page shows the postcard lead. `http://www.cs124.lab/postcard.html` → page; `port-80-0001.html` → Flag 3; `port-80-beef.html` → hint page; `port-80.html` → "two values" page.
- [ ] **New, needs a PT check:** in Simulation, the first HTTP event at WEB-SERVER shows L2 Src MAC 00C5.1240.0001 and Dst Port 80.
- [ ] `http://vault.cs124.lab` fails; `https://vault.cs124.lab` → page; `/port-443-127.html` → Flag 4; `/port-443-128.html` → hint page.
- [ ] **New, needs a PT check:** the first HTTPS event at VAULT shows TTL 127 in Inbound PDU Details and Dst Port 443.
- [ ] Simulation: Event List shows DNS/HTTP/HTTPS only; the first HTTP PDU at STUDENT-PC shows Dest MAC 00C5.1240.BEEF, TTL 128, Dst Port 80, Layer 7 HTTP.
- [ ] `osi-beef-128-80-http.html` → Flag 5; `osi-0020-127-80-http.html` → hint page listing MAC + TTL.
- [ ] Click R1: the CLI tab should be hidden (file preference). If it isn't, see "Locking things down."

If a value differs (e.g. TTL), change `OSI_ANSWER`/hints in `tools/build_lab.py`, rebuild, and update this key.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| First ping or page load says "Request timed out" | ARP is still resolving MAC addresses. Retry; it works the second time. |
| Browser says "Request Timeout" right after opening the file | Links are still coming up. Wait ~10 s (or click **Fast Forward Time** at the bottom). |
| Event List is empty in Simulation | Filters were changed. Edit Filters → tick HTTP, HTTPS, DNS. Or the student pressed Go *before* switching to Simulation. |
| Only DNS events, no HTTP | Keep pressing Play/Capture Forward. HTTP comes after the DNS reply and TCP setup. |
| Student sees TTL 127 or dest MAC …0020 | They clicked the packet after R1. Pick the event where "At Device" = STUDENT-PC. |
| Dst Port shows 1025-ish | They read Src Port, or clicked the server's reply (reply packets have ports reversed). |
| `http://vault.cs124.lab` fails | On purpose: VAULT only runs HTTPS. |
| `http://10.124.0.40` fails | On purpose: GATE-WEB is only reachable through the gateway's port-forward. |
| Page shows `&#67;&#83;…` instead of text | That PT version doesn't decode entities. Set `ent = lambda s: s` in `build_lab.py` and rebuild. |
| Flag 1 page doesn't load at `http://192.168.10.1` | PT's NAT didn't take. Check on R1 (unhide CLI): `show ip nat translations` should list `tcp 192.168.10.1:80 10.124.0.40:80`. Fallback: in `build_lab.py`, swap R1 for any device that serves HTTP at the gateway IP, or move Flag 1 to `http://gate.cs124.lab` (one DNS record) and update the handout. |

## Known limitations / v2 ideas

- **Peeking:** Students can open a server's Services → HTTP tab and read page files. Entity encoding and 90+ look-alike files make that slower than doing the lab, but it's not a lock. For a real lock, convert to a `.pka` activity and use Activity Wizard → interface locking, or set Preferences → Hide → Services (but students lose "see what services a server runs").
- **Answers are guessable** by someone who already knows 80/443. Accepted: the goal is learning, not secrecy.
- **Same flags for everyone.** Per-student flags would need a `.pka` with variable seeds or a server-side checker.
- `HIDECLIOFROUTERANDSWITCH` is saved in the file's options. Some PT versions apply local preferences instead, so treat it as a convenience, not security.

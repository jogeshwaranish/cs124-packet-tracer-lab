# CS124 Packet Tracer lab: "The Packet Trail"

A ready-to-open Packet Tracer network (`lab.pkt`) with five flags. Students explore it; they never configure anything.

## Repository structure

```
cs124-packet-tracer-lab/
├── README.md              ← you are here (staff overview)
├── lab.pkt                ← the Packet Tracer network students open
├── writeup.md             ← student start page
├── docs/                  ← the rest of the student write-up, read in order
│   ├── 1-setup.md
│   ├── 2-big-picture.md
│   ├── 3-the-lab.md
│   ├── glossary.md
│   └── wrap-up.md
├── ANSWER_KEY.md          ← staff only
└── tools/                 ← scripts that build lab.pkt
    ├── build_lab.py
    ├── ptcrypt.js
    ├── package.json
    └── package-lock.json
```

### For students

Students need `lab.pkt` and the write-up. Nothing else.

| File | What it is |
|---|---|
| `lab.pkt` | The pre-built campus network: 3 PCs, a switch, a router, a DNS server, and 3 web servers. Students explore it. They never configure anything. |
| `writeup.md` | The start page: intro, learning goals, prerequisites, reading order, and what to submit. |
| `docs/1-setup.md` | Installing Packet Tracer on Windows, macOS, and Linux, opening the lab, and Packet Tracer basics. |
| `docs/2-big-picture.md` | The ideas behind the flags in plain English (addresses, gateway, DNS, ports, HTTP vs HTTPS, OSI layers). No spoilers. |
| `docs/3-the-lab.md` | The 5 flags with exact steps. Each flag page in the lab gives the lead for the next one. |
| `docs/glossary.md` | Plain-English definitions of every term used. |
| `docs/wrap-up.md` | The whole request path explained. Contains spoilers, so it's for after Flag 5. |

### For staff

| File | What it is |
|---|---|
| `ANSWER_KEY.md` | Network diagram and addresses, all flags and expected values, how the answer pages work, the **pre-release test checklist**, and troubleshooting. |
| `README.md` | This file. |

### Tools (only needed to change the lab)

| File | What it is |
|---|---|
| `tools/build_lab.py` | Generates `lab.pkt`. All IPs, MACs, flags, DNS records, and web-page text live here. |
| `tools/ptcrypt.js` | Encodes and decodes Packet Tracer files (format documented by the open-source pka2xml project). |
| `tools/package.json`, `package-lock.json` | Node dependency for `ptcrypt.js` (the pure-JS `twofish` package). |
| `build/` | Created when you build, and ignored by git. `lab.xml` is the readable XML of `lab.pkt`. |

## How lab.pkt is made

Packet Tracer files are compressed XML in a Twofish/EAX wrapper. `build_lab.py` decodes Cisco's own bundled example `DNS-A-and-AAAA-records.pkt` (which has every device model we need), rewires it into the lab network (renames, IPs, MACs, VLANs, router NAT, DNS records, about 185 web pages, notes, simulation filters), and re-encodes it. The result is saved in PT 8.0 format, so PT 8.x and 9.x can open it.

To change only page wording, flags, or DNS records, you don't need the PT base file. Refresh the existing file in place:

```bash
cd tools && npm install
python3 build_lab.py --update ../lab.pkt
```

To change anything else (an IP, a MAC, the topology), do a full rebuild:

```bash
cd tools && npm install          # once: pulls the pure-JS twofish package
python3 build_lab.py --base "<Packet Tracer install>/saves/01 Networking/IPv6/DNS-A-and-AAAA-records.pkt"
```

On this machine the PT install is an AppImage. Extract it with `/opt/pt/packettracer.AppImage --appimage-extract`, and the base file is under `squashfs-root/opt/pt/saves/…`.

## Before release

1. Open `lab.pkt` in Packet Tracer and run the **test checklist** in `ANSWER_KEY.md`.
2. Optional: File → Save once from Packet Tracer, so the file is stamped by your PT version.
3. Fill in the `[instructor: …]` links: video and submission in `writeup.md`, download in `docs/1-setup.md`.

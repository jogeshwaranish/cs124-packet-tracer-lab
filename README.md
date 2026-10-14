# CS124 Packet Tracer lab: "The Packet Trail"

A ready-to-open Packet Tracer network (`lab.pkt`) with five flags. Students explore it; they never configure anything.

| File | For |
|---|---|
| `lab.pkt` | **Give this to students.** The pre-built campus network. |
| `writeup.md` | **Student start page.** Intro, learning goals, prerequisites, reading order, what to submit. |
| `docs/1-setup.md` | Students: install Packet Tracer (Windows/macOS/Linux), open the lab, Packet Tracer basics. |
| `docs/2-big-picture.md` | Students: the ideas behind the flags, no spoilers. |
| `docs/3-the-lab.md` | Students: the 5 flags with exact steps. |
| `docs/glossary.md`, `docs/wrap-up.md` | Students: word list, and the full explanation (spoilers, for after Flag 5). |
| `ANSWER_KEY.md` | Staff only. Flags, expected values, **pre-release test checklist**, troubleshooting. |
| `tools/build_lab.py` | Regenerates `lab.pkt`. All IPs, flags, and page text live here. |
| `tools/ptcrypt.js` | Packet Tracer file encoder/decoder (format documented by the open-source pka2xml project). |
| `build/` | Disposable build output (`lab.xml` is the readable XML of `lab.pkt`). |

## How lab.pkt is made

Packet Tracer files are compressed XML in a Twofish/EAX wrapper. `build_lab.py` decodes Cisco's own bundled example `DNS-A-and-AAAA-records.pkt` (which has every device model we need), rewires it into the lab network (renames, IPs, MACs, VLANs, router NAT, DNS records, 115 web pages, notes, simulation filters), and re-encodes it. The result is saved in PT 8.0 format, so PT 8.x and 9.x can open it.

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

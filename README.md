# CS124 Packet Tracer lab: "The Packet Trail"

A ready-to-open Packet Tracer network (`lab.pkt`) with five flags. Students explore it; they never configure anything.

| File | For |
|---|---|
| `lab.pkt` | **Give this to students.** The pre-built campus network. |
| `STUDENT_HANDOUT.md` | Give to students. Setup, the 5 stages with exact commands, glossary. Fill in the two `[instructor: …]` links. |
| `ANSWER_KEY.md` | Staff only. Flags, expected values, **pre-release test checklist**, troubleshooting. |
| `tools/build_lab.py` | Regenerates `lab.pkt`. All IPs, flags, and page text live here. |
| `tools/ptcrypt.js` | Packet Tracer file encoder/decoder (format documented by the open-source pka2xml project). |
| `build/` | Disposable build output (`lab.xml` is the readable XML of `lab.pkt`). |

## How lab.pkt is made

Packet Tracer files are compressed XML in a Twofish/EAX wrapper. `build_lab.py` decodes Cisco's own bundled example `DNS-A-and-AAAA-records.pkt` (which has every device model we need), rewires it into the lab network (renames, IPs, MACs, VLANs, router NAT, DNS records, 115 web pages, notes, simulation filters), and re-encodes it. The result is saved in PT 8.0 format, so PT 8.x and 9.x can open it.

To change anything (a flag, an IP, page wording):

```bash
cd tools && npm install          # once: pulls the pure-JS twofish package
python3 build_lab.py --base "<Packet Tracer install>/saves/01 Networking/IPv6/DNS-A-and-AAAA-records.pkt"
```

On this machine the PT install is an AppImage. Extract it with `/opt/pt/packettracer.AppImage --appimage-extract`, and the base file is under `squashfs-root/opt/pt/saves/…`.

## Before release

1. Open `lab.pkt` in Packet Tracer and run the **test checklist** in `ANSWER_KEY.md`.
2. Optional: File → Save once from Packet Tracer, so the file is stamped by your PT version.
3. Fill in the submission link and video link in `STUDENT_HANDOUT.md`.

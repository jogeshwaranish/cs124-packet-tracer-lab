# Step 1: Setup

Packet Tracer is free, but Cisco requires a free **Cisco Networking Academy (NetAcad)** account to download it and to log in the first time you run it.

## 1. Make a NetAcad account

1. Go to <https://www.netacad.com> and sign up. A personal or school email both work.
2. Find the **Download Packet Tracer** page. Search "Packet Tracer" on the site, or look under Resources. If you only see a course page, enroll in the free self-paced **Getting Started with Cisco Packet Tracer** course. The download links are in its resources.
3. Download **version 8.2 or newer** for your operating system.

## 2. Install

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

## 3. Open the lab

1. Download **`lab.pkt`**: **[instructor: download link]**.
2. In Packet Tracer, choose **File → Open** and pick `lab.pkt`.
3. You should see the campus network. If Packet Tracer says the file is from a newer version, update Packet Tracer.
4. Wait about 10 seconds for all the link lights to turn green. Or click **Fast Forward Time** at the bottom of the window.

## Packet Tracer in 60 seconds

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

When the lab is open and the lights are green, you're ready. Next: [the big picture](2-big-picture.md).

---

**1. Setup** · [2. Big picture](2-big-picture.md) · [3. The lab](3-the-lab.md) · [Glossary](glossary.md) · [Back to the start](../writeup.md)

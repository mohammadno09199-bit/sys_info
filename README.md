یک فایل `README.md` حرفه‌ای، تمیز و استاندارد (به زبان انگلیسی هم‌راستا با اسکریپت) برای پروژه‌ات آماده کردم:

```markdown
# Python System Information Tool 🖥️

A lightweight and clean Python script to gather detailed hardware and system specifications (CPU, RAM, GPU, Storage, Network, and Battery) across different operating systems.

---

## Features

- **System & OS Info:** Detects OS release, architecture, hostname, and system boot time.
- **Advanced CPU Details:** Retrieves exact processor brand/model, physical cores, threads, and current/max frequencies.
- **Memory Tracking:** Monitors total, available, and used RAM along with Swap space.
- **GPU Diagnostics:** Detects dedicated graphics cards (NVIDIA/AMD) via `GPUtil`, tracking VRAM, temperature, and load.
- **Storage Breakdown:** Lists all active storage partitions with total size, usage percentage, and file system types.
- **Network Interfaces:** Scans active network interfaces with their respective IPv4 and MAC addresses.
- **Battery Status:** Reports battery percentage, power plug status, and estimated remaining time for laptops.

---

## Prerequisites

Make sure you have Python 3.x installed on your system.

---

## Installation & Setup

It is recommended to run this script inside a Python Virtual Environment to avoid system-wide package restrictions (such as PEP 668 on Debian/Kali Linux).

### 1. Clone or download the project files
Open your terminal in the project directory.

### 2. Create a virtual environment
```bash
python3 -m venv venv
```

### 3. Activate the virtual environment
- **Linux / macOS:**
  ```bash
  source venv/bin/activate
  ```
- **Windows (CMD / PowerShell):**
  ```cmd
  venv\Scripts\activate
  ```

### 4. Install required dependencies
```bash
pip install psutil py-cpuinfo gputil tabulate
```

---

## Usage

Run the script directly in your terminal:
```bash
python3 sys_info.py
```

### Saving Output to a File
If you want to print the specifications on the screen and simultaneously save them to a text file:
```bash
python3 sys_info.py | tee system_report.txt
```

---

## Deactivation
When you are done, you can deactivate the virtual environment:
```bash
deactivate
```

---

## License
This project is open-source and free to use for personal and professional tasks.
```

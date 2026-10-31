import os
import platform
import socket
import psutil
import cpuinfo
from datetime import datetime

try:
    import GPUtil
except ImportError:
    GPUtil = None


def get_size(bytes_val, suffix="B"):
    """Scale bytes to proper human-readable format like KB, MB, GB, etc."""
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes_val < factor:
            return f"{bytes_val:.2f} {unit}{suffix}"
        bytes_val /= factor
    return f"{bytes_val:.2f} P{suffix}"


def print_header(title):
    print("\n" + "=" * 60)
    print(f" {title.center(56)} ")
    print("=" * 60)


def main():
    # --- System Information ---
    print_header("System Information")
    uname = platform.uname()
    print(f"OS:                 {uname.system} {uname.release}")
    print(f"OS Version:         {platform.version()}")
    print(f"Architecture:       {uname.machine}")
    print(f"Hostname:           {uname.node}")
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    print(f"Boot Time:          {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # --- CPU Information ---
    print_header("CPU Information")
    c_info = cpuinfo.get_cpu_info()
    print(f"Processor Model:    {c_info.get('brand_raw', 'Unknown')}")
    print(f"Architecture:       {c_info.get('arch', 'Unknown')}")
    print(f"Physical Cores:     {psutil.cpu_count(logical=False)}")
    print(f"Total Threads:      {psutil.cpu_count(logical=True)}")

    cpufreq = psutil.cpu_freq()
    if cpufreq:
        print(f"Max Frequency:      {cpufreq.max:.2f} MHz")
        print(f"Current Frequency:  {cpufreq.current:.2f} MHz")
    print(f"Total CPU Usage:    {psutil.cpu_percent(interval=1)}%")

    # --- Memory Information (RAM) ---
    print_header("Memory Information (RAM)")
    svmem = psutil.virtual_memory()
    print(f"Total RAM:          {get_size(svmem.total)}")
    print(f"Available RAM:      {get_size(svmem.available)}")
    print(f"Used RAM:           {get_size(svmem.used)} ({svmem.percent}%)")

    swap = psutil.swap_memory()
    print(f"Total Swap:         {get_size(swap.total)}")
    print(f"Used Swap:          {get_size(swap.used)} ({swap.percent}%)")

    # --- GPU Information ---
    print_header("GPU Information")
    if GPUtil:
        gpus = GPUtil.getGPUs()
        if gpus:
            for i, gpu in enumerate(gpus):
                print(f"[GPU {i + 1}]")
                print(f"  Model Name:       {gpu.name}")
                print(f"  Total VRAM:       {gpu.memoryTotal} MB")
                print(f"  Used VRAM:        {gpu.memoryUsed} MB")
                print(f"  Temperature:      {gpu.temperature} °C")
                print(f"  GPU Load:         {gpu.load * 100:.1f}%")
        else:
            print("No dedicated GPU (e.g., NVIDIA) detected.")
    else:
        print("GPUtil module not available.")

    # --- Storage / Partitions ---
    print_header("Storage / Partitions")
    partitions = psutil.disk_partitions(all=False)
    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        print(f"Device / Mount:     {partition.device} -> {partition.mountpoint}")
        print(f"  File System:      {partition.fstype}")
        print(f"  Total Size:       {get_size(partition_usage.total)}")
        print(f"  Used:             {get_size(partition_usage.used)} ({partition_usage.percent}%)")
        print(f"  Free:             {get_size(partition_usage.free)}")
        print("-" * 30)

    # --- Network Interfaces ---
    print_header("Network Interfaces")
    if_addrs = psutil.net_if_addrs()
    for interface_name, addresses in if_addrs.items():
        ipv4 = []
        mac = []
        for address in addresses:
            if str(address.family) == 'AddressFamily.AF_INET' or address.family == socket.AF_INET:
                ipv4.append(address.address)
            elif str(address.family) == 'AddressFamily.AF_PACKET' or address.family == psutil.AF_LINK:
                mac.append(address.address)

        if ipv4 or mac:
            print(f"Interface: {interface_name}")
            if mac:
                print(f"  MAC Address:      {mac[0]}")
            if ipv4:
                print(f"  IP Address:       {', '.join(ipv4)}")
            print("-" * 20)

    # --- Battery Status ---
    battery = psutil.sensors_battery()
    if battery:
        print_header("Battery Status")
        print(f"Battery Percentage: {battery.percent}%")
        print(f"Power Plugged In:   {'Yes' if battery.power_plugged else 'No'}")
        if not battery.power_plugged and battery.secsleft != psutil.POWER_TIME_UNLIMITED:
            hours, remainder = divmod(battery.secsleft, 3600)
            minutes, _ = divmod(remainder, 60)
            print(f"Remaining Time:     {int(hours)} hours and {int(minutes)} minutes")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()

import os
import platform
import time

import psutil
import speedtest
import wmi
from pyrogram import Client, __version__, filters, raw
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM
from pyrogram.types import Message

from config import SUDO_USERS

system_information = {}

def current_speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1e+6
    upload_speed = st.upload() / 1e+6
    
    return f"Download Speed: {download_speed:.2f} Mbps", f"Upload Speed: {upload_speed:.2f} Mbps"


def detect_disk_type():
    system = platform.system()
    if system == "Windows":
        try:
            wmi_client = wmi.WMI()
            for disk in wmi_client.Win32_DiskDrive():
                if disk.MediaType is None or "SSD" not in disk.MediaType:
                    if hasattr(disk, "RotationRate") and disk.RotationRate == 0:
                        type_ = "SSD"
                    else:
                        type_ = "HDD"
                else:
                    type_ = disk.MediaType
                return disk.Caption, type_
        except Exception as e:
            return "N/A", "N/A"
    elif system == "Linux":
        try:
            for disk in os.listdir('/sys/block'):
                rotational_file = f"/sys/block/{disk}/queue/rotational"
                if os.path.exists(rotational_file):
                    with open(rotational_file, 'r') as f:
                        is_rotational = f.read().strip()
                        disk_type = "HDD" if is_rotational == '1' else "SSD"
                        return disk, disk_type
        except Exception as e:
            print(f"Error: {e}")
            return "N/A", "N/A"
    else:
        print(f"Disk type detection is not supported on {system}.")
        return "N/A", "N/A"


def get_system_info(info_type: str = "system"):
    """Type of info you want to collect
    available types: system, cpu, memory, disk
    """
    global system_information

    info_type = info_type.lower()
    if _info := system_information.get(info_type, None):
        return _info[0], _info[1]

    if info_type == "system":
        # Collects info about os and system
        system_info = {
            "System": platform.system(),
            "Node Name": platform.node(),
            "Release": platform.release(),
            "Version": platform.version(),
            "Machine": platform.machine(),
            "Processor": platform.processor(),
            "Architecture": platform.architecture()[0],
            "Pyrogram version": __version__,
            "Python version": platform.python_version()
        }

        kb = IKM([[IKB("CPU info", "info_cpu"), IKB("Memory info", "info_memory")], [IKB("Disk info", "info_disk"), IKB("Network info", "info_network")]])

        system_information[info_type] = (system_info, kb)

        return system_info, kb

    elif info_type == "cpu":
        # Collects info about cpu
        cpu_info = {
            "Physical Cores": psutil.cpu_count(logical=False),
            "Total Cores": psutil.cpu_count(logical=True),
            "Max Frequency (MHz)": psutil.cpu_freq().max if psutil.cpu_freq() else "N/A",
            "Min Frequency (MHz)": psutil.cpu_freq().min if psutil.cpu_freq() else "N/A",
            "Current Frequency (MHz)": psutil.cpu_freq().current if psutil.cpu_freq() else "N/A",
            "CPU Usage (%)": psutil.cpu_percent(interval=1),
        }

        kb = IKM([[IKB("System info", "info_system"), IKB("Memory info", "info_memory")], [IKB("Disk info", "info_disk"), IKB("Network info", "info_network")]])
        
        system_information[info_type] = (cpu_info, kb)

        return cpu_info, kb

    elif info_type == "memory":
        # Collects info about memory
        virtual_memory = psutil.virtual_memory()
        memory_info = {
            "Total Memory (GB)": virtual_memory.total / (1024 ** 3),
            "Available Memory (GB)": virtual_memory.available / (1024 ** 3),
            "Used Memory (GB)": virtual_memory.used / (1024 ** 3),
            "Memory Usage (%)": virtual_memory.percent,
        }

        kb = IKM([[IKB("System info", "info_system"), IKB("CPU info", "info_cpu")], [IKB("Disk info", "info_disk"), IKB("Network info", "info_network")]])
        
        system_information[info_type] = (memory_info, kb)

        return memory_info, kb

    elif info_type == "disk":
        # Disk details
        disk_usage = psutil.disk_usage('/')
        disk, type_ = detect_disk_type()
        disk_info = {
            "Drive": disk,
            "Type": type_,
            "Total Disk Space (GB)": disk_usage.total / (1024 ** 3),
            "Used Disk Space (GB)": disk_usage.used / (1024 ** 3),
            "Free Disk Space (GB)": disk_usage.free / (1024 ** 3),
            "Disk Usage (%)": disk_usage.percent,
        }

        kb = IKM([[IKB("System info", "info_system"), IKB("CPU info", "info_cpu")], [IKB("Memory info", "info_memory"), IKB("Network info", "info_network")]])
        
        system_information[info_type] = (disk_info, kb)

        return disk_info, kb

    elif info_type == "network":
        # Network details
        interfaces = psutil.net_if_stats()
        for interface_name, stats in interfaces.items():
            if stats.isup:
                network_info = {
                    "Interface": interface_name,
                    "Speed": f"{stats.speed} Mbps",
                    "Duplex": 'Full' if stats.duplex == 2 else 'Half',
                    "MTU": stats.mtu
                }

        kb = IKM([[IKB("System info", "info_system"), IKB("CPU info", "info_cpu")], [IKB("Memory info", "info_memory"), IKB("Disk info", "info_disk")]])
        
        system_information[info_type] = (network_info, kb)

        return network_info, kb

    else:
        return None, None
"""
    return {
        "System Info": system_info,
        "CPU Info": cpu_info,
        "Memory Info": memory_info,
        "Disk Info": disk_info,
        "Network Info": network_details,
    }
""" # may be needed in future


@Client.on_message(filters.command(["sinfo", "info"]) & filters.user(SUDO_USERS))
async def give_system_info(c: Client, m: Message):
    if len(m.command) > 1:
        info_abt = m.command[1]
        info, kb = get_system_info(info_abt)
        
        if not info:
            info, kb = get_system_info()
            info_abt = "System"

    else:
        info, kb = get_system_info()
        info_abt = "System"

    rnd = c.rnd_id()

    start = time.perf_counter()
    await c.invoke(raw.functions.Ping(ping_id=rnd))
    ping = (time.perf_counter()-start) * 1000
    

    txt = f"**Current Ping: {ping}**\n**Info about {info_abt}:**\n"

    for key, value in info.items():
        txt += f"• {key}: `{value}`\n"

    if info_abt == "network":
        download, upload = current_speed()
        txt += f"{download}\n"
        txt += upload

    await m.reply_text(txt, reply_markup=kb)
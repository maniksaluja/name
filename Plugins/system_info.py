import platform

import psutil
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM
from pyrogram.types import Message

from config import SUDO_USERS


def get_system_info(info_type: str = "system"):
    """Type of info you want to collect
    available types: system, cpu, memory, disk, network
    """
    info_type = info_type.lower()
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
        }

        kb = IKM([[IKB("CPU info", "info_cpu"), IKB("Memory info", "info_memory")], [IKB("Disk info", "info_disk"), IKB("Network info", "info_network")]])

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
        
        return memory_info, kb

    elif info_type == "disk":
        # Disk details
        disk_usage = psutil.disk_usage('/')
        disk_info = {
            "Total Disk Space (GB)": disk_usage.total / (1024 ** 3),
            "Used Disk Space (GB)": disk_usage.used / (1024 ** 3),
            "Free Disk Space (GB)": disk_usage.free / (1024 ** 3),
            "Disk Usage (%)": disk_usage.percent,
        }

        kb = IKM([[IKB("System info", "info_system"), IKB("CPU info", "info_cpu")], [IKB("Memory info", "info_memory"), IKB("Network info", "info_network")]])
        
        return disk_info, kb

    elif info_type == "network":
        # Network details
        network_info = psutil.net_if_addrs()
        network_details = {
            interface: [
                {
                    "Address": addr.address,
                    "Netmask": addr.netmask,
                    "Broadcast": addr.broadcast,
                }
                for addr in addresses
            ]
            for interface, addresses in network_info.items()
        }

        kb = IKM([[IKB("System info", "info_system"), IKB("CPU info", "info_cpu")], [IKB("Memory info", "info_memory"), IKB("Disk info", "info_disk")]])
        
        return network_details, kb

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
async def give_system_info(_, m: Message):
    if len(m.command) > 1:
        info_abt = m.command[1]
        info, kb = get_system_info(info_abt)
        
        if not info:
            info, kb = get_system_info()
            info_abt = "System"

    else:
        info, kb = get_system_info()
        info_abt = "System"

    txt = f"**Info about {info_abt}:**\n"

    for key, value in info.items():
        txt += f"• {key}: `{value}`\n"

    await m.reply_text(txt, reply_markup=kb)
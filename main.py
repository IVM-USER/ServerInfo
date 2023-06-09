import os
import platform
import sys
from base.module import command, BaseModule
from pyrogram.types import Message
import psutil


def b2mb(b):
    return round(b / 1024 / 1024, 1)


def find_lib(lib: str) -> str:
    try:
        ver = os.popen(f"python3 -m pip freeze | grep {lib}").read().split("==")[1]
        if "\n" in ver:
            return ver.split("\n")[0]
        return ver
    except Exception:
        return "Not Installed"


def escape_html(txt: str) -> str:
    return txt.replace("<", "").replace(">", "")


ssinfo = (
    "<b><u>👾 Server Info:</u>\n\n"
    "<u>🗄 Used resources:</u>\n"
    "    CPU: {} Cores {}%\n"
    "    RAM: {} / {}MB ({}%)\n\n"
    "<u>🧾 Dist info</u>\n"
    "    Kernel: {}\n    Arch: {}\n"
    "    OS: {}\n\n"
    "<u>📦 Python libs:</u>\n"
    "    Pyrogram: {}\n"
    "    Aiohttp: {}\n"
    "    GitPython: {}\n"
    "    Python: {}\n"
    "    Pip: {}</b>"
)


class ServerInfo(BaseModule):
    @command("serverinfo")
    async def si(self, _, message: Message):
        """Module that shows the characteristics of the server"""
        inf = []
        try:
            inf.append(psutil.cpu_count(logical=True))
        except Exception:
            inf.append("n/a")

        try:
            inf.append(psutil.cpu_percent())
        except Exception:
            inf.append("n/a")

        try:
            inf.append(
                b2mb(psutil.virtual_memory().total - psutil.virtual_memory().available)
        )
        except Exception:
            inf.append("n/a")

        try:
            inf.append(b2mb(psutil.virtual_memory().total))
        except Exception:
            inf.append("n/a")

        try:
            inf.append(psutil.virtual_memory().percent)
        except Exception:
            inf.append("n/a")

        try:
            inf.append(escape_html(platform.release()))
        except Exception:
            inf.append("n/a")

        try:
            inf.append(escape_html(platform.architecture()[0]))
        except Exception:
            inf.append("n/a")

        try:
            system = os.popen("cat /etc/*release").read()
            b = system.find('DISTRIB_DESCRIPTION="') + 21
            system = system[b : system.find('"', b)]
            inf.append(escape_html(system))
        except Exception:
            inf.append("n/a")

        try:
            inf.append(find_lib("Pyrogram"))
        except Exception:
            inf.append("n/a")

        try:
            inf.append(find_lib("aiohttp"))
        except Exception:
            inf.append("n/a")

        try:
            inf.append(find_lib("GitPython"))
        except Exception:
            inf.append("n/a")

        try:
            inf.append(
            f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        )
        except Exception:
            inf.append("n/a")

        try:
            inf.append(os.popen("python3 -m pip --version").read().split()[1])
        except Exception:
            inf.append("n/a")

        await message.reply(ssinfo.format(*inf))

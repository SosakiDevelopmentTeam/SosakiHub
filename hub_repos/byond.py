import asyncio
from asyncio import subprocess
import os.path as osp
import os

DREAMMAKER = "DreamMaker" if os.name == "posix" else osp.join(os.environ["BYOND_BIN"], "dm.exe")

class BYOND:

    def __init__(self, dme_path):
        self.path = dme_path
        self.proc = None

    async def build(self):
        proc = await subprocess.create_subprocess_exec(f'"{DREAMMAKER}" {self.path} -max_errors 10', stdout=subprocess.PIPE)
        stdout, stderr = await proc.communiate()
        return stdout

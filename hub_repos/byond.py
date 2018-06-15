import asyncio
from asyncio import subprocess
import os.path as osp
import os

is_win = 0 if os.name == "posix" else 1
DREAMMAKER = f'"{osp.join(os.environ["BYOND_BIN"], "dm.exe")}"' if is_win else "DreamMaker"

class BYOND:

    def __init__(self, dme_path):
        self.path = dme_path
        self.proc = None

    async def build(self):
        proc = await subprocess.create_subprocess_exec(f'{DREAMMAKER} {self.path} -max_errors 10', stdout=subprocess.PIPE)
        stdout, stderr = await proc.communiate()
        return stdout

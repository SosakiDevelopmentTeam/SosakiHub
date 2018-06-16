import asyncio
from asyncio import subprocess
import os.path as osp
import os
from types import *

BUILDING = 0xA
STARTING = 0xA

is_win = 0 if os.name == "posix" else 1
DREAMMAKER = f'"{osp.join(os.environ["BYOND_BIN"], "dm.exe")}"' if is_win else "DreamMaker"
DREAMDAEMON = f'"{osp.join(os.environ["BYOND_BIN"], "dreamdaemon.exe")}"' if is_win else "DreamDaemon"


def dict_to_params(val: dict, l: LambdaType = lambda x: ...) -> str:
    s = ""
    if not len(val):
        return s
    for key in val:
        if l(key):
            s += f"-{key} {val[key]} "
    return s


class BYOND:

    def __init__(self, dme_path):
        self.path = dme_path
        self.proc = None

    async def build(self):
        yield {"output": None, "return_code": BUILDING}
        proc = await subprocess.create_subprocess_shell(f'{DREAMMAKER} {self.path} -max_errors 10',
                                                       stdout=subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        await proc.terminate()
        yield {"output": stdout, "return_code": proc.returncode}

    async def start(self, parameters: dict = None):
        yield {"output": None, "return_code": STARTING}
        build_f = osp.join(osp.dirname(self.path), f"{osp.basename(self.path)[:-4]}.dmb")
        if osp.isfile(build_f):
            proc = await subprocess.create_subprocess_shell(f'{DREAMDAEMON} {build_f} {dict_to_params(parameters)}',
                                                           stdout=subprocess.PIPE)
            stdout, stderr = await proc.communicate()
            yield {"output": stdout, "return_code": proc.returncode}
        yield {"output": "No such file or directory", "return_code": 1}

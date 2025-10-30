import os
import shlex

from src.modules.pwd_handler import PwdHandler
from src.modules.ls_handler import LsHandler
from src.modules.mv_handler import MvHandler
from src.modules.rm_handler import RmHandler
from src.modules.cat_handler import CatHandler
from src.modules.cp_handler import CpHandler
from src.modules.cd_handler import CdHandler

import platform
from typing import Protocol

UNIX = True if platform.system() == "Darwin" else False

class CommandHandler(Protocol):
    def execute(self, args: list[str], shell: "Bash") -> None | str: ...


class Bash:
    def __init__(self) -> None:
        self.current_directory = os.getcwd()
        self.complex_commands: dict[str, CommandHandler] = {
            "pwd": PwdHandler(),
            "ls": LsHandler(),
            "cd": CdHandler(),
            "rm": RmHandler(),
            "cat": CatHandler(),
            "cp": CpHandler(),
            "mv": MvHandler(),
        }

    def execute(self, command_line: str) -> None | str:
        command, args = self.parse_command(command_line)
        if command in self.complex_commands:
            return self.complex_commands[command].execute(args, self)
        else:
            return f"Command not found: {command}"

    def parse_command(self, command_line: str) -> tuple[str, list[str]]:
        parts = shlex.split(command_line)
        return parts[0], parts[1::]

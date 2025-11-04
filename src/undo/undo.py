import json
import shutil
import os

from src.constants import HISTORY_FILE
from src.constants import TRASH
from src.constants import UNDO_COMMANDS

from src.modules.logger import log_command


class UndoHandler:
    @log_command
    def execute(self, args: list[str], shell) -> None:
        if len(args) > 1:
            raise ValueError("undo: Too many arguments")
        command = args[0] if args else ""
        if command not in UNDO_COMMANDS and not command.isdigit():
            raise ValueError(f"undo: You cannot cancel the command {command} or this command doesn't exist")
        self.find_command(command)

    def find_command(self, command: str) -> None:
        command_handler = {
            "cp": self.handle_undo_cp,
            "mv": self.handle_undo_mv,
            "rm": self.handle_undo_rm,
        }
        with open(HISTORY_FILE, "r") as read:
            data = json.load(read)
            for command_id, cmd in enumerate(data["stack"][-1::-1]):
                if (cmd["command"] == command) or (str(cmd["id"]) == command) or (
                        command == "" and cmd["command"] in ["cp", "rm", "mv"]):
                    data["stack"].pop(len(data["stack"]) - command_id - 1)
                    command_handler[cmd["command"]](cmd["src"], cmd["dst"])
                    with open(HISTORY_FILE, "w") as write:
                        json.dump(data, write, indent=4)
                    return
            raise ValueError("undo: Nothing to or command not found")

    def handle_undo_cp(self, src: str, dst: str) -> None:
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        else:
            os.remove(dst)

    def handle_undo_mv(self, src: str, dst: str) -> None:
        source = os.path.join(dst, os.path.basename(src))
        target = os.path.dirname(src)
        shutil.move(source, target)

    def handle_undo_rm(self, src: str, dst: str) -> None:
        source = os.path.join(TRASH, os.path.basename(src))
        target = os.path.dirname(src)
        shutil.move(source, target)

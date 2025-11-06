import json
import shutil
import os

from src.constants import HISTORY_FILE
from src.constants import TRASH
from src.constants import UNDO_COMMANDS

from src.modules.logger import log_command


def remove_empty_folders(path):
    if not os.path.isdir(path):
        return

    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            remove_empty_folders(item_path)

    if not os.listdir(path):
        os.rmdir(path)


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
                if (cmd["command"] == command) or (
                        command == "" and cmd["command"] in ["cp", "rm", "mv"]):
                    data["stack"].pop(len(data["stack"]) - command_id - 1)
                    command_handler[cmd["command"]](cmd["args"], cmd["cwd"])
                    with open(HISTORY_FILE, "w") as write:
                        json.dump(data, write, indent=4)
                    return
            raise ValueError("undo: Nothing to undo or command not found")

    def handle_undo_cp(self, args: list[str], cwd: str) -> None:
        key = [arg for arg in args if arg.startswith("-")]
        args = [arg for arg in args if not arg.startswith("-")]
        if "-r" in key:
            path = os.path.join(cwd, args[-1])
            shutil.rmtree(path)
        else:
            path = os.path.join(cwd, args[-1])
            os.remove(path)
        parent_dir = os.path.dirname(path)
        remove_empty_folders(parent_dir)

    def handle_undo_mv(self, args: list[str], cwd: str) -> None:
        source = os.path.join(cwd, args[1])
        source = os.path.join(source, args[0])
        target = cwd
        shutil.move(source, target)

    def handle_undo_rm(self, args: list[str], cwd: str) -> None:
        for i in range(len(args)):
            source = os.path.join(TRASH, args[i].split("/")[-1])
            target = os.path.join(cwd, args[i])
            shutil.move(source, target)

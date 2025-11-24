import json
import shutil
import os
import hashlib

from src.constants import HISTORY_FILE
from src.constants import TRASH
from src.constants import UNDO_COMMANDS

from src.modules.logger import log_command


class UndoHandler:
    """Implementation of 'undo' command to reverse file operations.

    Supports undoing copy (cp), move (mv), and remove (rm) commands
    by tracking command history and reversing the file operations.
    """

    @log_command
    def execute(self, args: list[str], shell) -> None:
        """Run undo command with specified target."""
        if len(args) > 1:
            raise ValueError("undo: Too many arguments")
        command = args[0] if args else ""
        if command not in UNDO_COMMANDS and not command.isdigit():
            raise ValueError(f"undo: You cannot cancel the command {command} or this command doesn't exist")
        self.find_command(command)

    def find_command(self, command: str) -> None:
        """Find the target command in history and execute undo operation."""
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
                    args, cwd = cmd["args"], cmd["cwd"]
                    with open(HISTORY_FILE, "w") as write:
                        json.dump(data, write, indent=4)
                    command_handler[cmd["command"]](args, cwd)
                    return
            raise ValueError("undo: Nothing to undo or command not found")

    def handle_undo_cp(self, args: list[str], cwd: str) -> None:
        keys = [arg for arg in args if arg.startswith("-")]
        files = [arg for arg in args if not arg.startswith("-")]

        if len(files) < 2:
            raise ValueError("undo: cp: not enough arguments")

        src = files[0]
        dst = files[1]

        src_path = os.path.abspath(os.path.join(cwd, src))
        dst_path = os.path.abspath(os.path.join(cwd, dst))

        src_name = os.path.basename(src_path)

        possible = os.path.join(dst_path, src_name)

        if os.path.exists(possible):
            target = possible
        else:
            target = dst_path

        if "-r" in keys:
            shutil.rmtree(target)
        else:
            os.remove(target)

    def handle_undo_mv(self, args: list[str], cwd: str) -> None:
        """Undo move operation by moving file back to original location."""
        source = os.path.join(cwd, args[1])
        source = os.path.join(source, args[0])
        target = cwd
        shutil.move(source, target)

    def handle_undo_rm(self, args: list[str], cwd: str) -> None:
        """Undo remove operation by restoring files from trash."""
        files = [arg for arg in args if not arg.startswith("-")]

        for arg in files:
            if os.path.isabs(arg):
                abs_path = arg
            else:
                abs_path = os.path.abspath(os.path.join(cwd, arg))

            base = os.path.basename(abs_path) or "item"
            h_need = hashlib.sha256(abs_path.encode("utf-8")).hexdigest()[:6]

            best_name = None
            best_ts = -1

            for name in os.listdir(TRASH):
                parts = name.split("_", 2)
                if len(parts) != 3:
                    continue
                ts_str, h_str, base_name = parts
                if h_str != h_need or base_name != base:
                    continue
                try:
                    ts = int(ts_str)
                except ValueError:
                    continue
                if ts > best_ts:
                    best_ts = ts
                    best_name = name

            if best_name is None:
                raise FileNotFoundError(f"undo: Cannot restore '{arg}': not found in trash")

            source = os.path.join(TRASH, best_name)
            target_dir = os.path.dirname(abs_path)
            os.makedirs(target_dir, exist_ok=True)

            shutil.move(source, abs_path)

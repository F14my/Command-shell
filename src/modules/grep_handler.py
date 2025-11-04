import os
import re

from src.modules.logger import log_command


class GrepHandler:
    @log_command
    def execute(self, args: list[str], shell) -> None:
        keys = [arg for arg in args if arg.startswith("-")]
        args = [arg for arg in args if not arg.startswith("-")]
        if len(args) < 2:
            raise ValueError("grep: Too few arguments. Usage: grep <pattern> <path>")
        pattern, path = args[0], args[1::]
        self.handle_grep(keys, pattern, path)

    def get_all_files(self, path):
        files = []
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isfile(full_path):
                files.append(full_path)
        return files

    def get_all_files_recursive(self, path):
        files = []
        for curr_dir, dirs, filenames in os.walk(path):
            for filename in filenames:
                full_path = os.path.join(curr_dir, filename)
                files.append(full_path)
        return files

    def handle_grep(self, keys: list[str], pattern: str, path: list[str]) -> None:
        try:
            pattern = re.compile(pattern)
        except re.error:
            raise ValueError(f"grep: Invalid pattern: {pattern}")
        files = []
        for file in path:
            path = os.path.join(os.getcwd(), file)
            if os.path.isfile(path):
                files.append(path)
            else:
                if "-r" in keys:
                    files.extend(self.get_all_files_recursive(file))
                else:
                    files.extend(self.get_all_files(file))
        for file in files:
            if os.path.isfile(file):
                with open(file, "r", encoding="utf-8") as read:
                    for line_n, line in enumerate(read):
                        if pattern.search(line):
                            print(f"{file} : {line_n} : {line.strip()}")

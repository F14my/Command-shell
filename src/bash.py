import os
import shlex
import shutil
from os import listdir
from datetime import datetime

try:
    import pwd
    import grp

    UNIX = True
except ImportError:
    UNIX = False


class Bash:
    def __init__(self) -> None:
        self.current_directory = os.getcwd()
        self.complex_commands = {
            "ls": LsHandler(),
        }
        self.simple_commands = {
            "pwd": self.handle_pwd,
            "cd": self.handle_cd,
            "cat": self.handle_cat,
            "cp": self.handle_cp,
            "mv": self.handle_mv,
            "rm": self.handle_rm,
        }

    def execute(self, command_line: str) -> None | str:
        command, args = self.parse_command(command_line)
        if command in self.simple_commands:
            return self.simple_commands[command](args)
        elif command in self.complex_commands:
            return self.complex_commands[command].execute(args, self)
        else:
            return f"Command not found: {command}"

    def parse_command(self, command_line: str) -> tuple[str, list[str]]:
        parts = shlex.split(command_line)
        return parts[0], parts[1::]

    def handle_cd(self, args: list[str]) -> None:
        if not args:
            path = os.path.expanduser("~")
        else:
            path = "".join(args).replace("/", "\\")
            if path.startswith("~"):
                path = os.path.expanduser("~") + path[1::]
        try:
            os.chdir(path)
        except FileNotFoundError:
            raise FileNotFoundError(f"cd: cannot find '{path}': No such directory")

    def handle_pwd(self, args: list[str]) -> None:
        print(f"Current working directory: {os.getcwd().replace("\\", "/")}")

    def handle_cat(self, args: list[str]) -> None:
        path = "".join([arg for arg in args if not arg.startswith("-")])
        if os.path.isfile(path):
            with open(path, "r") as file:
                data = file.readlines()
                for line in data:
                    print(line)
                if not data:
                    print()
        else:
            raise ValueError(f"cat: Cannot open '{path}': Cannot open directory")

    def handle_cp(self, args: list[str]) -> None:
        keys = [arg for arg in args if arg.startswith("-")]
        files = [arg for arg in args if not arg.startswith("-")]
        if len(files) < 2:
            raise ValueError("cp: Missing file operand")
        source, target = files[0], files[1]
        try:
            if "-r" in keys or os.path.isdir(source):
                shutil.copytree(source, target)
            else:
                shutil.copy(source, target)
        except PermissionError:
            raise (f"cp: Permission denied: '{source}'")
        except FileNotFoundError:
            print(f"cp: Cannot stat '{source}': No such file or directory")
        except shutil.SameFileError:
            print(f"cp: '{source}' and '{target}' are the same file")

    def handle_mv(self, args: list[str]) -> None:
        if len(args) < 2:
            raise ValueError("mv: Missing file operand")
        source, target = args[0], args[1]
        try:
            shutil.move(source, target)
        except FileNotFoundError:
            print(f"mv: Cannot stat '{source}': No such file or directory")
        except PermissionError:
            print(f"mv: Cannot move '{source}': Permission denied")

    def handle_rm(self, args: list[str]) -> None:
        keys = [arg for arg in args if arg.startswith("-")]
        file = [arg for arg in args if not arg.startswith("-")][0]
        try:
            if "-r" in keys or os.path.isdir(file):
                response = input(f"rm: remove write-protected directory '{file}'? ")
                if response.lower() in ['y', 'yes']:
                    shutil.rmtree(file)
            else:
                os.remove(file)
        except PermissionError:
            raise (f"rm: Permission denied: '{file}'")
        except FileNotFoundError:
            print(f"rm: Cannot delete '{file}': No such file or directory")


class LsHandler:
    def execute(self, args: list, shell) -> None:
        keys = [arg for arg in args if arg.startswith("-")]
        args = [arg for arg in args if not arg.startswith("-")]
        self.handle_ls(keys, args, shell)

    def get_file_type(self, path: str) -> str:
        if os.path.isdir(path):
            return 'd'
        elif os.path.islink(path):
            return 'l'
        elif os.path.isfile(path):
            return '-'
        else:
            return '?'

    def get_permissions(self, code: str) -> str:
        perm_str = ""
        perm_list = ["---", "--x", "-w-", "-wx", "r--", "r-x", "rw-", "rwx"]
        for perm in code:
            perm_str += perm_list[int(perm)]
        return perm_str

    def get_owner_group(self, uid: int, gid: int) -> tuple[str, str]:
        if UNIX:
            try:
                owner = pwd.getpwuid(uid).pw_name
            except KeyError:
                owner = str(uid)
            try:
                group = grp.getgrgid(gid).gr_name
            except KeyError:
                group = str(gid)
        else:
            owner = os.getlogin()
            group = owner
        return owner, group

    def format_output(self, filepath: str) -> str:
        stat = os.stat(filepath)
        filename = os.path.basename(filepath)
        code = oct(stat.st_mode)[-3:]

        perms = self.get_file_type(filepath) + self.get_permissions(code)

        links = stat.st_nlink

        size = stat.st_size

        time = datetime.fromtimestamp(stat.st_mtime)
        formatted_time = time.strftime("%b %d %H:%M")

        owner, group = self.get_owner_group(stat.st_uid, stat.st_gid)

        return f"{perms} {links:>2} {owner:>8} {group:>8} {size:>8} {formatted_time} {filename}"

    def handle_ls(self, keys: list[str], args: list[str], shell) -> None:
        path = "".join(args).replace("/", "\\") if args else os.getcwd()
        try:
            lst_dir = listdir(path)
            if "-l" in keys:
                for file in sorted(lst_dir):
                    filepath = os.path.join(path, file)
                    print(self.format_output(filepath))
            else:
                print(" ".join(lst_dir))
        except FileNotFoundError:
            raise FileNotFoundError(f"ls: cannot access '{path}': No such file or directory")
        except PermissionError:
            raise FileNotFoundError(f"ls: cannot open directory '{path}': Permission denied")

import os
import platform
from datetime import datetime
from os import listdir
from src.modules.logger import log_command

UNIX = True if platform.system() == "Darwin" else False

if UNIX:
    import pwd
    import grp

class LsHandler:
    @log_command
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
                owner = pwd.getpwuid(uid).pw_name # type: ignore[attr-defined]
            except KeyError:
                owner = str(uid)
            try:
                group = grp.getgrgid(gid).gr_name # type: ignore[attr-defined]
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

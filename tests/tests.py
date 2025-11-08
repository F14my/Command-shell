import unittest
import os
import tempfile
from src.bash import Bash
import io
from contextlib import redirect_stdout


class TestBash(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        self.bash = Bash()
        self.test_dir = tempfile.mkdtemp()
        os.chdir(self.test_dir)

    def capture_output(self, command):
        """Capture print output from command execution."""
        f = io.StringIO()
        with redirect_stdout(f):
            self.bash.execute(command)
        return f.getvalue()

    def test_pwd_command(self):
        """Test pwd command returns current directory."""
        output = self.capture_output("pwd")
        self.assertIn(os.getcwd(), output)

    def test_ls_command(self):
        """Test ls command,"""
        with open("test1.txt", "w") as f:
            f.write("hello")
        with open("test2.txt", "w") as f:
            f.write("world")

        output = self.capture_output("ls")
        self.assertIn("test1.txt", output)
        self.assertIn("test2.txt", output)

    def test_cd_command(self):
        """Test command cd."""
        new_dir = os.path.join(self.test_dir, "subdir")
        os.makedirs(new_dir)

        self.bash.execute(f"cd {new_dir}")
        self.assertEqual(os.getcwd(), new_dir)

        self.bash.execute("cd ..")
        self.assertEqual(os.getcwd(), self.test_dir)

    def test_cat_command(self):
        """Test command cat."""
        test_content = "hello world"
        with open("test.txt", "w") as f:
            f.write(test_content)

        output = self.capture_output("cat test.txt")
        self.assertEqual(output, test_content + "\n")

    def test_mv_command(self):
        """Test command mv."""
        with open("old.txt", "w") as f:
            f.write("123")

        self.bash.execute("mv old.txt new.txt")
        self.assertFalse(os.path.exists("old.txt"))
        self.assertTrue(os.path.exists("new.txt"))

    def test_cp_command(self):
        """Test command cp."""
        with open("original.txt", "w") as f:
            f.write("123")

        self.bash.execute("cp original.txt copy.txt")
        self.assertTrue(os.path.exists("original.txt"))
        self.assertTrue(os.path.exists("copy.txt"))

        with open("copy.txt", "r") as f:
            content = f.read()
        self.assertEqual(content, "123")

    def test_rm_command(self):
        """Test command rm."""
        with open("to_delete.txt", "w") as f:
            f.write("123")

        self.bash.execute("rm to_delete.txt")
        self.assertFalse(os.path.exists("to_delete.txt"))

    def test_grep_command(self):
        """Test command grep."""
        with open("search.txt", "w") as f:
            f.write("MAI THE BEST")

        output = self.capture_output("grep MAI search.txt")
        self.assertIn(f"MAI THE BEST", output)
        self.assertNotIn(f"MAI NOT THE BEST", output)

    def test_unknown_command(self):
        """Test unknown command."""
        with self.assertRaises(ValueError):
            self.bash.execute("unknown_command")

    def test_command_with_quotes(self):
        """Test command with quotes."""
        with open("file with spaces.txt", "w") as f:
            f.write("123")

        output = self.capture_output('cat "file with spaces.txt"')
        self.assertEqual(output, "123\n")

    def test_history_command(self):
        """Test command history."""
        self.bash.execute("pwd")
        self.bash.execute("ls")

        output = self.capture_output("history 2")
        self.assertIn("pwd", output)
        self.assertIn("ls", output)

    def test_zip_command(self):
        """Test zip command creates archive."""
        os.makedirs("test_folder")
        with open("test_folder/file.txt", "w") as f:
            f.write("123")

        self.bash.execute("zip test_folder")

        self.assertTrue(os.path.exists("test_folder.zip"))

    def test_unzip_command(self):
        """Test unzip command extracts archive."""
        os.makedirs("extract_test")
        with open("extract_test/file.txt", "w") as f:
            f.write("123")
        self.bash.execute("zip extract_test")

        self.bash.execute("unzip extract_test.zip")

        self.assertTrue(os.path.exists("extract_test/file.txt"))

    def test_tar_command(self):
        """Test tar command creates tar archive."""
        os.makedirs("tar_folder")
        with open("tar_folder/file.txt", "w") as f:
            f.write("123")

        self.bash.execute("tar tar_folder")

        self.assertTrue(os.path.exists("tar_folder.tar"))

    def test_untar_command(self):
        """Test untar command extracts tar archive."""
        os.makedirs("untar_test")
        with open("untar_test/file.txt", "w") as f:
            f.write("123")
        self.bash.execute("tar untar_test")

        self.bash.execute("untar untar_test.tar")

        self.assertTrue(os.path.exists("untar_test/file.txt"))

    def test_zip_with_custom_name(self):
        """Test zip command with custom archive name."""
        os.makedirs("custom_zip")
        with open("custom_zip/file.txt", "w") as f:
            f.write("123")

        self.bash.execute("zip custom_zip my_archive")

        self.assertTrue(os.path.exists("my_archive.zip"))
        self.assertFalse(os.path.exists("custom_zip.zip"))


if __name__ == "__main__":
    unittest.main()
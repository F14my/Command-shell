from pathlib import Path

HISTORY_FILE = Path(__file__).parent.parent / "history.json"
TRASH = Path(__file__).parent.parent / ".trash"
UNDO_COMMANDS = ["cp", "rm", "mv", ""]
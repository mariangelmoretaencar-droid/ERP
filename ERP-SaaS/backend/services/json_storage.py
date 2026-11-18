
import json
import os
from pathlib import Path
from threading import RLock

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

_lock = RLock()


def read_data(filename):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    file_path = DATA_DIR / filename

    with _lock:
        if not file_path.exists():
            file_path.write_text("[]", encoding="utf-8")

        try:
            with file_path.open("r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            raise ValueError(f"El archivo {filename} contiene JSON inválido.")


def write_data(filename, data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    file_path = DATA_DIR / filename
    temp_path = file_path.with_suffix(".tmp")

    with _lock:
        with temp_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.flush()
            os.fsync(file.fileno())

        os.replace(temp_path, file_path)

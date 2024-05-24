from tinydb import TinyDB
from pathlib import Path
import tinydb_serialization as tise
from tinydb_serialization.serializers import DateTimeSerializer
from ..dirs import application_dir


def get_db(db_path: Path):
    db_serializer = tise.SerializationMiddleware()
    db_serializer.register_serializer(DateTimeSerializer(), "TinyDate")
    db = TinyDB(
        db_path,
        storage=db_serializer,
        encoding="utf-8",
        ensure_ascii=False,
        indent=2,
    )
    return db


# application-wide current DB
_current_db: None | TinyDB = None


def set_current_db(db: TinyDB):
    global _current_db
    if _current_db is not None:
        raise ValueError(f"Current DB is already set")
    _current_db = db


def unset_current_db():
    global _current_db
    _current_db = None


def get_current_db():
    if _current_db is None:
        raise ValueError(f"No DB set")
    return _current_db

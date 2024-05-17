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

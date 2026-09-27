# ============================================
# TYPE - Stockage JSON compatible anciennes versions MySQL/MariaDB
# ============================================
import json
from sqlalchemy import TypeDecorator, Text


class JSONText(TypeDecorator):
    """Stocke un dict/list Python en JSON dans une colonne TEXT.
    Évite de dépendre du type JSON natif, absent sur certaines
    installations MySQL/MariaDB plus anciennes."""
    impl = Text
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value, ensure_ascii=False)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return json.loads(value)
from sqlalchemy import func, select
from packages.sql.sql_controller import Database
from packages.models.savekill_table_model import SaveKill


def analyze_savekill(product) -> dict:
    fetch = Database().session.execute(select(SaveKill).where(SaveKill.name == product)).scalar()
    return fetch
    

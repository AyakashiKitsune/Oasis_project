from sqlalchemy import func, select
from packages.sql.sql_controller import Database
from packages.models.savekill_table_model import SaveKill
from packages.models.sales_table_model import Sales
from packages.models.Inventory_Analysis_model import Inventory_Analysis


def analyze_savekilling():
    fetch = Database().session.execute(select(SaveKill)).scalars()
    return [i.to_dict() for i in fetch] # type: ignore

def analyze_stocking():
    fetch = Database().session.execute(
        select(Inventory_Analysis)
    ).scalars()

    return [i.to_dict() for i in fetch]



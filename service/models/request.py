from datetime import datetime
from decimal import Decimal
from pony import orm
from .base import db

class Request(db.Entity):
    _table_ = "service_requests"

    created = orm.Optional(datetime, default=datetime.utcnow)
    txid = orm.Optional(str, nullable=True)
    amount = orm.Required(Decimal)
    address = orm.Required(str)
    agent = orm.Required(str)
    ip = orm.Required(str)

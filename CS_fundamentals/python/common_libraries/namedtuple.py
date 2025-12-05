from collections import namedtuple
Some = namedtuple("Person", ["name", "age"])
s = Some('alice', 30)
s # returns Person(name='alice', age=30)


from typing import NamedTuple
# the real reason to really use NamedTuple is so you can access tuples using name accessors
# can do "attribute acces" OR field access via attributes
from datetime import datetime
class Opportunity(NamedTuple):
    buy_dt: datetime
    sell_dt: datetime
    buy_price: float
    sell_price: float

opp = Opportunity("12/01", "12/05", 100.0, 110.0)
# it doesnt type check at runtime unless you use a type checker

print(opp.buy_dt)
print(opp.buy_price)
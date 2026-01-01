from syslinkPy import client
from syslinkPy import table
from syslinkPy import send_table

class hero(table):
    id: Opitionl[int] = field(defualt=None, primary_key=True)
    name: str

send_table([hero])

lists = [hero(name="aavart"),hero(name="sdfsdf")]
syslinkPy.insert(hero(),hero())  # how to make 





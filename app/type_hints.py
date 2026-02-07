from typing import Any

class City:
    def __init__(self, name: str,location):
        self.name = name
        self.location = location
text : str ="value"
pert : int = 90
temp : float =37.6
number:int | float =12
digits : list[int] = [1,2,3,4,5]
table_5 : tuple[int,...] = (1, 10, 15, 20, 15)

hampshirec=City("Hampshirec",200009)
city_temp : tuple[City ,float ] = (hampshirec, 20.5)
shipment : dict[str,Any] = {
    "id" : 17398,
    "weight" : 1.2,
    "content" : "wodden table",
    "status" : "in transit",

}


def root(num: int | float, exp: float | None = .5) -> float:
    return pow(num,.5)
root_25 =root(25.4)

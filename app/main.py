
from fastapi import FastAPI,HTTPException,status
from scalar_fastapi import get_scalar_api_reference
from typing import Any
from database import DataBase

from schemas import ShipmentRead, ShipmentCreate, ShipmentUpdate

app = FastAPI()
db = DataBase()

@app.get("/shipment",response_model=ShipmentRead)
def get_shipment(id :int):
    shipment = db.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="given id does not exist",
        )

    return shipment

@app.post("/shipment",response_model=None)
def submit_shipment(shipment:ShipmentCreate) -> dict[str, int]:
    new_id= db.create(shipment)
    return {"id":new_id}

# @app.get("/shipment/{id}")
# def get_shipment(id:int) -> dict[str, Any]:
#
#     if id not in shipments:
#         return {"detail" : "Given id doesn't exist"}
#
#     return shipments[id]


# @app.put("/shipment")
# def put_shipment(id :int,content :str ,weight :float,status: str) -> dict[str ,Any]:
#     shipments[id] = {
#         "content": content,
#         "weight": weight,
#         "status" : status,
#     }
#     return shipments[id]


@app.patch("/shipment",response_model=ShipmentRead)
def update_shipment(id:int,shipment: ShipmentUpdate) -> dict[str,Any]:
    shipment = db.update(id,shipment)
    return shipment

@app.delete("/shipment")
def delete_shipment(id :int) -> dict[str ,str]:
    db.delete(id)
    return {"detail": f"shipment #{id} was deleted"}




@app.get("/scalar",include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="scalar API",
    )
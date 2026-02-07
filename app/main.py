
from fastapi import FastAPI,HTTPException,status
from typing import Any
from database import shipments,save

from schemas import ShipmentRead, ShipmentCreate, ShipmentUpdate

app = FastAPI()


# shipments = {
#     12701:{
#         "weight": .6,
#         "content": "glasswar",
#         "status":"shipping"
#     },
#     12702: {
#                "weight": .10,
#                "content": "table",
#                "status": "placed"
#     },
#     12703: {
#         "weight": 20,
#         "content": "cloths",
#         "status": "placed"
#     },
#     12704: {
#                "weight": .11,
#                "content": "wood",
#                "status": "placed"
#     }
# }
@app.get("/shipment",response_model=ShipmentRead)
def get_shipment(id :int):
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="given id does not exist")

    return shipments[id]

@app.post("/shipment",response_model=None)
def submit_shipment(shipment:ShipmentCreate) -> dict[str, int]:
    new_id=max(shipments.keys()) +1

    shipments[new_id] = {
        **shipment.model_dump(),
        "id": new_id,
        "status": "shipping"
    }
    save()
    return {"id": new_id}

@app.get("/shipment/{id}")
def get_shipment(id:int) -> dict[str, Any]:

    if id not in shipments:
        return {"detail" : "Given id doesn't exist"}

    return shipments[id]


@app.put("/shipment")
def put_shipment(id :int,content :str ,weight :float,status: str) -> dict[str ,Any]:
    shipments[id] = {
        "content": content,
        "weight": weight,
        "status" : status,
    }
    return shipments[id]


@app.patch("/shipment",response_model=ShipmentRead)
def update_shipment(id:int,body : ShipmentUpdate) -> dict[str,Any]:

    shipments[id].update(body.model_dump(exclude_none=True))
    save()
    return shipments[id]

@app.delete("/shipment")
def delete_shipment(id :int) -> dict[str ,str]:
    shipments.pop(id)
    return {"detail": f"shipment #{id} was deleted"}




# @app.get("/scalar",include_in_schema=False)
# def get_scalar_docs():
#     return get_scalar_api_reference(
#         openapi_url=app.openapi_url,
#         title="scalar API",
#     )
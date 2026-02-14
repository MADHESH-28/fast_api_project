# import json
#
#
# shipments={}
# print("before load:",shipments)
#
# with open("shipments.json") as json_file:
#     data = json.load(json_file)
#
#     for value in data:
#         shipments[value["id"]] = value
#
# print("after load:",shipments)
#
# def save():
#     with open("shipments.json","w") as json_file:
#         json.dump(list(shipments.values()),json_file)
#
import sqlite3
from typing import Any

from schemas import ShipmentCreate, ShipmentUpdate


class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect("sqlite.db",check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS shipment (
            id INTEGER PRIMARY KEY,
            content TEXT,
            weight REAL,
            status TEXT
            )
        """,)

    def create(self,shipment:ShipmentCreate):
        self.cur.execute("SELECT MAX(id) FROM shipment ")
        result = self.cur.fetchone()

        new_id = result[0] + 1

        #insert values in the table
        self.cur.execute("""
            INSERT INTO shipment
            VALUES (:id, :content, :weight, :status)
        """,
            {
                "id": new_id,
                **shipment.model_dump(),
                "status":"placed"
            }
        )
        self.conn.commit()
        return new_id

    def get(self,id:int) -> dict[str, Any] | None:
        self.cur.execute("""
            SELECT * FROM shipment
            WHERE id =?
         """ ,(id,))
        row = self.cur.fetchone()
        return {
            "id":row[0],
            "content":row[1],
            "weight":row[2],
            "status":row[3],
        }if row else None

    def update(self,id:int,shipment:ShipmentUpdate):
        # 4. update a value
        self.cur.execute("""
            UPDATE shipment SET status = :status
            WHERE id = :id
        """,
 {
                "id":id,
                **shipment.model_dump()
            }
        )
        self.conn.commit()

        return self.get(id)


    def delete(self,id:int) :
        self.cur.execute("""
            DELETE FROM shipment
            WHERE id = ?
            """, (id,))
        self.conn.commit()


    def close(self):
        self.conn.close()


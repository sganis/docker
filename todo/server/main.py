from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient
from pydantic import BaseModel
import os
from bson import ObjectId
from typing import Optional

app = FastAPI()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
client = MongoClient(MONGO_URI)
db = client["todo_db"]
todos_collection = db["todos"]

# Todo model
class TodoItem(BaseModel):
    title: str
    completed: bool = False

class UpdateTodoItem(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None
    
@app.get("/api/todos")
def get_todos():
    todos = list(todos_collection.find({}, {"_id": 1, "title": 1, "completed": 1}))
    for todo in todos:
        todo["id"] = str(todo.pop("_id"))
    return todos

@app.post("/api/todos")
def create_todo(todo: TodoItem):
    result = todos_collection.insert_one(todo.dict())
    return {"id": str(result.inserted_id), **todo.dict()}


@app.put("/api/todos/{todo_id}")
def update_todo(todo_id: str, todo: UpdateTodoItem):
    update_data = {k: v for k, v in todo.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    print(f'updating item {todo_id} to completed: {update_data}')
    updated = todos_collection.find_one_and_update(
        {"_id": ObjectId(todo_id)},
        {"$set": update_data},
        return_document=True
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Todo not found")

    updated["id"] = str(updated.pop("_id"))
    return updated


@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: str):
    result = todos_collection.delete_one({"_id": ObjectId(todo_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted"}

# Serve static files (Svelte build output from client/dist)
app.mount("/", StaticFiles(directory="../client/dist", html=True), name="static")


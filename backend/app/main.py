from fastapi import FastAPI 
from pydantic import BaseModel
app = FastAPI()

class TaskRecived(BaseModel):
    description: str

@app.get("/")
def root():
    return {"message": "Hello, from DevTeam-AI!"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/task")
def create_task(task: TaskRecived):
    return {"message": "Task Recieved", "description": task.description}
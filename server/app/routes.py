from fastapi import APIRouter, Request
from app.controllers.metadata_controller import get_metadata_controller

router = APIRouter()

@router.get("/metadata")
def get_metadata():
    print("route")
    return get_metadata_controller()

@router.post("/stats")
async def receive_path(request: Request):
    print("stats")
    data = await request.json()
    print("Received path:", data)
    return {"message": "Path received", "path": data} 
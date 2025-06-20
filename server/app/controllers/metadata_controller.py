from app.services.metadata_service import get_metadata_service

def get_metadata_controller():
    print("controller")
    return get_metadata_service() 
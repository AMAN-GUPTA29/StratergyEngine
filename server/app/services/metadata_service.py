from app.utils.metadata_utils import scan_data_directory

def get_metadata_service():
    print("service")
    return scan_data_directory() 
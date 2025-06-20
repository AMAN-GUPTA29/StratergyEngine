from app.services.metadata_service import get_metadata_service, load_csv_service
import os
import pandas as pd

def get_metadata_controller():
    print("controller")
    return get_metadata_service()

def get_stats_controller(data):
    return load_csv_service(data) 
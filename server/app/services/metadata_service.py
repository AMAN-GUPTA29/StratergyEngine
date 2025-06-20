from app.utils.metadata_utils import scan_data_directory
import os
import pandas as pd

def get_metadata_service():
    print("service")
    return scan_data_directory()

def load_csv_service(data):
    person = data.get('person')
    country = data.get('country')
    strategy = data.get('strategy')
    docname = data.get('docname')
    if person and country and strategy:
        base_path = os.path.join('server', 'data', person, country, strategy)
    else:
        base_path = data.get('path')
    print("checkpath")
    print(base_path)
    if not base_path or not docname:
        return {'error': 'Missing path or docname'}
    csv_path = os.path.join(base_path, f"{docname}.csv")
    try:
        df = pd.read_csv(csv_path)
        return {'columns': df.columns.tolist(), 'shape': df.shape}
    except Exception as e:
        return {'error': str(e)} 
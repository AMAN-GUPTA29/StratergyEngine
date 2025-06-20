import os

def scan_data_directory(data_dir="data"):
    metadata = {}
    if not os.path.exists(data_dir):
        return metadata
    for person in os.listdir(data_dir):
        person_path = os.path.join(data_dir, person)
        if os.path.isdir(person_path):
            metadata[person] = {}
            for country in os.listdir(person_path):
                country_path = os.path.join(person_path, country)
                if os.path.isdir(country_path):
                    strategies = [s for s in os.listdir(country_path) if os.path.isdir(os.path.join(country_path, s))]
                    metadata[person][country] = strategies
    
    print(metadata)
    return metadata 
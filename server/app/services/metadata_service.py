from app.utils.metadata_utils import scan_data_directory
import os
import pandas as pd
import glob

def get_metadata_service():
    print("service")
    return scan_data_directory()

def load_csv_service(data):
    person = data.get('person')
    country = data.get('country')
    strategy = data.get('strategy')
    pnlfolder = "daily_pnl_files"
    docname = data.get('docname')
    if person and country and strategy:
        base_path = os.path.join('data', person, country, strategy)
    else:
        base_path = data.get('path')
    print("checkpath")
    pnlpath = os.path.join(base_path, pnlfolder)
    print(pnlpath)

    daywise_pnl = {}
    # Get all CSV files in the pnlpath 
    csv_files = glob.glob(os.path.join(pnlpath, '*.csv'))
    if not csv_files:
        print(f"No CSV files found in {pnlpath}")
        return {'daywise_pnl': {}}
    
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            # Clean column names (strip spaces)
            df.columns = [col.strip() for col in df.columns]
            # Clean up whitespace in DATE column if present
            if 'DATE' in df.columns:
                df['DATE'] = df['DATE'].astype(str).str.strip()
            # Ensure numeric columns
            for col in ['UNREAL_FTD', 'REAL_FTD']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            if not {'UNREAL_FTD', 'REAL_FTD', 'DATE'}.issubset(df.columns):
                continue
            # Sum UNREAL_FTD + REAL_FTD for each row
            df['PNL'] = df['UNREAL_FTD'] + df['REAL_FTD']
            # Group by DATE (should be one date per file, but robust)
            daily_pnl = df.groupby('DATE')['PNL'].sum()
            for date, pnl in daily_pnl.items():
                if date in daywise_pnl:
                    daywise_pnl[date] += pnl
                else:
                    daywise_pnl[date] = pnl
        except Exception as e:
            print(f"Error reading {csv_file}: {e}")
            continue
    # Return as a dictionary mapping date to pnl
    print(daywise_pnl)
    return {'daywise_pnl': daywise_pnl}
   
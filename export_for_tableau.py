import pandas as pd 
from sqlalchemy import create_engine
import os

DB_CONFIG = {
    'host':     os.environ.get('DB_HOST',      'localhost'),
    'database': os.environ.get('DB_NAME',      'cms_analytics'),
    'user':     os.environ.get('DB_USER',      'postgres'),
    'password': os.environ.get('DB_PASSWORD',  ''),
    'port':     os.environ.get('DB_PORT',      '5432')
}

def get_engine():
    url = (
        f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )

    return create_engine(url)

engine = get_engine()

hrrp_df = pd.read_sql("SELECT * FROM hrrp_clean", engine)

opioid_df = pd.read_sql("SELECT * FROM opioid_state", engine)

hrrp_df.to_csv("hrrp_clean_export.csv", index=False)

opioid_df.to_csv("opioid_state_export.csv", index=False)
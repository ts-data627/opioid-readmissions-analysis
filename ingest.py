import pandas as pd
from datetime import datetime
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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

def main():

    try:

        hrrp_data = pd.read_csv("FY_2026_Hospital_Readmissions_Reduction_Program_Hospital.csv")
        opioid_data = pd.read_csv("Medicare_Part_D_Opioid_Prescribing_Rates_by_Geography_2023.csv")

        logger.info(f"Load complete. {len(hrrp_data)} saved to DataFrames.")
        logger.info(f"Load complete. {len(opioid_data)} saved to DataFrames.")

    except FileNotFoundError:
        logger.error(f"File not found.")
        raise FileNotFoundError("Failed to find file.")

    try:
        with open('sql/create_tables.sql', 'r') as f:
            sql = f.read()

        engine = get_engine()

        with engine.connect() as conn:
            result = conn.execute(text(sql))
            conn.commit()
            logger.info("Tables created successfully.")

            hrrp_data = hrrp_data.rename(columns={
                                                  "Facility Name": "facility_name",
                                                  "Facility ID": "facility_id",
                                                  "State": "state",
                                                  "Measure Name": "measure_name",
                                                  "Number of Discharges": "number_discharges",
                                                  "Footnote": "footnote",
                                                  "Excess Readmission Ratio": "excess_read_ratio",
                                                  "Predicted Readmission Rate": "predicted_read_rate",
                                                  "Expected Readmission Rate": "expected_read_rate",
                                                  "Number of Readmissions": "num_readmissions",
                                                  "Start Date": "start_date",
                                                  "End Date": "end_date"
            })
            
            opioid_data = opioid_data.rename(columns={
                                                      "Year": "year",
                                                      "Prscrbr_Geo_Lvl": "prscrbr_geo_lvl",
                                                      "Prscrbr_Geo_Cd": "prscrbr_geo_cd",
                                                      "Prscrbr_Geo_Desc": "prscrbr_geo_desc",
                                                      "RUCA_Cd": "ruca_cd",
                                                      "Breakout_Type": "breakout_type",
                                                      "Breakout": "breakout",
                                                      "Tot_Prscrbrs": "tot_prscrbrs",
                                                      "Tot_Opioid_Prscrbrs": "tot_opioid_prscrbrs",
                                                      "Tot_Opioid_Clms": "tot_opioid_clms",
                                                      "Tot_Clms": "tot_clms",
                                                      "Opioid_Prscrbng_Rate": "opioid_prscrbng_rate",
                                                      "Opioid_Prscrbng_Rate_5Y_Chg": "opioid_prscrbng_rate_5y_chg",
                                                      "Opioid_Prscrbng_Rate_1Y_Chg": "opioid_prscrbng_rate_1y_chg",
                                                      "LA_Tot_Opioid_Clms": "la_tot_opioid_clms",
                                                      "LA_Opioid_Prscrbng_Rate": "la_opioid_prscrbng_rate",
                                                      "LA_Opioid_Prscrbng_Rate_5Y_Chg": "la_opioid_prscrbng_rate_5y_chg",
                                                      "LA_Opioid_Prscrbng_Rate_1Y_Chg": "la_opioid_prscrbng_rate_1y_chg"

            })

            hrrp_data.to_sql('hrrp_staging', conn, if_exists='append', index=False)
            logger.info(f"Loaded {len(hrrp_data)} rows into 'HRRP' table.")
            opioid_data.to_sql('opioid_staging', conn, if_exists='append', index=False)
            logger.info(f"Loaded {len(opioid_data)} rows into 'Opioid' table.")
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise

if __name__ == "__main__":
    main()
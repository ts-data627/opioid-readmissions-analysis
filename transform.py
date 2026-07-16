import pandas as pd
import logging
from datetime import datetime
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

states = {'Alabama': 'AL',
          'Alaska': 'AK',
          'Arizona': 'AZ',
          'Arkansas': 'AR',
          'California': 'CA',
          'Colorado': 'CO',
          'Connecticut': 'CT',
          'Delaware': 'DE',
          'District of Columbia': 'DC',
          'Florida': 'FL',
          'Georgia': 'GA',
          'Hawaii': 'HI',
          'Idaho': 'ID',
          'Illinois': 'IL',
          'Indiana': 'IN',
          'Iowa': 'IA',
          'Kansas': 'KS',
          'Kentucky': 'KY',
          'Louisiana': 'LA',
          'Maine': 'ME',
          'Maryland': 'MD',
          'Massachusetts': 'MA',
          'Michigan': 'MI',
          'Minnesota': 'MN',
          'Mississippi': 'MS',
          'Missouri': 'MO',
          'Montana': 'MT',
          'Nebraska': 'NE',
          'Nevada': 'NV',
          'New Hampshire': 'NH',
          'New Jersey': 'NJ',
          'New Mexico': 'NM',
          'New York': 'NY',
          'North Carolina': 'NC',
          'North Dakota': 'ND',
          'Ohio': 'OH',
          'Oklahoma': 'OK',
          'Oregon': 'OR',
          'Pennsylvania': 'PA',
          'Rhode Island': 'RI',
          'South Carolina': 'SC',
          'South Dakota': 'SD',
          'Tennessee': 'TN',
          'Texas': 'TX',
          'Utah': 'UT',
          'Vermont': 'VT',
          'Virginia': 'VA',
          'Washington': 'WA',
          'West Virginia': 'WV',
          'Wisconsin': 'WI',
          'Wyoming': 'WY',
          'Guam': 'GU',
          'Puerto Rico': 'PR',
          'Virgin Islands': 'VI',
          'Northern Mariana Islands': 'MP',
          'American Samoa': 'AS'}

def get_engine():
    url = (
        f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )

    return create_engine(url)

engine = get_engine()

def transform_data(hrrp_df: pd.DataFrame, opioid_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    hrrp_df['num_readmissions'] = hrrp_df['num_readmissions'].replace("Too Few to Report", None).astype('float').astype('Int64')
    hrrp_df['number_discharges'] = hrrp_df['number_discharges'].astype('float').astype('Int64')
    hrrp_df['footnote'] = hrrp_df['footnote'].astype('float').astype('Int64').astype('string')
    hrrp_df['predicted_read_rate'] = hrrp_df['predicted_read_rate'].astype('float')
    print(hrrp_df['footnote'].unique())

    opioid_df['year'] = opioid_df['year'].astype('float').astype('Int64')
    opioid_df['prscrbr_geo_cd'] = opioid_df['prscrbr_geo_cd'].astype('float').astype('Int64')
    opioid_df['tot_prscrbrs'] = opioid_df['tot_prscrbrs'].astype('float').astype('Int64')
    opioid_df['tot_opioid_prscrbrs'] = opioid_df['tot_opioid_prscrbrs'].astype('float').astype('Int64')
    opioid_df['tot_opioid_clms'] = opioid_df['tot_opioid_clms'].astype('float').astype('Int64')
    opioid_df['tot_clms'] = opioid_df['tot_clms'].astype('float').astype('Int64')
    opioid_df['ruca_cd'] = opioid_df['ruca_cd'].astype('float')
    opioid_df['opioid_prscrbng_rate'] = opioid_df['opioid_prscrbng_rate'].astype('float')
    opioid_df['opioid_prscrbng_rate_5y_chg'] = opioid_df['opioid_prscrbng_rate_5y_chg'].astype('float')
    opioid_df['opioid_prscrbng_rate_1y_chg'] = opioid_df['opioid_prscrbng_rate_1y_chg'].astype('float')
    opioid_df['la_opioid_prscrbng_rate'] = opioid_df['la_opioid_prscrbng_rate'].astype('float')
    opioid_df['la_opioid_prscrbng_rate_5y_chg'] = opioid_df['la_opioid_prscrbng_rate_5y_chg'].astype('float')
    opioid_df['la_opioid_prscrbng_rate_1y_chg'] = opioid_df['la_opioid_prscrbng_rate_1y_chg'].astype('float')
    opioid_df['la_tot_opioid_clms'] = opioid_df['la_tot_opioid_clms'].astype('float')

    bins = [0, 10, 15, 20, float("inf")]
    rate_names = ["Low", "Moderate", "High", "Very High"]

    hrrp_df['read_rate_buckets'] = pd.cut(hrrp_df['predicted_read_rate'], bins=bins, labels=rate_names)
    
    opioid_state = opioid_df[(opioid_df['prscrbr_geo_lvl'] == 'State') & (opioid_df['breakout'] == 'Overall')]

    opioid_state['state_abbrev'] = opioid_state['prscrbr_geo_desc'].map(states)

    return hrrp_df, opioid_df, opioid_state

def main():
    try:
        hrrp_df = pd.read_sql("SELECT * FROM hrrp_staging", engine)
        opioid_df = pd.read_sql("SELECT * FROM opioid_staging", engine)

    except Exception as e:
        logger.error(f"Error loading data into dataframe: {e}")
        raise

    hrrp_df, opioid_df, opioid_state = transform_data(hrrp_df, opioid_df)
    logger.info(f"Data transformation complete.")

    try:
        with open('sql/create_final_tables.sql', 'r') as f:
            sql = f.read()

        with engine.connect() as conn:
            result = conn.execute(text(sql))
            conn.commit()
            logger.info("Tables created successfully.")

            hrrp_df.to_sql('hrrp_clean', conn, if_exists='append', index=False)
            logger.info(f"Loaded {len(hrrp_df)} rows into 'HRRP' table.")
            opioid_df.to_sql('opioid_clean', conn, if_exists='append', index=False)
            logger.info(f"Loaded {len(opioid_df)} rows into 'Opioid' table.")
            opioid_state.to_sql('opioid_state', conn, if_exists='append', index=False)
            logger.info(f"Loaded {len(opioid_state)} rows into 'Opioid_State' table.")

    except SQLAlchemyError as e:
        logger.error(f"Error creating tables: {e}")
        raise

if __name__ == "__main__":
    main()


import pandas as pd
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

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

    engine = get_engine()

    try:   
        data = pd.read_sql("SELECT os.state_abbrev, os.opioid_prscrbng_rate, AVG(hc.predicted_read_rate) AS avg_pred_read_rate FROM opioid_state os INNER JOIN hrrp_clean hc ON os.state_abbrev = hc.state GROUP BY os.state_abbrev, os.opioid_prscrbng_rate ORDER BY os.opioid_prscrbng_rate DESC;", engine)
    except SQLAlchemyError as e:
        logger.error(f"Error executing query: {e}")
        raise


    X = data[['opioid_prscrbng_rate']]
    y = data['avg_pred_read_rate']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)

    model = LinearRegression()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    mse = mean_squared_error(y_test, preds)
    logger.info(f"MSE: {mse}")
    mae = mean_absolute_error(y_test, preds)
    logger.info(f"MAE: {mae}")
    r2 = r2_score(y_test, preds)
    logger.info(f"R2: {r2}")

if __name__ == "__main__":
    main()
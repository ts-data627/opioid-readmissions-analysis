CREATE TABLE IF NOT EXISTS hrrp_staging (
    id SERIAL PRIMARY KEY,
    facility_name TEXT,
    facility_id TEXT,
    state TEXT,
    measure_name TEXT,
    number_discharges TEXT,
    footnote TEXT,
    excess_read_ratio TEXT,
    predicted_read_rate TEXT,
    expected_read_rate TEXT,
    num_readmissions TEXT,
    start_date TEXT,
    end_date TEXT
);

CREATE TABLE IF NOT EXISTS opioid_staging (
    id SERIAL PRIMARY KEY,
    year TEXT,
    prscrbr_geo_lvl TEXT,  
    prscrbr_geo_cd TEXT,
    prscrbr_geo_desc TEXT,
    ruca_cd TEXT,
    breakout_type TEXT,
    breakout TEXT,
    tot_prscrbrs TEXT,
    tot_opioid_prscrbrs TEXT,
    tot_opioid_clms TEXT,
    tot_clms TEXT,
    opioid_prscrbng_rate TEXT,
    opioid_prscrbng_rate_5y_chg TEXT,
    opioid_prscrbng_rate_1y_chg TEXT,
    la_tot_opioid_clms TEXT,
    la_opioid_prscrbng_rate TEXT,
    la_opioid_prscrbng_rate_5y_chg TEXT,
    la_opioid_prscrbng_rate_1y_chg TEXT
)
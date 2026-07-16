SELECT os.state_abbrev, os.la_opioid_prscrbng_rate, AVG(hc.predicted_read_rate) AS avg_pred_read_rate
FROM opioid_state os
INNER JOIN hrrp_clean hc 
ON os.state_abbrev = hc.state
GROUP BY os.state_abbrev, os.la_opioid_prscrbng_rate
ORDER BY os.la_opioid_prscrbng_rate DESC
LIMIT 10;
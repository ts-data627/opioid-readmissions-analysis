SELECT state_abbrev, opioid_prscrbng_rate
FROM opioid_state
ORDER BY opioid_prscrbng_rate DESC
LIMIT 10;
SELECT id, facility_id, facility_name, state, excess_read_ratio
FROM hrrp_clean
WHERE excess_read_ratio > 1
ORDER BY excess_read_ratio DESC;
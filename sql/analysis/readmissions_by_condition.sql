SELECT measure_name, SUM(num_readmissions) as readmissions 
FROM hrrp_clean
GROUP BY measure_name
ORDER by readmissions DESC;
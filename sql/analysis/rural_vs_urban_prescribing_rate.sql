SELECT breakout, AVG(opioid_prscrbng_rate) AS avg_rate
FROM opioid_clean
WHERE breakout = 'Urban'
	OR breakout = 'Rural'
GROUP BY breakout
ORDER BY avg_rate DESC;
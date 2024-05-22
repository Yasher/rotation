SELECT
	c.person_id,
	--c.shift_id,
	r.rate, 
	p.employment_date 
FROM
	"current" c
JOIN rates r ON c.person_id = r.person_id AND c.shift_id = r.shift_id
JOIN person p ON c.person_id = p.id 
WHERE
	c.priority = 0
AND c.shift_id  = 5

ORDER BY rate DESC, employment_date
--LIMIT 2

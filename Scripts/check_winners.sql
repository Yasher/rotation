SELECT
	c.person_id,
	p.fio,
	--c.shift_id,
	r.rate, 
	p.employment_date,
	s.fullname 
FROM
	"current" c
JOIN rates r ON c.person_id = r.person_id AND c.shift_id = r.shift_id
JOIN person p ON c.person_id = p.id
JOIN shifts s ON c.shift_id = s.id 
WHERE
	c.priority = 0
AND c.shift_id  = 1
ORDER BY r.rate DESC, p.employment_date
--LIMIT 2

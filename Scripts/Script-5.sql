select * FROM person p 


update
	person
SET
	entered_data = 0

	
SELECT
	fio,
	tg_id
FROM
	person p
WHERE
	entered_data = 1


	
SELECT
	p.fio,
	s.fullname
FROM
	vote v
JOIN person p ON
	v.person_id = p.id
JOIN shifts s ON
	v.shift_id = s.id
ORDER BY
	s.id
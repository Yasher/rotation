SELECT
	h.id,
	h.period,
	p.fio,
	s.fullname
FROM
	history h
JOIN person p ON
	h.person_id = p.id
JOIN shifts s ON
	h.shift_id = s.id
WHERE
	h.period >= "2025-04-01 00:00:00" AND h.period <= "2025-05-31 00:00:00"
	
	
	
	
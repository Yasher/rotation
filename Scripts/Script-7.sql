SELECT p.fio, c.priority, s.fullname FROM "current" c join person p on c.person_id =p.id join shifts s on c.shift_id = s.id WHERE p.id = 5







SELECT
	s.fullname
FROM
	shifts s
WHERE
	s.id = 1

	
	
	SELECT s.fullname,c.priority FROM "current" c join shifts s on c.shift_id=s.id Where person_id = 8
	
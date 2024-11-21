SELECT
	c.shift_id
FROM
	"current" c
JOIN person p ON
	c.person_id = p.id
WHERE
	p.id = 2
ORDER BY
	c.priority
	
	
	SELECT s.id, s.fullname, p.tg_id	
--	, p2.*
    from shifts s
    JOIN
    person
    p
    ON
    1 = 1
    LEFT JOIN prohibited p2 
    ON
    p.id = p2.person_id AND
    s.id = p2.shift_id 
    WHERE
    s.enabled = 1
    AND
    p.enabled = 1
    AND 
    p2.person_id IS NULL
    ORDER BY s.id
    
    
    
    
    SELECT s.id, s.fullname, p.tg_id 
    from shifts s
    JOIN
    person
    p
    ON
    1 = 1
     LEFT JOIN prohibited p2 
    ON
    p.id = p2.person_id AND
    s.id = p2.shift_id 
    WHERE
    s.enabled = 1
    AND
    p.enabled = 1
    AND
    p.tg_id = 7050450693 
    AND 
    p2.person_id IS NULL
    ORDER BY s.id
    
    
    
    SELECT s.id, s.fullname, p.tg_id
     from shifts s
     JOIN
     person
     p
     ON
     1 = 1
     WHERE
     s.enabled = 1
     AND
     p.enabled = 1
     ORDER BY s.id
    
    
     
     
     
     
     
     
    SELECT
	p2.tg_id,
	p.shift_id
FROM
	prohibited p
JOIN person p2 ON
	p.person_id = p2.id 
    
    
	SELECT s.id, s.fullname, p.tg_id 
    from shifts s
    JOIN
    person
    p
    ON
    1 = 1
     LEFT JOIN prohibited p2 
    ON
    p.id = p2.person_id AND
    s.id = p2.shift_id 
    WHERE
    s.enabled = 1
    AND
    p.enabled = 1
    AND
    p.tg_id = 181564144 
    AND 
    p2.person_id IS NULL
    ORDER BY s.id
	
    SELECT
	c.*, p2.*
FROM
	"current" c
JOIN person p ON
	c.person_id = p.id
LEFT JOIN prohibited p2 
ON p.id = p2.person_id AND 
c.shift_id = p2.shift_id 
WHERE
	p.id = 9
ORDER BY
	c.priority

	
	SELECT
	s.id
FROM
	shifts s
JOIN person p 
ON 1=1
LEFT JOIN prohibited p2 
ON s.id = p2.shift_id AND p.id =p2.person_id 
WHERE
	s.enabled = 1 AND
	p.id = 1
ORDER BY p2.person_id 
	



SELECT
	s.id
FROM
	shifts s
JOIN person p 
ON 1=1
LEFT JOIN prohibited p2 
ON s.id = p2.shift_id AND p.id =p2.person_id 
WHERE
	s.enabled = 1 AND
	p.id = 1
ORDER BY p2.person_id


SELECT * FROM "current" c WHERE shift_id = 1 AND priority = 2



    
import datetime
import sqlite3

db = sqlite3.connect('rotation.db')
c = db.cursor()


def get_shifts (tg_id=0):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    if tg_id != 0:
        #print(tg_id)
        query = """SELECT s.id, s.fullname, p.tg_id 
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
    AND
    p.tg_id = ?
    ORDER BY s.id"""
        c.execute(query, (str(tg_id), ))
    else:

        query = """SELECT s.id, s.fullname, p.tg_id 
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
    ORDER BY s.id"""

    # query = "SELECT id, fullname  FROM shifts s WHERE enabled = 1"
        c.execute(query)
    shifts = c.fetchall()
    print(shifts)
    return shifts
    db.commit()
    db.close()


#get_shifts('181564144')



def get_person_id_from_tg_id(tg_id):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    query = "SELECT id FROM person p WHERE tg_id = ?"
    print (query)
    c.execute(query, (str(tg_id), ))
    id = c.fetchall()
    if len(id) > 0:
        return id[0][0]
    else:
        return 0

    db.commit()
    db.close()

#print(get_person_id_from_tg_id("7050450693"))

def insert_choice(choice, tg_id):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    person_id = get_person_id_from_tg_id(tg_id)
    print(person_id)
    count = 0
    for i in choice:
        if i[1] == str(tg_id):
            query = """INSERT
                        INTO
                        CURRENT (person_id,
                        shift_id,
                        priority, datetime)
                    VALUES (?, ?, ?, datetime('now'))"""
        # query = f'"""INSERT INTO current (person_id, shift_id, priority) VALUES ('
        # {str(person_id)}
        # ', "+str(i)+", "+str(choice.index(i))+")"""

        # print(query)
            c.execute(query, (str(person_id), str(i[0]), count))
            count += 1
    db.commit()
    db.close()

def get_chosen_shift(tg_id):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    query="""SELECT
	c.priority,
	s.fullname,
	p.tg_id
FROM
	"current" c
JOIN shifts s ON
	c.shift_id = s.id
JOIN person p ON
	c.person_id = p.id
WHERE
	p.tg_id = ?
ORDER BY
	p.tg_id,
	c.priority"""

    c.execute(query, (str(tg_id), ))
    shifts = c.fetchall()
    return shifts
    db.commit()
    db.close()

def delete_user_from_current(tg_id):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    query = """DELETE
FROM
	"current"
WHERE
	"current".person_id = ?"""
    id = get_person_id_from_tg_id(tg_id)

    c.execute(query, (str(id),))
    db.commit()
    db.close()


def check_shifts_persons_count():
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    shifts = 0
    persons = 0

    query = """SELECT
	SUM(s.quant)
FROM
	shifts s
WHERE
	s.enabled = 1"""

    c.execute(query)
    shifts = c.fetchone()[0]
    print(shifts)

    query = """SELECT
	sum(p.enabled)
FROM
	person p
WHERE
	enabled = 1"""

    c.execute(query)
    persons = c.fetchone()[0]
    print(persons)

    if shifts != persons:
        return False
    else:
        return True
    db.commit()
    db.close()

def random_insert_current():
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    import random
    a=random.sample(range(5), 5)
    print (a)

    query = """INSERT INTO current (person_id, shift_id, priority, datetime) VALUES (?, ?, ?, datetime('now'))
    """
    p=1

    while p<9:
        n = 1
        a = random.sample(range(5), 5)
        for i in a:
            print(p, n, i)
            c.execute(query, (p, n, i))
            n += 1
        p += 1

    db.commit()
    db.close()

#random_insert_current()

def get_voting_table(priority):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    query = """SELECT
	person_id ,
	shift_id ,
	priority
FROM
	"current" c
WHERE
	priority = ?
    """
    c.execute(query, (priority, ))
    return c.fetchall()

    db.commit()
    db.close()


#print(get_voting_table(0))

def get_person_count():
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    query = """SELECT
    	sum(p.enabled)
    FROM
    	person p
    WHERE
    	enabled = 1"""

    c.execute(query)
    return c.fetchone()[0]

    db.commit()
    db.close()

#рассчитать коэффициент сотрудника по определенной смене

#### rotation_period=202406 предусмотреть изменение
def get_shift_rates (shift):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    query = """SELECT rotation_period FROM settings"""
    c.execute(query)
    rotation_period = datetime.datetime.strptime(c.fetchone()[0], "%Y-%m-%d %H:%M:%S")
    print(rotation_period)

    p_count = get_person_count()
    rates = []
    for i in range(p_count):
        query = """SELECT
	period 
from
	history h
WHERE
	shift_id = ?
AND person_id = ?
ORDER BY
	period DESC
LIMIT 1
"""
        c.execute(query, (shift, i+1))
        last_period = c.fetchone()
        if last_period != None:
            last_period_date = datetime.datetime.strptime(last_period[0], "%Y-%m-%d %H:%M:%S")
            leftdays = (rotation_period - last_period_date).days
        else:
            last_period_date = None
            leftdays = 100000
        rates.append([i+1, leftdays])
    return rates
    db.commit()
    db.close()
#
a = get_shift_rates(3)
print(a)
# now = datetime.datetime.now()
# print(now)
#
# print(a[0][1][0])
# date = datetime.datetime.strptime(a[0][1][0], "%Y-%m-%d %H:%M:%S")
# print(date)
# notinshift = (now - date).days
# print(notinshift)

### записать всем ratio = (rotation_period - last_period) в месяцах, а тому у кого None ratio = 1000

#delete_user_from_current('181564144')
# choice = [[2, '181564144'], [4, '181564144'], [5, '181564144'], [2, '663014633'], [1, '181564144']]
# insert_choice(choice,"181564144")
def get_shifts_all():
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    query = """SELECT s.id FROM shifts s"""

    c.execute(query)
    shifts_all = c.fetchall()
    return  shifts_all
    db.commit()
    db.close()

#Запись коэффициентов на основе исторических данных - коэф-т для каждого сотрудника по каждой смене.
#Проводить перед запуском. При инициализации админом и выборе периода ротации
def insert_shift_rates ():
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    shifts = get_shifts_all()
    for sh in shifts:
        rates = get_shift_rates(sh[0])
        for rate in rates:
            query = """INSERT INTO rates (person_id, shift_id, rate) VALUES (?, ?, ?)"""
            c.execute(query, (rate[0], sh[0], rate[1]))

    db.commit()
    db.close()

insert_shift_rates()


def insert_choice_test(choice, tg_id):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    person_id = get_person_id_from_tg_id(tg_id)
    print(person_id)
    count = 0
    for i in choice:
        if i[2] == str(tg_id):
            query = """INSERT
                        INTO
                        CURRENT (person_id,
                        shift_id,
                        priority, datetime)
                    VALUES (?, ?, ?, "sdf")"""
        # query = f'"""INSERT INTO current (person_id, shift_id, priority) VALUES ('
        # {str(person_id)}
        # ', "+str(i)+", "+str(choice.index(i))+")"""

        # print(query)
            c.execute(query, (str(person_id), str(i[0]), count))
            count += 1
    db.commit()
    db.close()
#
# curr = [(1, '08:30 - 20:30', '7050450693'), (2, '20:30 - 08:30', '7050450693'), (3, '14:00 - 02:00', '7050450693'), (4, '15:30 - 00:00', '7050450693'), (5, '17:00 - 01:30', '7050450693')]
#
# insert_choice_test(curr, '7050450693')



#1)учесть запреты на смены.
# 2) сделать признак админа в persons и выдавать ему отдельное меню
# 3) переделать на f строки






# q="INSERT INTO current (id, person_id, shift_id, prioritry) VALUES ('1', '2', '4', '0')"
# c.execute(q)
# c.execute("INSERT INTO current VALUES (6, 1, 1, 1)")
# c.execute("INSERT INTO current VALUES (7, 1, 1, 1)")
#


# choice = [4,2,1,5,3]
# id_tg = "392408856"
# insert_choice(choice, id_tg)



#c.execute("INSERT INTO current (person_id, shift_id, priority) VALUES (2, 4, 0)")




db.commit()
db.close()




### функц очистка таблицы current



#a = get_shifts()
#print (a[0])


#for i in a:
 #   print (i)

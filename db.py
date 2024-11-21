import datetime
import sqlite3
import calendar

db = sqlite3.connect('rotation.db')
c = db.cursor()


def get_shifts (tg_id=0):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    if tg_id != 0:
    #     query = """SELECT s.id, s.fullname, p.tg_id
    # from shifts s
    # JOIN
    # person
    # p
    # ON
    # 1 = 1
    # WHERE
    # s.enabled = 1
    # AND
    # p.enabled = 1
    # AND
    # p.tg_id = ?
    # ORDER BY s.id"""

        query = """SELECT s.id, s.fullname, p.tg_id 
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
    p.tg_id = ? 
    AND 
    p2.person_id IS NULL
    ORDER BY s.id"""



        c.execute(query, (str(tg_id), ))
    else:

    #     query = """SELECT s.id, s.fullname, p.tg_id
    # from shifts s
    # JOIN
    # person
    # p
    # ON
    # 1 = 1
    # WHERE
    # s.enabled = 1
    # AND
    # p.enabled = 1
    # ORDER BY s.id"""

        query = """SELECT s.id, s.fullname, p.tg_id
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
    ORDER BY s.id"""

    # query = "SELECT id, fullname  FROM shifts s WHERE enabled = 1"
        c.execute(query)
    shifts = c.fetchall()
    return shifts
    db.commit()
    db.close()


#get_shifts('181564144')



def get_person_id_from_tg_id(tg_id):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    query = "SELECT id FROM person p WHERE tg_id = ?"
    c.execute(query, (str(tg_id), ))
    id = c.fetchall()
    if len(id) > 0:
        return id[0][0]
    else:
        return 0

    db.commit()
    db.close()

def insert_choice(choice, tg_id):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    person_id = get_person_id_from_tg_id(tg_id)
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
	p.tg_id,
	s.id
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
    query = """SELECT
	sum(p.enabled)
FROM
	person p
WHERE
	enabled = 1"""

    c.execute(query)
    persons = c.fetchone()[0]
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
    query = """INSERT INTO current (person_id, shift_id, priority, datetime) VALUES (?, ?, ?, datetime('now'))
    """
    p=1

    while p<9:
        n = 1
        a = random.sample(range(5), 5)
        for i in a:
            c.execute(query, (p, n, i))
            n += 1
        p += 1

    db.commit()
    db.close()



#random_insert_current()

def get_voting_table():
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    query = """SELECT
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
    """
    c.execute(query)
    return c.fetchall()

    db.commit()
    db.close()

def get_history(id = 0):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    period1 = get_current_period("curr_period_base")
    period2 = get_current_period("curr_period+1_base")

    query = """SELECT
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
"""
    if id == 0:
       	query += "h.period >= \"" + period1 + "\" AND h.period <= \"" + period2 + "\""
    else:
        query += "h.id = " + str(id)
    c.execute(query)
    return c.fetchall()

    db.commit()
    db.close()

def del_str_history(history_id):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    q = """DELETE
FROM
	history
WHERE
	id = """ + history_id
    c.execute(q)
    db.commit()
    db.close()

#d = get_history("2024-10-01 00:00:00", "2024-11-01 00:00:00")
def get_person_count(entered):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    query = """SELECT
    	sum(p.enabled)
    FROM
    	person p
    WHERE
    	enabled = 1 """
    if entered == True:
        query += "AND entered_data = 1"

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
    p_count = get_person_count(False)
    persons = get_persons_id()
    rates = []
    #for i in range(p_count):
    for i in persons.keys():
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
#Здесь можно будет поставить ограничение по давности проверки

        c.execute(query, (shift, i))
        last_period = c.fetchone()
        if last_period != None:
            last_period_date = datetime.datetime.strptime(last_period[0], "%Y-%m-%d %H:%M:%S")
            leftdays = (rotation_period - last_period_date).days
        else:
            last_period_date = None
            leftdays = 100000
        rates.append([i, leftdays])
    return rates
    db.commit()
    db.close()


### записать всем ratio = (rotation_period - last_period) в месяцах, а тому у кого None ratio = 1000

#delete_user_from_current('181564144')
# choice = [[2, '181564144'], [4, '181564144'], [5, '181564144'], [2, '663014633'], [1, '181564144']]
# insert_choice(choice,"181564144")
def get_shifts_all(count, with_disabled, addcurrent = 0, pers_id = 0):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    if addcurrent != 0:
        query = """SELECT
	s.id
FROM
	shifts s
JOIN person p 
ON 1=1
LEFT JOIN prohibited p2 
ON s.id = p2.shift_id AND p.id =p2.person_id 
WHERE
	s.enabled = 1 AND
	p.id = ?
ORDER BY p2.person_id """
        c.execute(query, (str (pers_id),))
    else:
        if count == False:
            query = """SELECT s.id FROM shifts s"""
        else:
            query = """SELECT s.id, s.quant FROM shifts s"""

        if with_disabled == False:
            query += " WHERE enabled = 1"

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

    shifts = get_shifts_all(False, True)
    for sh in shifts:
        rates = get_shift_rates(sh[0])
        for rate in rates:
            query = """INSERT INTO rates (person_id, shift_id, rate) VALUES (?, ?, ?)"""
            c.execute(query, (rate[0], sh[0], rate[1]))

    db.commit()
    db.close()



#insert_shift_rates()


def delete_shift_rates():
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    query = """DELETE FROM rates"""
    c.execute(query)

    db.commit()
    db.close()

#delete_shift_rates()





def insert_choice_test(choice, tg_id):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    person_id = get_person_id_from_tg_id(tg_id)
    count = 0
    for i in choice:
        if i[2] == str(tg_id):
            query = """INSERT
                        INTO
                        CURRENT (person_id,
                        shift_id,
                        priority, datetime)
                    VALUES (?, ?, ?, "sdf")"""
            c.execute(query, (str(person_id), str(i[0]), count))
            count += 1
    db.commit()
    db.close()

#####
def get_winners(prt, shift, count, persons_out, nominees):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    q="""SELECT
	c.person_id,
	r.rate,
	p.employment_date 
FROM
	"current" c
JOIN rates r ON c.person_id = r.person_id AND c.shift_id = r.shift_id
JOIN person p ON c.person_id = p.id 
WHERE
	c.priority = ?
AND c.shift_id  = ? """
    for key, value in persons_out.items():
        if value == False:
            q += """ AND c.person_id != """ + str(key)
    q += """ ORDER BY rate DESC, employment_date """
    if nominees == False:
        q += """LIMIT ?"""
        c.execute(q, (prt, shift, count))
    else:
        c.execute(q, (prt, shift))
    res = c.fetchall()
    return res
    db.commit()
    db.close()





#1)учесть запреты на смены.
# 2) сделать признак админа в persons и выдавать ему отдельное меню
# 3) переделать на f строки



def get_persons_id():
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    q="""SELECT
	id
FROM
	person p
WHERE
	enabled = 1
    """
    c.execute(q)
    persons_out = {}
    for p in c.fetchall():
        persons_out[p[0]]=True
    return persons_out
    #return c.fetchall()
    db.commit()
    db.close()

def insert_winners(person_id, shift_id):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    q="""INSERT INTO vote (person_id,shift_id) VALUES (?, ?)"""
    c.execute(q, (person_id, shift_id))
    db.commit()
    db.close()

def del_vote():
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    q="""DELETE FROM vote"""
    c.execute(q)
    db.commit()
    db.close()

#del_vote()

def get_shift_out():
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    shifts = get_shifts_all(True, False)
    shifts_out = {}
    for sh in shifts:
        shifts_out[sh[0]]=sh[1]
    return shifts_out
    db.commit()
    db.close()


# q="INSERT INTO current (id, person_id, shift_id, prioritry) VALUES ('1', '2', '4', '0')"
# c.execute(q)
# c.execute("INSERT INTO current VALUES (6, 1, 1, 1)")
# c.execute("INSERT INTO current VALUES (7, 1, 1, 1)")
#


# choice = [4,2,1,5,3]
# id_tg = "392408856"
# insert_choice(choice, id_tg)



#c.execute("INSERT INTO current (person_id, shift_id, priority) VALUES (2, 4, 0)")



#### Получаем роль юзера (админ или нет)
def is_user_admin(person_id):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    q="""SELECT
	admin
FROM
	person
WHERE
	tg_id = ?"""
    c.execute(q, (str(person_id),))
    if c.fetchone()[0] == 1:
        return True
    else:
        return False

    db.commit()
    db.close()

def get_admin_tg_id():
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    q="""SELECT
	tg_id
FROM
	person
WHERE
	admin = 1"""
    c.execute(q)
    admin_tg_id = c.fetchone()

    return admin_tg_id[0]

    db.commit()
    db.close()

def get_users_entered_data(entered):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    q = """SELECT
	fio,
	tg_id
FROM
	person p
WHERE enabled = 1 AND """
    if entered == True:
        q += "entered_data = 1"
    else:
        q += "entered_data = 0"

    c.execute(q)
    list_entered = c.fetchall()

    return list_entered

    db.commit()
    db.close()

#t = heck_all_entered_data(True)

#t = get_admin_tg_id()
def check_settings_admin_msg():
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    q="""SELECT admin_received_final_msg  FROM settings s """

    c.execute(q)
    if c.fetchone()[0] == 1:
        return True
    else:
        return False

    db.commit()
    db.close()

def set_admin_msg(bool):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    q="""UPDATE settings SET admin_received_final_msg = """
    if bool:
        q += "1"
    else:
        q += "0"

    c.execute(q)

    db.commit()
    db.close()

#set_admin_msg()

#t = check_settings_admin_msg()
def enter_data_by_user(tg_ig_current):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    q="""update
	person
SET
	entered_data = 1
WHERE
	tg_id = ?"""

    c.execute(q, (tg_ig_current, ))

    db.commit()
    db.close()

#enter_data_by_user("")

def update_period (year, month):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    q = """DELETE FROM settings;"""
    c.execute(q)

    q = """INSERT INTO
    settings (rotation_period)
    VALUES (?)"""

    date = year + "-" + month + "-01 00:00:00"
    c.execute(q, (date,))
    db.commit()
    db.close()

def clear_entered_data_in_person():
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    q = """update
	person
SET
	entered_data = 0"""

    c.execute(q)
    db.commit()
    db.close()

#update_period("2020", "01")

def insert_voting_results_into_history():
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    q = """SELECT
	s.rotation_period
FROM
	settings s 
"""
    c.execute(q)
    period = c.fetchone()[0]
    q = """INSERT
	INTO
	history (person_id,
	shift_id,
	period)
SELECT
	person_id ,
	shift_id,
	? period
FROM
	vote v"""
    #period = '2024-12-01 00:00:00'
    c.execute(q, (period,))

    #year = period[0:4]
    #month = period[5:7]
    period = datetime.datetime.strptime(period, "%Y-%m-%d %H:%M:%S")
    days_in_month = calendar.monthrange(period.year, period.month)[1]
    period += datetime.timedelta(days=days_in_month)

    c.execute(q, (period,))
    db.commit()
    db.close()
def check_current_vote_in_history():
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    q = """SELECT COUNT(1)  FROM history h WHERE period = (SELECT s.rotation_period FROM settings s LIMIT 1)"""
    c.execute(q)
    if c.fetchone()[0] == 0:
        return False
    else:
        return True
    db.commit()
    db.close()

def get_current_period(arg):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    q="""SELECT
	s.rotation_period
FROM
	settings s
"""
    c.execute(q)
    period = c.fetchone()[0]
    period_base = period
    period1 = datetime.datetime.strptime(period, "%Y-%m-%d %H:%M:%S")
    days_in_month = calendar.monthrange(period1.year, period1.month)[1]
    period2 = period1 + datetime.timedelta(days=days_in_month)
    if period1.month < 10:
        month1 = "0" + str(period1.month)
    else:
        month1 = str(period1.month)
    if period2.month < 10:
        month2 = "0" + str(period2.month)
    else:
        month2 = str(period2.month)

    if str(arg) == "normal":
        period_text = month1 + "." + str(period1.year)
        return period_text
    if str(arg) == "curr_period":
        period_text = str(period1.year) + "-" + month1
        return period_text
    if str(arg) == "curr_period+1":
        period_text = str(period2.year) + "-" + month2
        return period_text
    if str(arg) == "curr_period_base":
        period_text = str(period1.year) + "-" + month1 + "-01 00:00:00"
        return period_text
    if str(arg) == "curr_period+1_base":
        period_text = str(period2.year) + "-" + month2 + "-01 00:00:00"
        return period_text

    db.commit()
    db.close()

def check_table_is_empty(table):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    q = """SELECT COUNT(1)  FROM """ + str(table)
    c.execute(q)
    if c.fetchone()[0] == 0:
        return True
    else:
        return False
    db.commit()
    db.close()


def del_results_from_history():
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    period = str(get_current_period("curr_period"))
    q = """DELETE
FROM
	history
WHERE
	period LIKE '""" + period + "%'"

    c.execute(q)

    period = str(get_current_period("curr_period+1"))
    q = """DELETE
    FROM
    	history
    WHERE
    	period LIKE '""" + period + "%'"

    c.execute(q)


    db.commit()
    db.close()

#del_results_from_history()

#def add_missed_in_current():

def insert_shift_in_current(choice, pers_id, priority):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    #person_id = get_person_id_from_tg_id(tg_id)

    query = """INSERT
                        INTO
                        CURRENT (person_id,
                        shift_id,
                        priority, datetime)
                    VALUES (?, ?, ?, datetime('now'))"""

    c.execute(query, (pers_id, choice, priority))
    db.commit()
    db.close()

def get_chosen_shift_id(pers_id):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    query="""SELECT
	c.shift_id
FROM
	"current" c
JOIN person p ON
	c.person_id = p.id
WHERE
	p.id = ?
ORDER BY
	c.priority"""

    c.execute(query, (str(pers_id), ))
    shifts = c.fetchall()
    return shifts
    db.commit()
    db.close()

def get_person_fio_from_tg_id (tg_id):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    query = """SELECT
        p.fio
    FROM
        person p
    WHERE
        p.tg_id = ?"""
    c.execute(query, (str(tg_id), ))
    fio = c.fetchone()
    return fio
    db.commit()
    db.close()

#get_person_fio_from_tg_id(7050450693)
def get_prohibuted ():
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    query = """SELECT
	p2.tg_id,
	p.shift_id
FROM
	prohibited p
JOIN person p2 ON
	p.person_id = p2.id"""
    c.execute(query)
    prohibited = c.fetchall()
    return prohibited
    db.commit()
    db.close()




#get_chosen_shift_id (2)
#===

def close_base_conn():
    db = sqlite3.connect('rotation.db')
    c = db.cursor()
    db.commit()
    db.close()

#close_base_conn()




db.commit()
db.close()






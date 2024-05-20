import sqlite3

db = sqlite3.connect('rotation.db')
c = db.cursor()


def get_shifts ():
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

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
    p.enabled = 1"""

    # query = "SELECT id, fullname  FROM shifts s WHERE enabled = 1"
    c.execute(query)
    shifts = c.fetchall()
    print(shifts)
    return shifts
    db.commit()
    db.close()







def find_person_id_for_tg_id(id_tg):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    query = "SELECT id FROM person p WHERE tg_id = '" + str(id_tg) + "'"
    print (query)
    c.execute(query)
    id = c.fetchone()[0]
    return id

    db.commit()
    db.close()


def insert_choice(choice, tg_id):
    db = sqlite3.connect('rotation.db')
    c = db.cursor()

    person_id = find_person_id_for_tg_id(tg_id)
    print(person_id)
    count = 0
    for i in choice:
        if i[1] == str(tg_id):
            query = """INSERT INTO current (person_id, shift_id, priority) VALUES (?, ?, ?)"""
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
    query="""SELECT c.priority, s.fullname, p.tg_id FROM "current" c JOIN shifts s ON c.shift_id = s.id JOIN person p ON c.person_id = p.id WHERE p.tg_id = ? ORDER BY p.tg_id, c.priority"""

    c.execute(query, (str(tg_id), ))
    shifts = c.fetchall()
    return shifts
    db.commit()
    db.close()


# choice = [[2, '181564144'], [4, '181564144'], [5, '181564144'], [2, '663014633'], [1, '181564144']]
# insert_choice(choice,"181564144")





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

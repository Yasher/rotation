import sqlite3

db = sqlite3.connect('rotation.db')

c = db.cursor()

def get_shifts ():
    query = "SELECT id, fullname  FROM shifts s WHERE enabled = 1"
    c.execute(query)
    shifts = c.fetchall()
    return shifts





c.execute("INSERT INTO current VALUES (4, 1, 1, 1)")
id = 1
#query = "SELECT x.fio FROM person x WHERE x.id = " + str(id)

query = "SELECT x.fio FROM person x"

c.execute(query)
# print (c.fetchmany(1))

name = c.fetchall()

# for el in name:
#     print (el[0])
n = name[1][0]

print(n)



# print ("SELECT x.fio, x.id  FROM person x WHERE x.id = " + str(id) + ";")

db.commit()

db.close()
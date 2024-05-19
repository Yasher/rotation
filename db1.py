
import db
#from db import get_shifts

shifts = db.get_shifts()

# print (type(shifts))
#shifts.pop(0)

print (shifts)

shifts.remove(shifts[0])

print (shifts)

#
# print (type(shifts[0]))
# q=str(shifts[0][0])+", '"+shifts[0][1]+"'"
# print(q)


#shifts.remove((1, '08:30 - 20:30'))
         #      (1, '08:30 - 20:30')

# shifts.remove((q))
# print (shifts)


# a = [234, 32, "dsfjhg"]
# a.pop(0)
# print (a)
# print(type(shifts))

#
# for i in shifts:
#     print (i[0])
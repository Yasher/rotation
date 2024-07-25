import db

t = db.get_persons_id()
print(t)

for n in t.keys():
    print(n)
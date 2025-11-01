import datetime
import db
import logging

logger = logging.getLogger("voting")

#РАСЧЕТ rate ПЕРЕД voting
def voting():
    db.delete_shift_rates()
    db.insert_shift_rates()

    #persons_out = получить словарь person:true\false - выбрана смена или нет
    persons_out = db.get_persons_id()
    #shifts_out = -\\- по сменам id:колво невыбраных чел и минусовать выбраных
    shifts_out = db.get_shift_out()
    #добавляем в current новые смены и новых пользователей, если они есть (для корректного более-менее промежуточного результата)
    add_missed_in_current(db.get_persons_id())

    db.del_vote() #очищаем таблицу vote
    shifts = db.get_shifts_all(True, False) #список смен
   # print (shifts)
   # with open("scheme.txt", "w") as file:
   #     file.write(str(shifts) + "\n")
    count_shifts_prts = len (shifts) #количество смен = количество кругов розыгрыша
    #print (count_shifts_prts)
    with open("scheme.txt", "w") as file:
        file.write(str(datetime.datetime.now()) + "\n" + "Распределение смен"+ "\n\n" + \
            "Формат записи сотрудника - [Фамилия И.], [количество дней назад выбирал смену (кратно месяцам)], [месяц приема на работу]" + "\n")
    for round in range(count_shifts_prts):  #проход по кругам
        print("\n >круг " + str(round) + "\n")
        with open("scheme.txt", "a") as file:
            file.write("\n >круг " + str(round + 1) + "\n")
    #count_shifts_prts - количество приоритетов = количество разных смен
        for shift in shifts: #проход по сменам
            #проверяем сколько у смены вакантных мест
            #print(shifts_out)
            if shifts_out[shift[0]] != 0: #проверяем наличие текущей смены в out-списке (смена занята)
                count = shift[1] #количество экземпляров смены (парная, непарная)
                print("\n >>>>>смена " + db.get_shift_name(shift[0])[0] + "\n")
                with open("scheme.txt", "a") as file:
                    file.write("\n >>>>>смена " + db.get_shift_name(shift[0])[0] + "\n")

                nominees=db.get_winners(round, shift[0], count, persons_out, True, False)
                nominees_for_print=db.get_winners(round, shift[0], count, persons_out, True, True)
                print("Смену выбрали: " + str(nominees_for_print))
                with open("scheme.txt", "a") as file:
                    file.write("Смену выбрали: " + str(nominees_for_print) + "\n")

                winners = db.get_winners(round, shift[0], shifts_out[shift[0]], persons_out, False, False)
                winners_for_print = db.get_winners(round, shift[0], shifts_out[shift[0]], persons_out, False, True)#получаем список тех кто хочет данную смену. Ограничение длины списка = count
                print("Победители: " + str(winners_for_print))
                with open("scheme.txt", "a") as file:
                    file.write("Победители: " + str(winners_for_print) + "\n")
                for winner in winners: #перебираем победителей данной смены
                    db.insert_winners(winner[0], shift[0]) #пишем хотящих в базу в таблицу vote
                    shifts_out[shift[0]] -= 1 #-1 к количеству экземпляров данной смены
                    persons_out[winner[0]]=False #победитель дальше не участвует
                #print("Persons_out: ")
                #print(persons_out)
            else:
                print(f"Смена {db.get_shift_name(shift[0])[0]} уже занята!")
                with open("scheme.txt", "a") as file:
                    file.write(f"Смена {db.get_shift_name(shift[0])[0]} уже занята!" + "\n")



def add_missed_in_current(persons):
    for p in persons:

        shifts = db.get_shifts_all (True, False, 1, p)
        shifts_list = []
        for sh in shifts:
            shifts_list.append(sh[0])
        current_shifts = db.get_chosen_shift_id(p)
        current_shifts_list = []
        for c_sh in current_shifts:
            current_shifts_list.append(c_sh[0])
        count_current_shifts = len(current_shifts_list)


        for sh in shifts_list:
            if current_shifts_list.count(sh) == 0:
                db.insert_shift_in_current(sh, p, count_current_shifts)
                count_current_shifts+=1
            #sh = current_shifts_list.count(1)

        i=1





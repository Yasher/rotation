import db



#РАСЧЕТ rate ПЕРЕД voting
def voting():
    db.delete_shift_rates()
    db.insert_shift_rates()

    #persons_out = получить словарь person:true\false - выбрана смена или нет
    persons_out = db.get_persons_id()
    #shifts_out = -\\- по сменам id:колво невыбраных чел и минусовать выбраных
    shifts_out = db.get_shift_out()

    db.del_vote()
    shifts = db.get_shifts_all(True, False)
    print (shifts)
    count_shifts_prts = len (shifts)
    print (count_shifts_prts)
    for round in range(count_shifts_prts):
        print("круг " + str(round))
    #count_shifts_prts - количество приоритетов = количество разных смен
        for shift in shifts:
            #проверяем сколько у смены вакантных мест
            print(shifts_out)
            if shifts_out[shift[0]] != 0:
                count = shift[1]
                print("смена " + str(shift[0]))
                winners = db.get_winners(round, shift[0], count, persons_out)
                print(winners)
                for winner in winners:
                    db.insert_winners(winner[0], shift[0])
                    shifts_out[shift[0]] -= 1
                    persons_out[winner[0]]=False
                print(persons_out)
            else:
                print(f"Смена {shift[0]} уже занята!")


            #убираем 1 или 2 у смены в счетчике




        #функция выбора 1 или 2х человек из argue

        #проверка вышла ли смена? - дальше




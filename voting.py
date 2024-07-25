import db



#РАСЧЕТ rate ПЕРЕД voting
def voting():
    db.delete_shift_rates()
    db.insert_shift_rates()

    #persons_out = получить словарь person:true\false - выбрана смена или нет
    persons_out = db.get_persons_id()
    #shifts_out = -\\- по сменам id:колво невыбраных чел и минусовать выбраных
    shifts_out = db.get_shift_out()

    db.del_vote() #очищаем таблицу vote
    shifts = db.get_shifts_all(True, False) #список смен
    print (shifts)
    count_shifts_prts = len (shifts) #количество смен = количество кругов розыгрыша
    print (count_shifts_prts)
    for round in range(count_shifts_prts):  #проход по кругам
        print("круг " + str(round))
    #count_shifts_prts - количество приоритетов = количество разных смен
        for shift in shifts: #проход по сменам
            #проверяем сколько у смены вакантных мест
            #print(shifts_out)
            if shifts_out[shift[0]] != 0: #проверяем наличие текущей смены в out-списке (смена занята)
                count = shift[1] #количество экземпляров смены (парная, непарная)
                print("смена " + str(shift[0]))

                nominees=db.get_winners(round, shift[0], count, persons_out, True)
                print("Смену выбрали: " + str(nominees))

                winners = db.get_winners(round, shift[0], shifts_out[shift[0]], persons_out, False) #получаем список тех кто хочет данную смену. Ограничение длины списка = count
                print("Победители: " + str(winners))
                for winner in winners: #перебираем победителей данной смены
                    db.insert_winners(winner[0], shift[0]) #пишем хотящих в базу в таблицу vote
                    shifts_out[shift[0]] -= 1 #-1 к количеству экземпляров данной смены
                    persons_out[winner[0]]=False #победитель дальше не участвует
                print("Persons_out: ")
                print(persons_out)
            else:
                print(f"Смена {shift[0]} уже занята!")

#voting()
            #убираем 1 или 2 у смены в счетчике




        #функция выбора 1 или 2х человек из argue

        #проверка вышла ли смена? - дальше




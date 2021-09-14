import random
f = open("maps/Map_2level.txt", 'w')

for i in range(57):
        number1 = (random.randint(0, 500))
        number2 = (random.randint(0, 500))
        number3 = (random.randint(0, 150))
        number4 = (random.randint(0, 100))
        f.writelines(f"{str(number1)},{str(number2)},{str(number3)},{str(number4)}\n")
        f.close()
from datetime import datetime
import os

if __name__  == '__main__':
    models = ["euc", "man"]

    f = open("running.txt", 'a')
    for model in range(0, 2):
        for i in range(4, 11):
            os.system("python3 run.py aprox %d 0 %s" % (i , models[model]))

    for model in range(0, 2):
        for i in range(4, 11):
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            f.write("%s\nRodando bnb modelo = %s i = %d\n" % (dt_string, models[model], i))
            os.system("python3 run.py bnb %d 0 %s" % (i , models[model]))
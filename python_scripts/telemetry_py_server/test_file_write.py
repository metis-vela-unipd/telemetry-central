from random import randint

with open('testFile.txt', 'w') as file:
    while True:
        try:
            file.write(str(randint(0, 10)))
        except KeyboardInterrupt:
            break
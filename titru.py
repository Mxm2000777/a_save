chisla = [['1', '2'], ['11', '2'], ['1', '12'], ['11', '12'], ['-11', '-12'], ['-11', '12'], ['-12', '11'], ['10', '10'], ['10', '5']]
for A in range(-100, 100):
    YES = 0
    NO = 0
    for i in chisla:
        s = int(i[0])
        t = int(i[1])
        if s > 10 or t > A:
            YES += 1
        else:
            NO += 1
    if NO == 5:
        print(A)
x = 0 or 1
y = not 1
print(x, y)
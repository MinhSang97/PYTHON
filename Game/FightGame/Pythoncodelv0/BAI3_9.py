import sys
sys.stdin = open("BAI3_9.inp","r")
sys.stdout = open("BAI3_9.out","w")
a = []
while True:
    try:
        line =input()
        try:
            x = int(line)
            a.append(x)
        except ValueError:
            break
    except EOFError:
        break
t = 0
d = 0
for i in range(0,len(a)):
    if a[i]%2==0:
        t+=a[i]
        d = 1
if d == 0:
    print("-1")
else:
    print(t)
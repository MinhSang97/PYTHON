import sys
sys.stdin = open("0021.inp","r")
sys.stdout = open("0021.out","w")
n = int(input())
a = []
b = []
for i in range(0,n):
    x = int(input())
    a.append(x)
b = sorted(set(a),key=a.index)
c = []
for i in range(0,len(b)):
    c.append(a.count(b[i]))
M = max(c)
for i in range(0,len(c)):
    if c[i]==M:
        print(b[i],c[i])
import sys
sys.stdin = open("0002.inp","r")
sys.stdout = open("0002.out","w")

s = input()
a = s.lower()
b = sorted(set(a),key=a.index)

c = []
for i in range(0,len(b)):
    c.append(a.count(b[i]))
for i in range(0,len(b)):
    print(b[i],":",c[i],sep="",end=" ")
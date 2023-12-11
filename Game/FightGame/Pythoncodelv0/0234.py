import sys
sys.stdin = open("0234.inp","r")
sys.stdout = open("0234.out","w")
m,n = map(int,input().split())
d = ""
for i in range (m,n+1):
    s = str(i)
    for j in s:
        if j=="0":
            d+=j
print (len(d))
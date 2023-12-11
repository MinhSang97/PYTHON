import sys,math
sys.stdin = open("0019.inp","r")
sys.stdout = open("0019.out","w")
a,b,c = map(int,input().split())
if a+b<c or a+c<b or b+c<a:
    print("Day khong phai la 3 canh cua mot tam giac")
elif a+b==c or a+c==b or b+c==a:
    print("Day khong phai la 3 canh cua mot tam giac")
else:
    print("Day la 3 canh cua mot tam giac")
    cv=a+b+c
    p=cv/2
    dt=math.sqrt(p*(p-a)*(p-b)*(p-c))
    print("%0.2f"%cv,"%0.1f"%dt)


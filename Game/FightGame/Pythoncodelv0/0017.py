import sys,math
sys.stdin = open("0017.inp","r")
sys.stdout = open("0017.out","w")

a,b = map(float,input().split())
TBCN =(a+b*2)/3
print("%0.1f"%TBCN)
if TBCN>=8:print("Gioi")
elif 6.5<=TBCN <8:print("Kha")
elif 5.0<=TBCN <6.5:print("Trung Binh")
elif  3.5<=TBCN <5:print("Yeu")
elif TBCN<3.5:print("Kem")
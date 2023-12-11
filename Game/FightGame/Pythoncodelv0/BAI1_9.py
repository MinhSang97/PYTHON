import sys
sys.stdin = open("BAI1_9.inp","r")
sys.stdout = open("BAI1_9.out","w")

t,v,a = map(float,input().split())
kv = input()
dc = 0
if kv == "KV1":
    dc = 0.50
elif kv == "KV2":
    dc= 0.75
else:
    dc = 0
dtb = (t*2+v*2+a)/5+dc
print("%0.2f"%dtb,"-",end=" ")
if dtb>=8:
    print("GIOI")
elif 6.5<= dtb < 8:
    print("KHA")
elif 5<= dtb  <6.5:
    print("TRUNG BINH")
elif dtb<5:
    print("YEU")

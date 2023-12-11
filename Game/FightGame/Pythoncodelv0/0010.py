import sys
sys.stdin = open("0010.inp","r")
sys.stdout = open("0010.out","w")

n = int(input())
a = list(map(int,input().split()))
t = 0
dem = 0 
for i in range(0,len(a)):
    if a[i]%2==0:
        dem+=1
        t+=a[i]
tbc = t/dem
print("%0.2f"%tbc)
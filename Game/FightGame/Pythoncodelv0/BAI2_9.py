import sys
sys.stdin = open("BAI2_9.inp","r")
sys.stdout = open("BAI2_9.out","w")

n = int(input())
a = list(map(int,input().split()))
for i in range(0,len(a)):
    if a[i]%3==0 and a[i]%5==0:
        print(a[i],end=" ")
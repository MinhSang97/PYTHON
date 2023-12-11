import sys
sys.stdin = open("0018.inp","r")
sys.stdout = open("0018.out","w")

tuổi = int(input())
if 0< tuổi<=11:print("Thieu nhi")
elif 11< tuổi <=25:print("Thieu nien")
elif 25< tuổi <=50:print("Trung nien")
elif tuổi >50:print("Lao nien")
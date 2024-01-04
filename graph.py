import matplotlib.pyplot as plt

lp_file = "lpcoeffs23.txt"
lpcc_file = "lpcccoeffs23.txt"
mfcc_file = "mfcccoeffs23.txt"

lp2 = []
lp3 = []
lpcc2 = []
lpcc3 = []
mfcc2 = []
mfcc3 = []

with open(lp_file, 'r') as lpfile:
    for line1 in lpfile:
        columns1 = line1.split()
        lp2.append(float(columns1[0]))
        lp3.append(float(columns1[1]))
with open(lpcc_file, 'r') as lpccfile:
    for line2 in lpccfile:
        columns2 = line2.split()
        lpcc2.append(float(columns2[0]))
        lpcc3.append(float(columns2[1]))
with open(lpcc_file, 'r') as mfccfile:
    for line3 in mfccfile:
        columns3 = line3.split()
        mfcc2.append(float(columns3[0]))
        mfcc3.append(float(columns3[1]))

plt.subplot(3,1,1)

plt.scatter(lp2, lp3, 1 ,label= "LP coefficient values", color="red")
plt.xlabel("LP 2nd coefficient")
plt.ylabel("LP 3rd coefficient")

plt.grid(True, linestyle="--", alpha=0.7)

plt.subplot(3,1,2)

plt.scatter(lpcc2, lpcc3, 1, label= "LP coefficient values", color="green")

plt.xlabel("LPCC 2nd coefficient")
plt.ylabel("LPCC 3rd coefficient")

plt.grid(True, linestyle="--", alpha=0.7)

plt.subplot(3,1,3)

plt.scatter(mfcc2, mfcc3, 1 , label= "LP coefficient values", color="blue")

plt.xlabel("MFCC 2nd coefficient")
plt.ylabel("MFCC 3rd coefficient")


plt.grid(True, linestyle="--", alpha=0.7)
plt.show()


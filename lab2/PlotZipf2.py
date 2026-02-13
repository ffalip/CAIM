import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

'''
spc = "ªº:.!@#$%^&*()-+?_=,<>/"
def valid(word):
    if any(c in spc for c in word):
        return False
    return True
'''


def fits(r, a, b, c):
    return c / pow((r+b),a)

map = [{}, {}, {}, {}]
valors = [[], [], [], []]
end = False
docs = ["letter", "classic", "standard", "whitespace"]
i = 0
fig, axs = plt.subplots(1,4, figsize=(20,10))
for doc in docs:
    with open(f"data/{doc}Novels.txt", encoding='utf-8') as data:
        for line in data:
            if line == "--------------------\n": 
                end = True
                print(f"Data from {doc}Novels.txt")
            elif not end:
                line.strip()
                n, word = line.split(",", 1)
                map[i][word] = int(n)
                

    sns.set_theme()
    
    valors[i] = list(map[i].values())
    valors[i].sort(reverse=True)

    if not valors[i]:
        print("No data")
    else:
        print(f"Data from {doc}Novels.txt")

    
    axs[i].plot(valors[i], label='data') 

    popt, pcov = curve_fit(fits, range(0, len(valors[i])), valors[i], bounds=([0.5, 0, -np.inf], [3, np.inf, np.inf]))
    axs[i].plot(range(0, len(valors[i])), fits(range(0, len(valors[i])), *popt), 'r-', label='curve fit')

    #axs[i].ylabel("freq (log)")
    #axs[i].xlabel("rank (log)")

    axs[i].set_yscale('log')
    axs[i].set_xscale('log')
    
    axs[i].legend()
    i += 1
    

plt.title("Zipf of Novels", fontsize='large', fontweight = 'bold', pad = 20)
plt.tight_layout()
plt.show()

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

spc = "ªº:.!@#$%^&*()-+?_=,<>/0123456789"

def valid(word):
    if any(c in spc for c in word):
        return False
    return True

def fits(r, a, b, c):
    return c / pow((r+b),a)

def fits2(r, a, b, c):
    return c*pow((r+b), -a)

#llegir txt crear un map amb (word, num) descartant paraules 
map = {}
end = False
with open("data/dades.txt") as data:
    for line in data:
        if line == "--------------------\n": 
            end = True
        elif not end:
            line.strip()
            n, word = line.split(",", 1)
            if valid(word):
                map[word] = int(n)

sns.set_theme()

valors = list(map.values())
valors.sort(reverse=True)
plt.figure(figsize=(10,10))
plt.plot(valors, label='data') 

#a ~= 1
popt, pcov = curve_fit(fits, range(0, len(valors)), valors, bounds=([0.5, 0, -np.inf], [3, np.inf, np.inf]))
plt.plot(range(0, len(valors)), fits(range(0, len(valors)), *popt), 'r-', label='curve fit')

#a ~= 1.7
#popt2, pcov2 = curve_fit(fits, range(1000, len(valors)), valors[-(len(valors) - 1000):], bounds=([0.5, 0, -np.inf], [3, np.inf, np.inf]))
#plt.plot(range(1000, len(valors)), fits(range(1000, len(valors)), *popt2), 'g-', label='fit2')

plt.xlabel("rank (log)")
plt.ylabel("freq (log)")

plt.yscale('log')
plt.xscale('log')
plt.title("Rank-Frequency of 20_newsgroups", fontsize='large', fontweight = 'bold', pad = 20)
plt.text(0.5, 0.8, f"a = {popt[0]:.4f}\nb = {popt[1]:.4f}\nc = {popt[2]:.4f}", fontsize=11, transform=plt.gcf().transFigure, bbox=dict(facecolor='white', alpha=0.6, edgecolor='black', boxstyle='round,pad=0.4'))
plt.legend()
plt.show()



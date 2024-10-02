import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

spc = "ªº:.!@#$%^&*()-+?_=,<>/0123456789"

def valid(word):
    if any(c in spc for c in word):
        return False
    return True

def heaps(n, k, B):
    return k * pow(n, B)

#llegir txt crear un map amb (word, num) descartant paraules 
"""
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
"""
sns.set_theme()

valors = list(map.values())
valors.sort(reverse=True)
plt.figure(figsize=(10,10))
sns.lineplot(valors)

#popt, pcov = curve_fit(fits, range(0, len(valors)), valors, bounds=([0.5, 0, -np.inf], [3, np.inf, np.inf]))
#plt.plot(range(0, len(valors)), fits(range(0, len(valors)), *popt), 'r-', label='fit')

#a ~= 1.7 
#popt2, pcov2 = curve_fit(fits, range(1000, len(valors)), valors[-(len(valors) - 1000):], bounds=([0.5, 0, -np.inf], [3, np.inf, np.inf]))
#plt.plot(range(1000, len(valors)), fits(range(1000, len(valors)), *popt2), 'g-', label='fit2')

plt.xlabel("rank (log)")
plt.ylabel("freq (log)")

plt.yscale('log')
plt.xscale('log')
plt.show()

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
with open("dades.txt") as data:
    for line in data:
        line.strip()
        n, word = line.split(",", 1)
        if valid(word):
            map[word] = int(n)

#with open("xd.txt", 'w') as file:
#    for w in map:
#        file.write(f"{map[w]}, {w}")
sns.set_theme()
sns.set_style("darkgrid")
sns.color_palette("pastel")

valors = list(map.values())
valors.sort(reverse=True)
plt.figure(figsize=(10,10))
sns.lineplot(valors)

#a ~= 1
popt, pcov = curve_fit(fits, range(0, len(valors)), valors)
plt.plot(range(0, len(valors)), fits(range(0, len(valors)), *popt), 'r-', label='fit')

#a ~= 1.7
popt2, pcov2 = curve_fit(fits, range(1000, len(valors)), valors[-(len(valors) - 1000):])
plt.plot(range(1000, len(valors)), fits(range(1000, len(valors)), *popt2), 'g-', label='fit2')
print(popt2)

plt.xlabel("rank (log)")
plt.ylabel("freq (log)")

plt.yscale('log')
plt.xscale('log')
plt.show

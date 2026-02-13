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
x_values = []
y_values = []
with open("data/dataHeapsAll.txt") as data:
    for line in data:
        df_word, n_words = line.split(",")
        x_values.append(int(n_words))
        y_values.append(int(df_word))


sns.set_theme()

plt.figure(figsize=(10,10))
plt.scatter(x_values, y_values, label='Data') 

popt, pcov = curve_fit(heaps, x_values, y_values, bounds=([0, 0], [100, 1]))
plt.plot(x_values, heaps(x_values, *popt), 'r-', label='Curve fit')

plt.xlabel("Number of words (log)")
plt.ylabel("Number of different words (log)")

plt.xscale('log')
plt.yscale('log')

plt.title("Heaps' Law (log scale)", fontsize='large', fontweight = 'bold', pad = 20)
plt.text(0.5, 0.82, f"k = {popt[0]:.4f}\nB ={popt[1]:.4f}", fontsize=11, transform=plt.gcf().transFigure, bbox=dict(facecolor='white', alpha=0.6, edgecolor='black', boxstyle='round,pad=0.4'))
plt.legend()
plt.show()

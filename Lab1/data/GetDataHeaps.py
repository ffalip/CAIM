spc = "ªº:.!@#$%^&*()-+?_=,<>/0123456789"

def valid(word):
    if any(c in spc for c in word):
        return False
    return True

with open("dataHepasAll.txt", 'w') as res:
    for i in range(1,33):
        with open(f"dataHeaps_{i}.txt") as data:
            end = False
            N_words = 0
            diff_words = 0
            for line in data:
                if line == "--------------------\n":
                    end = True
                elif not end:
                    line.strip()
                    n, word = line.split(",", 1)
                    if valid(word):
                        N_words += int(n)
                        diff_words += 1
            res.write(f"{diff_words},{N_words}\n")

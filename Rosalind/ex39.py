"""**Piotrek's solution**"""

with open('input.txt', 'r') as file:
    lines = file.readlines()
dnas = []
temp = []
for line in lines:
    if line.startswith('>'):
        temp = ''.join(temp)
        dnas.append(temp)
        temp = []
        continue
    else:
        temp.append(line[:-1])
temp = ''.join(temp)
dnas.append(temp)
dnas.remove('')

def is_transition(nuc_first: str, nuc_second: str) -> bool:
    # A<->G
    # C<->T
    translations = {"A": "G", "G": "A", "C": "T", "T": "C"}
    # print(nuc_first + " " + nuc_second+"\n")
    return translations[nuc_first] == nuc_second

def transition_transversion_ratio(s: str, t: str) -> float:
    transition_counter = 0
    transversion_counter = 0
    for i in range(len(s)):
        if s[i] != t[i]:
            if is_transition(s[i], t[i]):
                transition_counter += 1
            else:
                transversion_counter += 1
    return transition_counter / transversion_counter

print(transition_transversion_ratio(dnas[0], dnas[1]))

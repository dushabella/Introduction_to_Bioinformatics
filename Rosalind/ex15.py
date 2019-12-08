from typing import List

dna = str()
with open("input.txt", "r") as file:
    for line in file:
        if line.startswith(">"):
            continue
        else:
            dna += line[:-1]
print(dna)

def failure_array(sequence: str) -> List[int]:
    n = len(sequence)
    P = [0] * n
    k = 0
    for i in range(1, n):
        while k > 0 and sequence[i] != sequence[k]:
            k = P[k - 1]
        if sequence[k] == sequence[i]:
            k += 1
        P[i] = k
    return P

for element in failure_array(dna):
    print(element, end=" ")
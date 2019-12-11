from math import log10
from typing import List

with open("input.txt", "r") as file:
    lines = file.readlines()
dna_string = lines[0][:-1]
gc_content = lines[1].split()
gc_content = [float(item) for item in gc_content]

# calculate a probability of a string
def calculate_probability(sequence: str, x: float) -> float:
    probability = 0
    for chara in sequence:
        if chara in "GC":
            probability += log10(x / 2)
        else:
            probability += log10((1 - x) / 2)
    return probability

# create and print an array of probabilities
def create_array(sequence: List[str], gc_contents: List[float]) -> List[float]:
    probabilities = list()
    for x in gc_contents:
        p = calculate_probability(sequence, x)
        probabilities.append(p)
        print(p, end = " ")
    return probabilities

create_array(dna_string, gc_content)
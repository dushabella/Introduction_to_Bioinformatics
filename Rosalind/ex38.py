from typing import Dict, List, Tuple
import numpy as np
"""**Piotrek's solution**"""

def read_data(file_path: str) -> Tuple[str, Dict[str, int], Dict[str, int], List[List[float]], List[List[float]]]:
    with open(file_path, 'r') as file:
        x_emi = file.readline()[:-1]
        file.readline()  # ---
        alpha = {letter: i for i, letter in enumerate(file.readline()[:-1].split())}
        file.readline()  # ---
        stats = {letter: i for i, letter in enumerate(file.readline()[:-1].split())}
        file.readline()  # ---
        file.readline()  # states of transition matrix
        tr = list()
        while True:
            line = file.readline()
            if line[0] == "-":
                break
            tr.append([float(a) for a in line.split()[1:]])
        file.readline()  # emissions of emission matrix
        emi = list()
        while True:
            line = file.readline()
            if len(line) == 0 or line[0] == "-":
                break
            emi.append([float(a) for a in line.split()[1:]])  # rows are states, cols are emissions
        return x_emi, alpha, stats, tr, emi


def forward(emission: str, emissions: Dict[str, int], states: Dict[str, int], transition_matrix: List[List[float]],
            emission_matrix: List[List[float]]) -> np.ndarray:
    fwd = np.zeros((len(states), len(emission)))
    for state in states:
        fwd[states[state], 0] = emission_matrix[states[state]][emissions[emission[0]]] * (1 / len(states))

    for i in range(1, len(emission)):
        for state in states:
            suma = sum([fwd[states[state_from], i-1] * transition_matrix[states[state_from]][states[state]]
                        for state_from in states])
            fwd[states[state], i] = emission_matrix[states[state]][emissions[emission[i]]] * suma
    return fwd


def backward(emission: str, emissions: Dict[str, int], states: Dict[str, int], transition_matrix: List[List[float]],
            emission_matrix: List[List[float]]) -> np.ndarray:
    bwd = np.zeros((len(states), len(emission)))
    for state in states:
        bwd[states[state], len(emission)-1] = 1.0  # (1 / len(states))

    for i in range(len(emission) - 2, -1, -1):
        for state in states:
            bwd[states[state], i] = sum([transition_matrix[states[state]][states[state_to]] *
                                         emission_matrix[states[state_to]][emissions[emission[i+1]]] *
                                         bwd[states[state_to], i + 1] for state_to in states])
    return bwd


x, alphabet, states, tr_matrix, emi_matrix = read_data('input.txt')
f = forward(x, alphabet, states, tr_matrix, emi_matrix)
b = backward(x, alphabet, states, tr_matrix, emi_matrix)
prob = 0
for state in states:
    prob += f[states[state], -1]

answer = np.zeros((len(states), len(x)))
for i in range(len(x)):
    for state in states:
        answer[states[state], i] = (f[states[state], i] * b[states[state], i])/prob

for state in states:
    print(state, end="\t")
print()
for i in range(len(x)):
    for state in states:
        print(round(answer[states[state], i], 4), end="\t")
    print()


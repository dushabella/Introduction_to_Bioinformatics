import numpy as np
from typing import List, Tuple, Dict
"""**Piotrek's solution**"""

def read_file(file_path: str) -> Tuple[str, Dict[str, int], Dict[str, int], List[List[float]], List[List[float]]]:
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
            emi.append([float(a) for a in line.split()[1:]]) # rows - states, cols - emissions

        return x_emi, alpha, stats, tr, emi


def viterbi(x: str, alphabet: List[str], states: List[str],
            transition: List[List[float]], emission: List[List[float]]) -> str:
    st_len = len(states)
    de = {}
    dt = {}
    for i in range(st_len):
        de_tmp = {}
        for j in range(len(alphabet)):
            de_tmp.update({alphabet[j]: emission[i][j]})
        de.update({states[i]: de_tmp})
        dt_tmp = {}
        for j in range(st_len):
            dt_tmp.update({states[j]: transition[i][j]})
        dt.update({states[i]: dt_tmp})

    viter = np.zeros((len(x) + 1, st_len))
    initial_probability = 1

    for i in range(st_len):
        viter[1][i] = de[states[i]][x[0]] * initial_probability * 0.5  # assumption: all states are equal at start

    for i in range(2, len(x) + 1):
        first = []
        before = []
        for j in range(st_len):
            first.append(de[states[j]][x[i-1]])
            before.append(viter[i - 1][j])

        values = []
        for j in range(st_len):
            for k in range(st_len):
                values.append(before[k] * dt[states[k]][states[j]])
            viter[i][j] = first[j] * max(values)
            values = []

    max_ind = 0
    for j in range(1, st_len):
        if viter[-1][j] > viter[-1][max_ind]:
            max_ind = j

    res = states[max_ind]
    for i in range(1, len(viter)-1):
        char = res[0]
        max_ind = 0
        for j in range(1, st_len):
            if viter[len(viter)-i-1][j] * dt[states[j]][char] > viter[len(viter)-i-1][max_ind] * \
                    dt[states[max_ind]][char]:
                max_ind = j
        res = states[max_ind] + res
    return res

x, alphabet, states, transitions, emissions = read_file('input.txt')

print(viterbi(x, list(alphabet.keys()), list(states.keys()), transitions, emissions))
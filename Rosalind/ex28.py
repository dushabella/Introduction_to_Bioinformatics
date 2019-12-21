from typing import Tuple, Dict, List


def read_file(path: str) -> Tuple[str, Dict[str, int], str, Dict[str, int], List[List[float]]]:
    x = ""
    alphabet = dict()
    hidden_path = ""
    states = dict()
    emission_matrix = list()
    with open(path, 'r') as file:
        prob_row_count = -1
        for i, line in enumerate(file):

            if i == 0:
                x = line[0:-1]

            elif i == 2:
                alphabet_list = line.split()
                letter_number = 0
                for letter in alphabet_list:
                    alphabet[letter] = letter_number
                    letter_number += 1

            elif i == 4:
                hidden_path = line[0:-1]

            elif i == 6:
                states_list = line.split()
                state_number = 0
                for state in states_list:
                    states[state] = state_number
                    state_number += 1

            elif i > 8:
                prob_row_count += 1
                emission_matrix.append(list(map(float, line[1:].split())))

    return x, alphabet, hidden_path, states, emission_matrix

x, alphabet, hidden_path, states, emission_matrix = read_file('input.txt')

prob = 1

# print(emission_matrix[alphabet["y"]][states["B"]])

for i in range(len(x)):
    prob *= emission_matrix[states[hidden_path[i]]][alphabet[x[i]]]

print(prob)
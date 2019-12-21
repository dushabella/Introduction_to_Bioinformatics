from typing import Dict, List, Tuple

def read_file(file_path: str) -> Tuple[str, Dict[str, int], List[List[float]]]:
    hidden_path = ""
    states = dict()
    transition_matrix = list()
    with open(file_path, 'r') as file:
        prob_row_counter = -1
        for i, line in enumerate(file):

            if i == 0:
                hidden_path = line[0:-1]

            if i == 2:
                states_list = line.split()
                count = 0
                for state in states_list:
                    states[state] = count
                    count += 1

            if i > 4:
                prob_row_counter += 1
                transition_matrix.append(list(map(float, line[1:].split())))

    return hidden_path, states, transition_matrix

hidden_path, states, transition_matrix = read_file('input.txt')

probability_of_path = 0.5

previous_state = None
for state in list(hidden_path):
    if previous_state is not None:
        probability_of_path *= transition_matrix[states[previous_state]][states[state]]
    previous_state = state

print(probability_of_path)
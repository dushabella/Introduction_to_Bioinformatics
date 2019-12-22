import numpy as np
from Bio import HMM
from Bio.HMM.MarkovModel import MarkovModelBuilder
from Bio.Alphabet import Alphabet
from funcs import viterbi
"""**Elia's solution**"""

#INPUT PHASE

lines = []

with open('input.txt','r') as handle:
    for l in handle.readlines():
        lines.append(l)

iterations = int(lines[0])

x = lines[2].strip()

alphabet = lines[4].split()
emission_alphabet = Alphabet()
emission_alphabet.size = 1
emission_alphabet.letters = alphabet

states = lines[6].split()
states_alphabet = Alphabet()
states_alphabet.size = 1
states_alphabet.letters = states

transition_probs = np.zeros((len(states),len(states)))

for i in range(len(states)):
    prob = lines[9+i].split()
    for j in range(len(states)):
        put = prob[1+j]
        transition_probs[i][j] = float(put)

emission_probs = np.zeros((len(states), len(alphabet)))

for i in range(len(states)):
    prob = lines[13+i].split() # zahardcodowane linie (15 jest dla macierzy o wym 4)
    for j in range(len(alphabet)):
        put = prob[1+j]
        emission_probs[i][j] = float(put)

# INPUT FINISHED

# SOME FUNCTIONS
def estimate_transitions(path,states):
    d_states = {}
    for i in range(len(states)):
        d_states.update({states[i]:i})
    transition_probs = np.zeros((len(states),len(states)))
    for i in range(1,len(path)):
        row = d_states[path[i-1]]
        col = d_states[path[i]]
        transition_probs[row][col] += 1
    for i in range(len(transition_probs)):
        s = sum(transition_probs[i])
        if (s == 0):
            transition_probs[i] = round(1 / len(transition_probs[i]), 3)
        else:
            transition_probs[i] = np.round(transition_probs[i] / s, 3)
    return transition_probs

def estimate_emissions(path, x, states, alphabet):
    d_states = {}
    for i in range(len(states)):
        d_states.update({states[i]: i})
    d_alph = {}
    for i in range(len(alphabet)):
        d_alph.update({alphabet[i]: i})

    emission_probs = np.zeros((len(states), len(alphabet)))
    for i in range(len(x)):
        row = d_states[path[i]]
        col = d_alph[x[i]]
        emission_probs[row][col] += 1
    for i in range(len(states)):
        s = sum(emission_probs[i])
        if s != 0:
            emission_probs[i] = np.round(emission_probs[i] / s, 3)
        else:
            emission_probs[i] = round(1 / len(transition_probs[i]), 3)
    return emission_probs


for i in range(iterations):
    path = viterbi(x, states, alphabet, emission_probs, transition_probs)

    transition_probs = estimate_transitions(path, states)
    emission_probs = estimate_emissions(path, x, states, alphabet)

tab = "\t"

f = open('output.txt', 'w')

f.write(tab + states[0] + tab + states[1] + "\n")
for i in range(len(transition_probs)):
    st = states[i] + tab
    for j in range(len(transition_probs)):
        st += str(transition_probs[i][j]) + tab
    f.write(st + "\n")
f.write("--------\n")
f.write(tab + alphabet[0] + tab + alphabet[1] + tab + alphabet[2] + "\n")
for i in range(len(states)):
    st = states[i] + tab
    for j in range(len(alphabet)):
        st += str(emission_probs[i][j]) + tab
    f.write(st + "\n")
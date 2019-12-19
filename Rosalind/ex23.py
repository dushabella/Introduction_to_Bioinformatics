import numpy as np
from Bio.SubsMat.MatrixInfo import blosum62
from typing import Tuple
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
print(dnas)

def scoring_matrix_distance(s: str, t: str, indel_penalty: int = -5) -> Tuple[int, np.ndarray]:
    s = "-" + s
    t = "-" + t
    m = len(s)
    n = len(t)
    d_t = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            if i == 0:
                d_t[i][j] = j * indel_penalty
            elif j == 0:
                d_t[i][j] = i * indel_penalty
            else:
                try:
                    blosum_penalty = blosum62[(s[i], t[j])]
                except KeyError:
                    blosum_penalty = blosum62[(t[j], s[i])]
                d_t[i][j] = max(d_t[i-1][j-1] + blosum_penalty,
                                d_t[i-1][j] + indel_penalty,
                                d_t[i][j-1] + indel_penalty)
                
    return int(d_t[m-1][n-1]), d_t

distance, dyn_tbl = scoring_matrix_distance(dnas[0], dnas[1])
print(distance)


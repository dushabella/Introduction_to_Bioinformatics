import numpy as np
from Bio.SubsMat.MatrixInfo import pam250
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

def build_dynamic_progr_tbl_4_local_alignment(s: str, t: str, indel_penalty: int = -5) -> Tuple[np.ndarray, np.ndarray]:
    s = "-" + s
    t = "-" + t
    m = len(s)
    n = len(t)
    d_t = np.zeros((m, n))
    d_t_dir = np.zeros((m, n))
    for i in range(1, m):
        for j in range(1, n):
            try:
                pam_penalty = pam250[(s[i], t[j])]
            except KeyError:
                pam_penalty = pam250[(t[j], s[i])]
            options = {
                0: 0,
                3: d_t[i - 1][j] + indel_penalty,  # up
                1: d_t[i][j - 1] + indel_penalty,  # left
                2: d_t[i - 1][j - 1] + pam_penalty  # diagonal
            }
            d_t_dir[i][j] = max(options, key=options.get)
            d_t[i][j] = options[max(options, key=options.get)]
    return d_t, d_t_dir


def get_max_alignment_score(d_t: np.ndarray) -> Tuple[int, int, int]:
    max_align_score = np.max(d_t)

    row, col = np.where(d_t == max_align_score)
    row = row[0]  # there can be multiple best substrings and as I can output any, I choose first one...
    col = col[0]
    return int(max_align_score), row, col


def get_substrings_with_max_score(d_t_dir: np.ndarray, row: int, col: int, s: str, t: str) -> Tuple[str, str]:
    r = ""  # substring of s
    u = ""  # substring of t
    while True:
        direction = d_t_dir[row][col]
        if direction == 2:  # diagonal
            row -= 1
            col -= 1
            r += s[row]
            u += t[col]
        elif direction == 1:  # left
            col -= 1
            u += t[col]
        elif direction == 3:  # up
            row -= 1
            r += s[row]
        elif direction == 0:
            break

    return r[::-1], u[::-1]

dyn_tbl, dyn_tbl_dir = build_dynamic_progr_tbl_4_local_alignment(dnas[0], dnas[1])
max_alig_score, x, y = get_max_alignment_score(dyn_tbl)
r, u = get_substrings_with_max_score(dyn_tbl_dir, x, y, dnas[0], dnas[1])
print(max_alig_score)
print(r)
print(u)
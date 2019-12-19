from typing import List, Tuple
import numpy as np
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

def scoring_matrix_distance(s: str, t: str, indel_penalty: int = -5) -> Tuple[np.ndarray, np.ndarray]:
    """
    Creates dynamic programming table for global alignment task. It also produces matrix containing integers decoding
    direction from where the current result was calculated (1 - from left cell, 3 - from right cell, 2 - from diagonal
    cell).

    CAUTION!!! The function is not universal - it uses built-in scoring method (see "penalty" variable). It should be
    changed to be more versatile.

    :param s:
    :param t:
    :param indel_penalty: linear penalty for adding an indel ("-") to any of strings s or t
    :return: dynamic programing table, and matrix with directions
    """
    # s to wiersze, t to kolumny
    s = "-" + s
    t = "-" + t
    m = len(s)
    n = len(t)
    d_t = np.zeros((m, n))
    d_t_dir = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            if i == 0:
                d_t[i][j] = j * indel_penalty
                if j != 0:
                    d_t_dir[i][j] = 1
            elif j == 0:
                d_t[i][j] = i * indel_penalty
                if i != 0:
                    d_t_dir[i][j] = 3
            else:
                penalty = 0
                if s[i] != t[j]:
                    penalty = -1
                options = {
                    1: d_t[i][j - 1] + indel_penalty,  # left
                    2: d_t[i - 1][j - 1] + penalty,  # diagonal
                    3: d_t[i - 1][j] + indel_penalty  # up
                }
                d_t_dir[i][j] = max(options, key=options.get)
                d_t[i][j] = options[max(options, key=options.get)]
    # print(s, t)
    # print(d_t)
    # print(d_t_dir)
    return d_t, d_t_dir


def get_aligned_strings(d_t_dir: np.ndarray, s: str, t: str) -> Tuple[str, str]:
    """
    Performs backtracking in dynamic programming table (to be more precise: backtracking of the matrix containing
    directions from where current cell's result was calculated). In other words it produces aligned sequences from not
    aligned sequences on the basis of matix of "jumps".
    :param d_t_dir:
    :param s:
    :param t:
    :return: two strings aligned to each other
    """
    r = ""  # substring of s
    u = ""  # substring of t
    row = len(s)
    col = len(t)
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
            r += "-"
        elif direction == 3:  # up
            row -= 1
            r += s[row]
            u += "-"
        elif direction == 0:
            break
    return r[::-1], u[::-1]


def align_global(s1: str, s2: str) -> Tuple[str, str]:
    """
    Gets two strings and returns their global alignments.

    CAUTION!!! It is not versatile, has hardcoded -1 value for linear penalty for indels.

    :param s1:
    :param s2:
    :return: two strings aligned to each other
    """
    _, dyn_tbl_dir = scoring_matrix_distance(s1, s2, -1)
    return get_aligned_strings(dyn_tbl_dir, s1, s2)


def score(seq1: str, seq2: str, match: int = 0, mismatch: int = -1) -> int:
    """
    Calculates alignment score between two sequences where matching characters add 'match' value to score, and
    mismatching characters add 'mismatch' value to score.
    :param seq1:
    :param seq2:
    :param match:
    :param mismatch:
    :return: similarity score of the two strings (int)
    """
    score = 0
    for i in range(min(len(seq1), len(seq2))):
        if seq1[i] == seq2[i]:
            score += match
        else:
            score += mismatch
    score += abs(len(seq1) - len(seq2)) * mismatch
    return score


def insert_indel_at_position(s: str, pos: int, indel: str = "-") -> str:
    """
    Inserts indel character into string at given position.
    :param s:
    :param pos:
    :param indel:
    :return:
    """
    return s[:pos] + indel + s[pos:]


def get_positions_of_new_indels(old_seq: str, new_seq: str) -> List[int]:
    """
    Compares old sequence with new sequence and finds where indels were added. Returns positions of the new indels.
    :param old_seq:
    :param new_seq:
    :return: list of integers where each integer denotes indel position in string (the position is "relative", so i-th
    indel position is given for sequence with added all previous (i-1, i-2, ..., 0) indels).
    """
    result = list()
    old_seq += "x"  # trick to avoid index out of range error
    for i in range(len(new_seq)):
        if new_seq[i] != old_seq[i]:
            old_seq = insert_indel_at_position(old_seq, i)
            result.append(i)
    return result


def multiple_alignment(sequences: List[str]) -> List[str]:
    """
    Performs multiple sequences alignment. See comments for more details.
    :param sequences:
    :return:
    """
    # Part I: calculate similarity (score) of each pair of sequences, get best pair and make global alignment of it.
    # Move newly created aligned sequences into new list "aligned" (means list of sequences that were aligned already).
    # Remove the sequences` ancestors (archetypes) form the "sequences" list (the base/start list)
    n = len(sequences)
    x = 0
    y = 1
    current_max = score(sequences[x], sequences[y])
    for i in range(n):
        for j in range(i + 1, n):
            tmp = score(sequences[i], sequences[j])
            if tmp > current_max:
                current_max = tmp
                x = i
                y = j
    aligned = list(align_global(sequences[x], sequences[y]))
    if x > y:
        del sequences[x]
        del sequences[y]
    else:
        del sequences[y]
        del sequences[x]

    # Part II: Calculate score for each pair [not-yet-aligned-sequence <-> already-aligned-sequence] and repeat until
    # list of sequences (not-yet-aligned) is not empty:
    # a) chose pair with best score and make global alignment for the two sequences
    # b) if sequence from "aligned" list was changed (added indel) make the same changes in every other sequence in
    #    "aligned" - so if new indel was added, add indels to other sequences in the same place
    # c) add newly created sequence (from the not-yet-aligned) to "aligned" list and remove its ancestor (archetype)
    #    from "sequences" list (list of sequences that were NOT aligned yet)

    while len(sequences) != 0:
        x = 0
        y = 0
        current_max = score(sequences[x], aligned[y])
        for i in range(len(sequences)):
            for j in range(len(aligned)):
                tmp = score(sequences[i], aligned[j])
                if tmp > current_max:
                    current_max = tmp
                    x = i
                    y = j
        oryginal = aligned[y]
        best = align_global(sequences[x], aligned[y])
        positions = get_positions_of_new_indels(oryginal, best[1])
        for i in range(len(aligned)):
            for position in positions:
                aligned[i] = insert_indel_at_position(aligned[i], position)
        aligned.append(best[0])
        del sequences[x]
    return aligned


def reorder_sequences(new_sequences: List[str], oryginals: List[str]) -> List[str]:
    """
    Function used for esthetical purposes of the final answer. It reorders new aligned sequences to the same order as
    it was in input sequence.
    :param new_sequences:
    :param oryginals:
    :return:
    """
    result = list()
    for oryginal_sequence in oryginals:
        for new_sequence in new_sequences:
            if oryginal_sequence == new_sequence.replace("-", ""):
                result.append(new_sequence)
    return result

m_align = multiple_alignment(dnas.copy())  # .copy() because dnas will be used one, and multiple_alignment destroys
# the list it receives
n = len(m_align)
scor = np.zeros((n, n))
for i in range(n):
    for j in range(i + 1, n):
        scor[i][j] = score(m_align[i], m_align[j])
print(int(np.sum(scor)))
m_align = reorder_sequences(m_align, dnas)
for sequence in m_align:
    print(sequence)
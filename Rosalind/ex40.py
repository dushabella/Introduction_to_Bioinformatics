from typing import List

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

def profile_matrix(list_of_dna: List[str]) ->List[int]:
    """ creates profile matrix which is based on counting nucleotydes in column """
    """ counts chars (ACTG) in particular column """
    temp_str = ""

    in_columns = len(list_of_dna[0]) # rows of input table; notice that the input dnas must be the same length
    in_rows = len(list_of_dna) # rows of input table

    result = [[0 for i in range(in_columns)] for j in range(4)]

    for i in range(in_columns):
        # print("column", i, ":") # debug
        for j in range(in_rows):
            temp_str += list_of_dna[j][i]
        # print(temp_str) # debug
        A_in_col = temp_str.count("A")
        C_in_col = temp_str.count("C")
        G_in_col = temp_str.count("G")
        T_in_col = temp_str.count("T")
        result[0][i] = A_in_col
        result[1][i] = C_in_col
        result[2][i] = G_in_col
        result[3][i] = T_in_col
        temp_str = ""

    return(result)

def consensus(profile: List[int]) -> str:
    result = ""
    temp = list()
    in_columns = len(profile[0])
    for i in range(in_columns):

        for j in range(4):
            temp.append(profile[j][i])

        if max(temp) == temp[0]:
            result += "A"
        elif max(temp) == temp[1]:
            result += "C"
        elif max(temp) == temp[2]:
            result += "G"
        elif max(temp) == temp[3]:
            result += "T"

        temp = list()

    return result

profile = profile_matrix(dnas)
consensus = consensus(profile)

# print(f"A {profile[0]}")
# print(f"C {profile[1]}")
# print(f"G {profile[2]}")
# print(f"T {profile[3]}")

# print("Consensus: ")
print(consensus)
# print("Profile: ")
print("A:", end=" ")
print(' '.join(map(str, profile[0])))
print("C:", end=" ")
print(' '.join(map(str, profile[1])))
print("G:", end=" ")
print(' '.join(map(str, profile[2])))
print("T:", end=" ")
print(' '.join(map(str, profile[3])))
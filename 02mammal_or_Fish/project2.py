from typing import List, Dict
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from matplotlib import pyplot as plt
from collections import defaultdict
from Bio import pairwise2

def read_file(path: str) -> Dict:
    ''' Reading genes from a file into a dictionary
    in which the keys represent a gene type,
    and the values - the genes of particular species.

    There is 7 different species of each gene. '''
    with open(path, 'r') as file:
        genes = defaultdict(list)
        temp_gene_name = ""
        for i, line in enumerate(file):
            if (i + 1) % 8 == 1:
                temp_gene_name = line
            else:
                values = line.split("\t")
                genes[temp_gene_name].append(values)
    genes = dict(genes)

    return genes

# X = [[i] for i in [2, 8, 0, 4, 1, 9, 9, 0]]
# Y = [[2, 3], [8, 4], [0, 4], [4, 5], [1, 6], [9, 9], [9, 1], [0, 0]]
# print(type(Y))
# print("Y ", Y)
#
# Z = linkage(Y, 'average')
# fig = plt.figure(figsize=(25, 10))
# dn = dendrogram(Z)
# print("average: ", Z)

def distance_matrices(genes: Dict) -> Dict: #Dict[List[List[int]]]
    gene_matrices = defaultdict(list)
    for key in genes:
        i=0
        mtrx = []
        for species in genes[key]:
            species_gene1 = species[-1]
            row = []
            for species in genes[key]:
                i+=1
                species_gene2 = species[-1]
                # print(species_gene2)
                alignment = pairwise2.align.globalms(species_gene1, species_gene2, 1, -1, -2, -2)
                # print(alignment[0][0])
                # print(alignment[0][1])
                distance = count_distance(alignment[0][0], alignment[0][1])
                row.append(distance)
            mtrx.append(row)
            gene_matrices[key].append(row)
        # print(key, mtrx)
        # gene_matrices[key].append(mtrx)

    gene_matrices = dict(gene_matrices)
    return gene_matrices


def count_distance(str1: str, str2: str) ->float:
    ''' Returns the distance between two strings,
    corrected according to Juke-Cantor model.
    http://readiab.org/book/0.1.3/2/4 '''

    res = 0

    # Hamming distance
    i = 0
    if len(str1) != len(str2):
        raise Exception('Compared strings must be the same length!')
    for position in str1:
        if position != str2[i]:
            res += 1
        i += 1

    # Jukes-Cantor correction
    res = res/len(str1)

    # Jukes-Cantor (JC69)
    res = -3/4 * np.log(1 - 4/3 * res)
    return res


def show_dendrograme(distance_matrices: dict) ->None:
    for key in distance_matrices:
        # print(distance_matrices[key])
        upgma = linkage(distance_matrices[key], 'average')
        fig = plt.figure(figsize=(12, 4))
        dn = dendrogram(upgma)
        plt.title(key)
        plt.show()


genes = read_file('genes.txt')

distances = distance_matrices(genes)
for key in distances:
    print(key)
    print(distances[key])
    print("-----------")

show_dendrograme(distances)


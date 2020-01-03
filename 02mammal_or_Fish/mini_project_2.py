from typing import List, Dict
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from matplotlib import pyplot as plt
from collections import defaultdict
from Bio import pairwise2
from Bio.pairwise2 import format_alignment

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
# # dn = dendrogram(Z)
# print("average: ", Z)


# alignments = pairwise2.align.globalms("ACCGT", "ACG", 1, -1, -2, 0) # Last one: -2? -1? 0? 1?
# print(type(format_alignment(*alignments[0])))
# print(alignments[0][2])

def distance_matrices(genes: Dict) -> Dict: #Dict[List[List[int]]]
    for key in genes:
        print(key)
        gene_matrices = defaultdict(list)
        i=0
        matrix = []
        for species in genes[key]:
            species_gene1 = species[-1]
            # print("..............")
            # print(species_gene1)
            # print("lolll")
            row = []
            for species in genes[key]:
                i+=1
                species_gene2 = species[-1]
                # print(species_gene2)
                alignment = pairwise2.align.globalms(species_gene1, species_gene2, 1, -1, -2, -2) # Last one: -2? -1? 0? 1?
                row.append([alignment[0][2]])
                # print(i)
            matrix.append(row)
            # print(row)
        # print(key, matrix)
        gene_matrices[key] = matrix

    return gene_matrices

''' displaying distance matrix'''

# from Bio.Phylo.TreeConstruction import _Matrix
# names = ['Alpha', 'Beta', 'Gamma', 'Delta']
# matrix = [[0], [1, 0], [2, 3, 0], [4, 5, 6, 0]]
# m = _Matrix(names, matrix)
#
# _Matrix(names=['Alpha', 'Beta', 'Gamma', 'Delta'], matrix=[[0], [1, 0], [2, 3, 0], [4, 5, 6, 0]])
# print(m)

''' '''
genes = read_file('genes.txt')

distances = distance_matrices(genes)

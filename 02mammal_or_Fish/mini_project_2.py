# from scipy.cluster.hierarchy import dendrogram, linkage
# import numpy as np
# from Bio import pairwise2
# from Bio.pairwise2 import format_alignment
#
# alignments = pairwise2.align.globalms("ACCGT", "ACG", 1, -1, -2, 0)
# print(format_alignment(*alignments[0]))

from typing import List, Dict
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
from collections import defaultdict

def read_file(path: str) -> Dict:
    with open(path, 'r') as file:
        genes = defaultdict(list)
        temp_gene_name = ""
        for i, line in enumerate(file):
            print(i)
            if (i + 1) % 8 == 1:
                temp_gene_name = line
                print(line)
            else:
                # print(line)
                values = line.split("\t")
                genes[temp_gene_name].append(values)
    return genes

# X = [[i] for i in [2, 8, 0, 4, 1, 9, 9, 0]]
Y = [[2, 3], [8, 4], [0, 4], [4, 5], [1, 6], [9, 9], [9, 1], [0, 0]]
print(type(Y))
print("Y ", Y)

Z = linkage(Y, 'average')
fig = plt.figure(figsize=(25, 10))
# dn = dendrogram(Z)
print("average: ", Z)

genes = read_file('genes.txt')
print(genes)
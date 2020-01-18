"""
Mini project #3:
---------------

The project is focused on finding the minimum length k of k-mers for which it is possible to obtain unique cyclic genome.
Implementation of a whole method for constructing Hamiltionian cycle which recovers the genome wasn't necessary.

Good source of knowledge: https://www.youtube.com/watch?v=0JlUy_l-RTk&t=2s
"""

from typing import Dict, List, Tuple
from collections import defaultdict

def read_file(path: str) -> Dict:
    """ Reading genes from a file into a dictionary
    in which keys represent a genome name,
    and a values - the genomes. """
    genomes = dict()
    dict_hlpr = ""
    with open(path, 'r') as file:
        for line in file:
            if line.startswith(">"):
                dict_hlpr = line[2:-1]
                # print(dict_hlpr)
            else:
                genomes[dict_hlpr] = line[:-1]
                # print(line[:-1])

    return(genomes)


def composition(genomes: str, k_len: int) -> List[str]:
    """
    Takes a circular genes and divide it for all possible k-mers (fragments) of a size of "k-mer" parameter
    and returns a list of k-mers that "wrap around" the end.

    For example:
        in: composition(“ATACGGTC”, 3)
        out: [“ATA”, “TAC”, “ACG”, “CGG”, “GGT”, “GTC”, “TCA”, “CAT”]

    :param gene: gene for reconstruction
    :param k_len: size of each divided kmer (fragment)
    :return fragments: list of kmers """

    fragments = list()
    length = len(genomes)

    hlpr = ""
    for i in range(length):
        hlpr = genomes[i : i+k_len]
        len2 = len(hlpr)
        if len2 < k_len:
            hlpr = hlpr + genomes[: k_len-len2]
        fragments.append(hlpr)

    # print(fragments)
    return(fragments)


def suffix_prefix(kmers: List[str]) ->Tuple[Dict, int]:
    """
    Returns a prefix and a suffix of each k-mer from the list.

    :param kmers: A list of error-free DNA k-mers taken from the strand of circular chromosome
    :return result: A dictionary of prefixes and suffixes for each kmer: result[prefix] = suffix
    """

    # Quick result: at the end, check if the len(result) is the same as len(kmers)\
    # if yes - the circular genome won't be ambiguous (will be unique)

    kmer_len = len(kmers)
    ambiguous = 1
    unique = 0 # assembled genome will be ambiguous

    result = defaultdict(list)
    for kmer in kmers:
        prefix = kmer[:-1]
        suffix = kmer[1:]
        print(prefix)
        print(suffix)
        result[suffix].append(prefix)
        print("suffix:", suffix, "prefiks: ", result[suffix])
        print("__________")
    result = dict(result)
    result_len = len(result)
    if kmer_len == result_len:
        print("The number of kmers and distinctive prefixes are the same, so circular gene will be unique!")
        unique = 1

    print("o tutej:", result)
    return(result, unique)


def is_ambiguous(pref_suf: Dict) -> List[str]:
    """
    Checks if the circular genome assembled with these mers will be unique.

    :param pref_suf: A dictionary that contains suffixes of kmers and prefixes which correspond them: pref_suf[suffix] = prefixes
    :return: list of dictinctive prefixes or suffixes (kmers)
    """
    # check if in lists of prefixes that correspond to each suffix contains the same prefixes \
    # if yes - leave only one of them and print the message about how many was removed
    # check how many prefixes is in each list
    # if each list of prefixes still consist of more than one element - assembled genome will be ambiguous for sure

    suffixes = list()
    for key in pref_suf:
        suffixes.append(pref_suf[key])
        print(key, ":", pref_suf[key])
    print(len(suffixes))

    for key in pref_suf:
        ile = suffixes.count(key)
        print(key, "ile: ", ile)

    # for key, value in pref_suf.items():
    #     if key not in result:
    #         result.append(key)
    #     if value not in result:
    #         result.append(value)
    # print(result)

    # return(result)

def simple_reconstruction(kmers: List[str]) ->str: #->List[str]:
    """
    Reconstruction of a circular string from a k-mers using de Bruijn graph.
    http://rosalind.info/problems/grep/

    For example:
        circular string assembled from the cycle "AC" -> "CT" -> "TA" -> "AC" is simply (ACT)
    :param kmers: A list of error-free DNA (k+1) mers taken from the strand of circular chromosome
    :return result: one of the circular strings assembled by complete cycles in the Bruijn graph. """

    result = ""
    i = 0
    for kmer in kmers:
        if i == 0:
            result = kmer
        elif i < len(kmers) - len(kmer) + 1:
            result += kmer[-1]
        i += 1

    # print(result)
    return(result)


def main():
    genes = read_file("genomes.txt")
    kmers = composition('ATACGGTC', 3)
    simple_reconstruction(kmers)
    pref_suf, is_unique = suffix_prefix(kmers)
    example_prefixes_suf, is_unique = suffix_prefix(["CAG", "AGT", "GTT", "TTT", "TTG", "TGG", "GGC", "GCG", "CGT", "GTT", "TTC", "TCA", "CAA", "AAT", "ATT", "TTC", "TCA"])
    # example_distinctive = is_ambiguous(example_prefixes_suf)
    # distinctive(pref_suf)

    # if is_unique == 1: gene will be unique, break;

if __name__ == "__main__":
    main()
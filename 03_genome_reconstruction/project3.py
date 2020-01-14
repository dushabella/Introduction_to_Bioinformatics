from typing import Dict, List

def read_file(path: str) -> Dict:
    """ Reading genes from a file into a dictionary
    in which the keys represent a gene type,
    and the values - the genes. """
    genes = dict()
    dict_hlpr = ""
    with open(path, 'r') as file:
        for line in file:
            if line.startswith(">"):
                dict_hlpr = line[2:-1]
                # print(dict_hlpr)
            else:
                genes[dict_hlpr] = line[:-1]
                # print(line[:-1])

    return(genes)


def composition(gene: str, k_len: int) -> List[str]:
    """
    Takes a circular genes and divide it for all possible kmers (fragments) of a size of "kmer" parameter
    and returns a list of k-mers that "wrap around" the end.

    For example:
        in: composition(“ATACGGTC”, 3)
        out: [“ATA”, “TAC”, “ACG”, “CGG”, “GGT”, “GTC”, “TCA”, “CAT”]

    :param gene: gene for reconstruction
    :param k_len: size of each divided kmer (fragment)
    :return fragments: list of kmers """

    fragments = list()
    length = len(gene)

    hlpr = ""
    for i in range(length):
        hlpr = gene[i : i+k_len]
        len2 = len(hlpr)
        if len2 < k_len:
            hlpr = hlpr + gene[: k_len-len2]
        fragments.append(hlpr)

    print(fragments)
    return(fragments)

def deBruijn(kmers: List[str]) ->str: #->List[str]:
    """
    Reconstruction of a circular string from a k-mers using de Bruijn graph.
    For example:
        circular string assembled from the cycle "AC" -> "CT" -> "TA" -> "AC" is simply (ACT)
    :param kmers: A list of error-free DNA (k+1) mers taken from the strand of circular chromosome
    :return result: All circular strings assembled by complete cycles in the Bruijn graph. """

    hlpr = ""
    i = 0
    for kmer in kmers:
        if i == 0:
            hlpr = kmer
        elif i < len(kmers) - len(kmer) + 1:
            hlpr += kmer[-1]
        i += 1

    print(hlpr)
    return(hlpr)

def prefix_suffix(kmers: List[str]) ->Dict:
    """
    Returns a prefix and a suffix of each kmer from the list
    For example:
        circular string assembled from the cycle "AC" -> "CT" -> "TA" -> "AC" is simply (ACT)
    :param kmers: A list of error-free DNA k-mers taken from the strand of circular chromosome
    :return result: A dictionary of prefixes and suffixes for each kmer: result[prefix] = suffix
    """
    result = dict()
    hlpr = ""
    i = 0
    for kmer in kmers:
        prefix = kmer[:-1]
        suffix = kmer[1:]
        print(prefix)
        print(suffix)
        print("__________")
        result[prefix] = suffix

    return(result)

def distinctive(pref_suf: Dict) -> List[str]:
    """
    Creates a list of distinctive (unique) prefixes/suffixes
    :param pref_suf: A dictionary that contains prefixes and suffixex of kmers
    :return: list of dictinctive prefixes or suffixes (kmers)
    """

    result = list()
    for key, value in pref_suf.items():
        if key not in result:
            result.append(key)
        if value not in result:
            result.append(value)
    print(result)

    return(result)

def main():
    genes = read_file("genomes.txt")
    kmers = composition('ATACGGTC', 3)
    deBruijn(kmers)
    pref_suf = prefix_suffix(kmers)
    distinctive(pref_suf)

if __name__ == "__main__":
    main()
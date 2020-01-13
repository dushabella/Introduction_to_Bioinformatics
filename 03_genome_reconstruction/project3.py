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

def composition(gene: str, kmer: int) -> List[str]:
    """
    Takes a circular genes and divide it for all possible kmers (fragments) of a size of "kmer" parameter
    and returns a list of k-mers that "wrap around" the end.

    For example:
        composition(“ATACGGTC”, 3)
        returns: [“ATA”, “TAC”, “ACG”, “CGG”, “GGT”, “GTC”, “TCA”, “CAT”]

    :param gene: gene for reconstruction
    :param kmer: size of each divided kmer (fragment)
    :return fragments: list of kmers """

    fragments = list()
    length = len(gene)

    hlpr = ""
    for i in range(length):
        hlpr = gene[i : i+kmer]
        len2 = len(hlpr)
        if len2 < kmer:
            hlpr = hlpr + gene[: kmer-len2]
        print(hlpr)

    return(fragments)


def main():
    genes = read_file("genomes.txt")
    composition('ATACGGTC', 3)

if __name__ == "__main__":
    main()
""" A program to find the anagrams of a given word in a given word list.

The program prints each anagram of the given word as well as the anagrams
of each subset of letters that can be formed from the letters of the word.
The given word is not considered an anagram of itself. The complexity of the program
is O((2^l)*n), where l is the length of the input word and n is the length of the word list.
If you assume a fixed word list, then the complexity is O(2^l)

How to use the program (in a command line):

    python3 jumble_solver.py <list_of_words> <word_of_interest>

Example:

    python3 jumble_solver.py words.txt dog
"""

import sys

def read_word_list(file_name):
    """Reads the word list from the specified file and returns it as a list of words.
    Arg:
        file_name: A string, which represents the name of a file
    Returns:
        A list of the content of each line of the given file, where each line is
        expected to be a single word
    """
    with open(file_name, 'r') as file:
        # Read all lines and strip any surrounding whitespace
        words = [line.strip() for line in file.readlines()]
    return words


def word_to_letters(word: str) -> list[str]:
    """ Converts letters in a word to lower case and returns them in a list.

    Arg:
        word: A string, which will be a single word
    Returns:
        A list of the letters in a word, all lowercase
    """
    word = word.lower() # convert the word to lower case
    lst = list(word)
    return lst

def find_sub_versions(letters: list[str]) -> list[list[str]]:
    """Finds all subsets of a given list of chars.

    Args:
        letters: A list of all the characters of a word
    Returns:
        A list of lists of char, each containing a subset of chars from the
        original list. Will include duplicates and the original list. Will not include
        single letters other than 'a' and 'i'.
    """
    # make sure letter sets of length 1 can represent actual words
    if len(letters) == 1:
        if letters[0] == 'a' or letters[0] == 'i':
            return letters
        else:
            return []
    # include the base set of letters as a sub version in a list
    sub_versions: list[list[str]] = [letters]

    # gather each subset of letters possible with one letter from the original list removed
    for i in range(len(letters)):
        temp: list[list[str]] = letters[:i] + letters[i+1:]
        sub_versions += find_sub_versions(temp)
    return sub_versions


def find_sorted_sub_versions(word: str) -> list[list[str]]:
    """Finds every subset of letters contained in a given word.

    Arg:
        word: A string, which will be a single word
    Returns:
        A list of lists of chars with the unique sets of chars contained in the
        original word. Each list of chars will be unique and sorted. Will not include
        lists with a single letter other than 'a' or 'i'.
    """
    # break the word into its letters
    letters: list[str] = word_to_letters(word)

    # find each subversion of letters possible in the word
    sub_versions: list[list[str]] = find_sub_versions(letters)

    sorted_sub_versions: list[list[str]] = []

    # sort each set of letters
    for version in sub_versions:
        sorted_version = sorted(version)
        sorted_sub_versions.append(sorted_version)

    unique_sub_versions: list[list[str]] = []

    # remove duplicate sets of letters
    for version in sorted_sub_versions:
        if version not in unique_sub_versions:
            unique_sub_versions.append(version)

    return unique_sub_versions


def separate_words_by_len(words: list, n: int) -> dict[int, dict[str, list[str]]]:
    """Groups words from a given list by length.

    Only groups words shorter than n. Groups words of each length into a
    dictionary with the strings as keys and lists of letters as values. Returns a dictionary
    with word length as keys and the dictionaries of words and sorted letters as values.

    Args:
        words: a list of strings, each of which will be a word
        n: an int which is the maximum length of string to include in the output
    Returns:
        A dictionary mapping word length to a dictionary mapping strings of that word length
        to their letters (sorted). For example:
        {1: {'a': ['a'], 'i': ['i']},
         2: {'to': ['o','t'], 'it': ['i','t']},
         3: {'the': ['e', 'h', 't'], 'got': ['g','o', 't']}
         }
    """
    words_by_length: dict[int, dict[str, list[str]]] = {}

    # create a dictionary for each word length up to n
    for i in range(1, n+1):
        words_by_length[i] = {}

    # populate each length-specific dictionary with the words of that length (and their letters)
    for word in words:
        word = word.lower()
        word_length = len(word)

        # only include words with length less than or equal to the given value
        if 0 < word_length <= n:
            words_by_length[word_length][word] = sorted(word)

    return words_by_length


def letters_match(subversion: list[str], prospect: list[str]) -> bool:
    """Determines if two lists of chars are equal"""
    return subversion == prospect

def find_anagrams(
        subversion: list[str],
        words: dict[str, list[str]],
        orig_word: str
) -> list[str]:
    """Finds the anagrams of a given list of letters.

    Args:
        subversion: A list of strings, which are the subsets of letters in a word of a certain length
        words: A dictionary with words (strings) as keys and a sorted list of the word's letters as values
    Returns:
         A list of the anagrams of subversion
    """
    anagrams: list[str] = []

    # check if each word of a certain length is an anagram of the given letters
    for word,letters in words:
        if letters_match(subversion, letters):
            if word != orig_word: # ensure the anagram is not the original word
                anagrams.append(word)

    return anagrams

def find_all_anagrams(
        sorted_sub_versions: list[list[str]],
        words_by_len: dict[int, dict[str, list[str]]],
        orig_word: str,
) -> list[str]:
    """Finds the anagrams of a given list of lists of letters.

    Args:
        sorted_sub_versions: A list containing subsets of letter of a word, as sorted lists
        words_by_len: A dictionary mapping word length to a dictionary mapping strings of that word length
                      to their letters (sorted).
        orig_word: A string, word the find anagrams of
    Returns:
        A list of the anagrams of a word and each subset of letters within that word
    """
    all_anagrams: list[str] = []

    # find the anagrams of each given subset of letters
    for sub_version in sorted_sub_versions:
        n: int = len(sub_version)
        anagrams: list[str] = find_anagrams(sub_version, words_by_len[n].items(), orig_word)
        all_anagrams += anagrams

    return all_anagrams

def main():
    # ensure the user has provided the filename  and word as a command-line argument
    if len(sys.argv) != 3:
        print("Usage: python3 jumble_solver.py <word_list_file> <word>")
        sys.exit(1)  # Exit with error status

    # get the filename from the command line
    word_list_file = sys.argv[1]

    # read the word list from the file
    words = read_word_list(word_list_file)

    # get the word to search from the command line
    word = sys.argv[2]

    # get the length of the word
    n: int = len(word)

    # separate words by length
    words_by_length: dict[int, dict[str, list[str]]] = separate_words_by_len(words, n)

    # find all sub-versions of the given word
    sorted_sub_versions: list[list[str]] = find_sorted_sub_versions(word)

    # find the anagrams of each subversion of the original word
    anagrams: list[str] = find_all_anagrams(sorted_sub_versions, words_by_length, word)

    for anagram in anagrams:
        print(anagram)


if __name__ == "__main__":
    main()

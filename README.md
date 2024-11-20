# jumble_solver
Jumble Solver Program


Program Overview:

The program, jumble_solver.py, finds the anagrams of a given word in a given word list as well as the anagrams
of each subset of letters that can be formed from the letters of the word.
The program prints each anagram. The program will not print the given word, since a word is not an anagram of itself. Note: If the program is used with words.txt, the program will output many anagrams that are not 'common' words , since words.txt contains many acronyms. For example, if you ask for the acronyms of dog, you will get commons words (god, do, and go) as well as uncommon words (og, dg, gd, and od). 

Description of Program Function:

The program finds anagrams by comparing the letters of subsets
of the given word to the letters of words in the word list. To perform this comparison,
the program uses the following steps and functions:

The program first converts the given word file to a list of words using the function read_word_list. The program
then calls the function separate_words_by_len to group the words by length. separate_words_by_len returns a dictionary with
ints as values, which represent word length, and dictionaries as the values. These nested dictionaries contains words as values and a sorted list of each word's letters as values. Grouping the words by length allows a subset of letters from the given word to only be compared to words with the same number of letters, reducing runtime. Additionally, the program assesses if two words are anagrams by comparing sorted lists of their letters, so it is beneficial to have each word and its sorted letters stored together. The variable words_by_length holds the output of separate_words_by_len.

The program finds the unique subsets of letters within the given word by calling the function find_sorted_sub_versions. find_sorted_sub_versions calls word_to_letters to break the word into a list of its letters, calls find_sub_versions to gather each combination of letters within the word, sorts each combination, removes any duplicate lists, and then returns the list of unique, sorted lists of letters. There are 2^L - 1 unique, unsorted subsets of letters within a word, where L is the length of the word. However, find_sorted_sub_versions will always return fewer than 2^L - l, since sorting removes subsets with the same characters in different orders and since find_sub_versions only returns 1-letter subsets that can be real words (i.e. a and i). The unique list of lists of letters is stored in the variable sorted_sub_versions. 

To find each of the anagrams of the given word, the program calls find_all_anagrams, which takes words_by_length, sorted_sub_versions, and the given word as inputs. For each subversion, the function calls another function, find_anagrams, to find the anagrams of that subversion. find_all_anagrams then aggregates and returns all of the anagrams. 

The function find_anagrams takes a single sub_version, the dictionary of words of matching length, and the original word as inputs. For each word in the input dictionary, the function calls another function, letters_match, to compare the letters of the subversion to the letters of the word. If the letters match, and the word is not the orignally-given word (a word is not an anagram of itself), the word is appended to a list, anagrams. Once each word has been evaluated, the function returns anagrams. 

Complexity Analysis:

The runtime of the program will be O(2^L*n), where L is the length of the given word and n is the length of the word list. If we assume we will always use the same word list, then the complexity can be simplified to O(2^L). The function find_all_anagrams dictates this O() value. The loop within the function runs once for each subversion of the given word, and the number of subversions will be a function of 2^L (as discussed above). Each loop iteration runs in O(n), since the subversion must be compared to a portion of the entire word list. 

If we assume that the only word list we will use is word_list.txt, and we only look for the anagrams of words of 8 letters or less, the complexity becomes O(2^(2L)). This is because as word length, m, increases, the number of words of length m increases exponentially while m <= 8. When m > 8, the number of words per length platues and then decreases exponentially.



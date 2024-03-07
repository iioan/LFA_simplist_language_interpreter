# Lexical Analyzer Algorithm

This README describes the detailed implementation of a Lexical Analyzer Algorithm.

## Overview

The Lexical Analyzer algorithm is constructed as follows:

### Initialization

The algorithm starts by taking an array of tuples `spec`, where each tuple consists of a string representing the name of the token, and a regular expression. For each tuple, it creates a corresponding DFA (Deterministic Finite Automaton) using Thompson's Construction and Subset Construction algorithms, and stores these DFA's along with their respective names in the class specification.

### Tokenization

The algorithm then tokenizes an input string `word` as follows:

1. It initializes an empty `tokens` list to store the resulting tokens, a `line` variable representing the current line number, and two index variables (`princ_index` and `sec_index`) that keep track of the position in the string.
2. While the string `word` is not empty, it does the following:
    
    a. If the first character of `word` is a newline, it increments `line`, resets `princ_index` to -1 (since it will be incremented when processing the newline), and updates `word_copy` to be `word[1:]`.
    
    b. It initializes an empty `accepted_tokens` list to store tokens that have been accepted by the DFA's, and two variables `len_longest` and `sec_index` to keep track of the length of the longest accepted substring and a secondary index, respectively.
    
    c. While `len_longest` is less than the length of `word`, it does the following:
    
    i. It sets `longest` to be the substring of `word` of length `len_longest + 1`.
    
    ii. For each DFA in the class specification, it checks if the DFA can possibly accept `longest`. If it can and does accept `longest`, it adds the tuple `(index, longest)` to `accepted_tokens`. If it can't, it increments a counter `who_rejected`.
    
    iii. If all DFA's have rejected `longest`, it breaks out of the loop. Otherwise, it increments `sec_index` and `len_longest`.
    
    d. If `accepted_tokens` is not empty, it does the following:
    
    i. It sorts `accepted_tokens` in decreasing order of the length of the accepted substrings, and in case of a tie, in increasing order of the index of the tuples in the class spec.
    
    ii. It adds the tuple `(wanted_spec_name, longest_seq)` to `tokens`, where `wanted_spec_name` is the name of the DFA that accepted the longest substring, and `longest_seq` is the longest substring.
    
    iii. It updates `word` to be the substring of `word` starting from `len(longest_seq)`, and increments `princ_index` by `len(longest_seq)`.
    
3. If the sum of `princ_index` and `sec_index` is equal to the length of `word_copy`, it returns an error indicating that it has reached EOF (End-Of-File). Otherwise, it returns an error indicating that there is no viable alternative at the character position `princ_index + sec_index` on line `line`.
4. Finally, it returns `tokens`.

## Conclusion

The Lexical Analyzer algorithm is an efficient and effective method for tokenizing an input string based on a given set of regular expressions. It can be used for a variety of applications such as lexical analysis in compilers, text parsing, and more.
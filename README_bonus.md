## Lisp-inspired Language Interpreter 

This document outlines a high-level explanation of a Lambda Calculus Interpreter algorithm in Python. This algorithm takes a file as an argument, reads the lines, and then closes the file. The lines are then combined using `''.join(lines)`.

## Lexer Specification

The lexer specification is as follows:

1. Parentheses `()`
2. Open parenthesis
3. Closed parenthesis
4. Space
5. Newline
6. Tab
7. Number
8. Plus (`+`)
9. Concatenation (`++`)
10. Lambda
11. Colon
12. IDs (letters)

The lexer returns a list of all found tokens. Each element in the list is in the form `(TOKEN_TYPE or regex_name, described string of characters)`. If the type of the first element is `''`, then an error is returned and the program exits. The list is then passed to the `check_parenthesis` function, which verifies the correct closing of parentheses.

## Check Parentheses Function

The `check_parentheses` function verifies the correct closing of parentheses. If the stack is not empty, this means that parentheses have not been distributed correctly. Therefore, an error will be returned at the point of the problem (which parenthesis was not closed) and the program will exit.

## Parse Function

The `parse` function parses the expression. The parsed list replaces parentheses with lists (except for `()`, which is an empty list).

## Compute Function

The `compute` function computes the expression.

The list of tokens is passed through, and if the type of the token is a list, it is treated separately. If the last operation on the sublist is not a lambda, it is added to the result list. If the last operation on the sublist is a lambda, the element is removed from the `tokens` and the result of the computation is added back into the `tokens`.

## Compute Functions by Operation Type

There are specific functions to compute the result based on the type of operation. These include `compute_sum()`, `compute_cc()`, and `compute_lambda()`.

### Compute Sum Function

The `compute_sum()` function runs through the entire list of tokens and computes the sum for each element that is a number.

### Compute CC Function

The `compute_cc()` function iterates over the list of tokens and concatenates the elements that are numbers.

### Compute Lambda Function

The `compute_lambda()` function is the most important part of the algorithm. It returns the body of the function if `not_replaceable` is true. Otherwise, the result is calculated in `solve_lambda()`.

The `solve_lambda()` function iterates over the body of the expression and replaces the argument with the value where applicable.

## Final Steps

The final result is printed to the console. If parentheses are necessary, they are added to the result.

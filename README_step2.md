## Regular Expression to Non-deterministic Finite Automaton (NFA) Conversion Algorithm

This guide provides an in-depth explanation of the algorithm that converts regular expressions into non-deterministic finite automata.

## Overview

The algorithm starts at the `parse_regex` function, which calls `build_tree`. The `Regex` class has several attributes: `left`, `right`, which are the leaves of the central node `data`. Each node has an NFA. The node belongs to a subclass depending on the type of `data`.

**`build_tree`**

The purpose of the stack is to store the tree/nodes/possible sub-trees. In the end, the final tree is at `stack.pop()`.

The `quantifiers` list contains elements that quantify the appearance of characters in the regex, while the `ignore` list includes spaces and closed parentheses. The `last_operation` variable represents the last node/sub-tree added to the final tree.

The regex is traversed to transform it into a tree. Everything happens within `while i < len(regex):`.

**`insert_union`**

A new node is created with | in the center and, on the left, the tree processed so far.

**`insert_quantifier`**

The processed tree so far is taken, and the quantifier is put in front of it, with the help of the `find_add` function.

**`find_add`**

If self is what is desired (here, the addresses of the node instances are considered), i.e., the root of the tree to be changed, then a new instance is created for self's data. Then, the new root, `new_node`, is created, which will have as data the desired quantifier, and on the left is what it will quantify. The necessary data is put in self, the class, data, left, right, and everything is returned.

**`insert_regex`**

In this function, the regex within parentheses is processed. If something is in the stack, it will be checked if the previous character is `UNION`. In that case, the root from the stack is taken, and on its right is the just-processed regex. If `UNION` does not exist, it means that the implementation must simply continue, so the concatenation of the two parts is done.

**`generate_expression`**

Several cases exist for generating the expression. If the character is a syntactic sugar of the form `[something]`, the closing bracket ] is searched for, and the expression is precisely that.

**`insert_expression`**

The state of the stack is checked, and if the root equals `UNION`, the expression is added accordingly. Otherwise, the stack contains an expression, and concatenation between the two is performed.

## The Regex Class

Depending on what the data is, there are inheriting classes of Regex:

- For star → KleeneStar
- For ? → QuestionMark
- For + → Plus
- For | → Union
- For cc → Concat
- For when data[0] is [ → SyntacticSugar
- Otherwise → Character

Each class inherits the Thompson method!

## The Character Class

A new NFA is created with just two states and one transition.

## The Concatenation Class

The left and right NFAs are recursively computed. The states are remapped to avoid conflicts, and then a new NFA is created, with the initial state equal to the left NFA's and the final state equal to the right NFA's.

## The Union Class

The left and right NFAs are computed, remapped, and merged. Epsilon transitions are created from the new initial state to the old initial states and from the old final states to the new final state.

## The KleeneStar Class

The left NFA is computed and remapped. The new initial and final states are added, and epsilon transitions are created to allow looping over the old NFA.

## The QuestionMark Class

This class works similarly to the KleeneStar class, but the transition from the old final state to the old initial state is removed, as the old NFA should be traversed at most once.

## The Plus Class

This class works similarly to the KleeneStar class, but the transition from the new initial state to the new final state is removed, as the old NFA should be traversed at least once.

## The SyntacticSugar Class

The values within the brackets are processed and converted to their corresponding ASCII values. Transitions are created for each character in the alphabet.

---

This is just a brief overview of the described algorithm. For more in-depth understanding, please refer to the provided code and comments.
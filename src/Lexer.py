from .Regex import Regex, parse_regex
from .DFA import DFA
from .NFA import NFA


class Lexer:
    def __init__(self, spec: list[tuple[str, str]]) -> None:
        self.spec = []
        for (name, regex) in spec:
            DFA_regex = parse_regex(regex).thompson().subset_construction()
            self.spec.append((name, DFA_regex))

    def lex(self, word: str) -> list[tuple[str, str]] | None:
        tokens = []
        word_copy = word
        line = 0
        princ_index = 0

        while len(word) > 0:
            if word[0] == '\n':
                line += 1
                princ_index = -1  # se va aduna 1 cand procesam subsirul '\n'
                word_copy = word[1:]

            accepted_tokens = []
            len_longest = 0
            sec_index = 0

            while len_longest < len(word):
                longest = word[0: len_longest + 1]
                who_rejected = 0
                for ((name, AFD), index) in zip(self.spec, range(len(self.spec))):
                    # verificam posibilitatea DFA-urilor pentru a accepta o parte din subsir
                    if AFD.possible(longest):
                        # daca e posibila acceptarea, verificam daca nu chiar accepta subsirul
                        if AFD.accept(longest):
                            # daca da, se adauga in accepted_tokens
                            accepted_tokens.append((index, longest))
                    else:
                        who_rejected += 1
                # daca toate automatele resping subsirul, iesim (nu mai are rost sa cautam subsirul)
                if who_rejected == len(self.spec):
                    break
                else:
                    # index-ul caracterului la care ne aflam in mom de fata
                    sec_index += 1

                len_longest += 1

            if accepted_tokens:
                # sortam descrescator in func de lungimea subsirului; in caz de =, ordonam crescator in +
                # + func de index-ul elementelor din specificatie (are prioritate cel mai apropiat de 0)
                accepted_tokens = sorted(accepted_tokens, key=lambda x: (-len(x[1]), x[0]))
                # accepted_tokens[0] -> tuplul dorit (are cel mai lung subsir + tine cont de ordinea din spec)
                # accepted_tokens[0][0] -> index-ul dorit pentru a accesa token-ul din spec
                # self.spec[accepted_tokens[0][0]] -> tuplu cu token-ul final din spec
                # self.spec[accepted_tokens[0][0]][0] -> token final
                wanted_spec_name = self.spec[accepted_tokens[0][0]][0]

                # accepted_tokens[0][1] -> cel mai lung subsir
                longest_seq = accepted_tokens[0][1]
                tokens.append((wanted_spec_name, longest_seq))
                word = word[len(longest_seq):]
                princ_index += len(longest_seq)
            else:
                # avem cuvant invalid
                # daca am ajuns la finalul lui word -> cuvant incomplet
                if princ_index + sec_index == len(word_copy):
                    return [("", f"No viable alternative at character EOF, line {line}")]
                # caracterul la care am ajuns este invalid si nu mai avem cum sa acceptam
                return [("", f"No viable alternative at character {princ_index + sec_index}, line {line}")]
        return tokens

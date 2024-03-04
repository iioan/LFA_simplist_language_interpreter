from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class DFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], STATE]
    F: set[STATE]

    def accept(self, word: str) -> bool:
        current_state = self.q0
        for i in word:
            for delta in self.d:
                c = delta[1].replace('\\', '') if delta[1] != '\n' else delta[1]
                if delta[0] == current_state and c == i and self.d[delta] != set():
                    current_state = self.d[delta]
                    word = word[1:]
                    break
        return current_state in self.F and not word

    def possible(self, word: str) -> bool:
        current_state = self.q0
        for i in word:
            for delta in self.d:
                c = delta[1].replace('\\', '') if delta[1] != '\n' else delta[1]
                if delta[0] == current_state and c == i and self.d[delta] != set():
                    current_state = self.d[delta]
                    word = word[1:]
                    break
        return not word

    def remap_states[OTHER_STATE](self, f: Callable[[STATE], 'OTHER_STATE']) -> 'DFA[OTHER_STATE]':
        self.K = {frozenset(f(x) for x in list(inner_frozenset)) for inner_frozenset in self.K}
        self.q0 = frozenset(f(x) for x in list(self.q0))
        remap_d = {}
        for delta in self.d:
            remap_d[(frozenset(f(x) for x in list(delta[0])), delta[1])] = (
                set(f(x) for x in self.d[delta]))
        self.d = remap_d
        self.F = {frozenset(f(x) for x in list(inner_frozenset)) for inner_frozenset in self.F}

from .DFA import DFA

from dataclasses import dataclass
from collections.abc import Callable

EPSILON = ''  # this is how epsilon is represented by the checker in the transition function of NFAs


@dataclass
class NFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], set[STATE]]
    F: set[STATE]

    def epsilon_closure_helper(self, state: STATE, visited: list) -> set[STATE]:
        S = {state}
        visited.append(state)
        next_states = self.d.get((state, EPSILON), set())
        for i in next_states:
            if i not in visited:
                # union = uneste unul sau mai multe set-uri intr-unul singur
                S = S.union(self.epsilon_closure_helper(i, visited))
        return S

    def epsilon_closure(self, state: STATE) -> set[STATE]:
        return self.epsilon_closure_helper(state, [])

    def subset_construction(self) -> DFA[frozenset[STATE]]:
        # memoreaza eps. tranzitiile fiecarei stari
        closures = {}
        for i in self.K:
            closures[i] = self.epsilon_closure(i)
        init_state = closures[self.q0]
        K = {frozenset(init_state)}
        d = {}
        F = set()
        if self.F.intersection(init_state):
            F.add(frozenset(init_state))
        verify_states = [init_state]
        # incepe algoritmul; iau o stare nevizitata
        while verify_states:
            curr_closure = verify_states.pop()
            for letter in self.S:
                # starea in care se poate ajunge din curr_closure pe litera respectiva
                next_states = set()
                for state in curr_closure:
                    next_states.update(self.d.get((state, letter), set()))
                # adaugam fiec epsilon closure din multimea next_states
                next_closure = set()
                for state in next_states:
                    next_closure.update(closures[state])
                # noul state al DFA-ul:
                new_state = frozenset(next_closure)
                if new_state not in K:
                    K.add(new_state)
                    verify_states.append(next_closure)
                if next_closure.intersection(self.F):
                    F.add(new_state)
                # adauga intrare in functia de transitie.
                d[(frozenset(curr_closure), letter)] = next_closure
        return DFA(self.S, K, frozenset(closures[self.q0]), d, F)

    def remap_states[OTHER_STATE](self, f: 'Callable[[STATE], OTHER_STATE]') -> 'NFA[OTHER_STATE]':
        self.K = set(f(x) for x in self.K)
        self.q0 = f(self.q0)
        remap_d = {}
        for delta in self.d:
            remap_d[(f(delta[0]), delta[1])] = set(f(x) for x in self.d[delta])
        self.d = remap_d
        self.F = set(f(x) for x in self.F)

from .NFA import NFA

EPSILON = ''


class Regex:
    # In functie de data, vom crea un nou obiect de tipul corespunzator
    def __new__(cls, data, left=None, right=None):
        if data == '*':
            return super().__new__(KleeneStar)
        if data == '?':
            return super().__new__(QuestionMark)
        if data == '+':
            return super().__new__(Plus)
        if data == '|':
            return super().__new__(Union)
        if data == 'cc':
            return super().__new__(Concatenation)
        if data[0] == '[':
            return super().__new__(SyntacticSugar)
        return super().__new__(Character)

    # Am decis ca Regex-ul sa fie reprezentat ca un arbore binar
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
        self.NFA = None

    def thompson(self) -> NFA[int]:
        pass

    # Cauta nodul 'wanted' si adauga in fata sa un nou nod cu data 'new_data'
    def find_add(self, wanted, new_data):
        if self == wanted:
            saved = Regex(self.data, self.left, self.right)
            new_node = Regex(new_data, saved)
            # Copiem atributele din new_node in self
            self.__class__ = new_node.__class__
            self.data = new_node.data
            self.left = new_node.left
            self.right = new_node.right
            return
        if self.left:
            self.left.find_add(wanted, new_data)
        if self.right:
            self.right.find_add(wanted, new_data)


class Character(Regex):
    # Pentru un caracter, vom crea un NFA cu 2 stari si o tranzitie intre ele
    def thompson(self) -> NFA[int]:
        d = {(0, self.data): {1}}
        self.NFA = NFA({self.data}, {0, 1}, 0, d, {1})
        return self.NFA


class Concatenation(Regex):
    # Pentru concatenare, luam NFA-urile din stg si dr si le combinam
    def thompson(self) -> NFA[int]:
        if self.left:
            left_NFA = self.left.thompson()
        if self.right:
            right_NFA = self.right.thompson()
        left_states_no = len(left_NFA.K)
        # Remapam starile din NFA-ul din dreapta pentru a nu avea conflicte
        right_NFA.remap_states(lambda x: x + left_states_no)

        S = left_NFA.S.union(right_NFA.S)
        K = left_NFA.K.union(right_NFA.K)
        d = left_NFA.d | right_NFA.d.copy()

        last_left_state = max(left_NFA.K)
        first_right_state = min(right_NFA.K)
        # Se ia starea finala din NFA-ul stang si se face un +
        # eps-transition catre starea initiala din NFA-ul drept
        d[(last_left_state, EPSILON)] = {first_right_state}

        self.NFA = NFA(S, K, left_NFA.q0, d, right_NFA.F)
        return self.NFA


class Union(Regex):
    # Pentru uniune luam NFA-urile din stg si dr si le combinam
    def thompson(self) -> NFA[int]:
        if self.left:
            left_NFA = self.left.thompson()
        if self.right:
            right_NFA = self.right.thompson()
        left_states_no = len(left_NFA.K)
        # Adunam cu 1 starile din NFA-ul stang (vrem sa adaugam o noua stare initiala)
        left_NFA.remap_states(lambda x: x + 1)
        # Remapam starile din NFA-ul din dreapta pentru a nu avea conflicte
        right_NFA.remap_states(lambda x: x + left_states_no + 1)

        S = left_NFA.S.union(right_NFA.S)
        K = left_NFA.K.union(right_NFA.K)
        qF = max(K)  # Starea finala va fi max(K)
        K = K.union({0, qF})
        F = {qF}
        d = left_NFA.d | right_NFA.d.copy()

        # Adaugam de la q0 (0) eps-tranzitii catre starile initiale din NFA-ul stang si drept
        first_left_state = left_NFA.q0
        first_right_state = right_NFA.q0
        d[(0, EPSILON)] = {first_left_state, first_right_state}
        # Adaugam de la ultimele stari din NFA-urile stang si drept eps-tranzitii catre qF
        last_left_state = max(left_NFA.F)
        last_right_state = max(right_NFA.F)
        d[(last_left_state, EPSILON)] = {qF}
        d[(last_right_state, EPSILON)] = {qF}

        self.NFA = NFA(S, K, 0, d, F)
        return self.NFA


class KleeneStar(Regex):
    # Pentru KleeneStar, luam NFA-ul din stg si il combinam cu el insusi
    def thompson(self) -> NFA[int]:
        if self.left:
            prev_NFA = self.left.thompson()

        states_no = len(prev_NFA.K)
        # Adunam cu 1 starile din NFA-ul stang (vrem sa adaugam o noua stare initiala)
        prev_NFA.remap_states(lambda x: x + 1)

        qF = states_no + 1  # noua stare finala
        init_state = prev_NFA.q0  # starea initiala a NFA-ului
        final_state = max(prev_NFA.F)  # starea finala a NFA-ului

        prev_NFA.K = prev_NFA.K.union({0, qF})
        # De la q0 (0) adaug eps-tranzitii catre starea initiala a NFA-ului si catre qF
        prev_NFA.d[(0, EPSILON)] = {init_state, qF}
        # De la ultima stare a NFA-ului adaug eps-tranzitii catre init_state si catre qF
        prev_NFA.d[(final_state, EPSILON)] = {init_state, qF}
        prev_NFA.F = {qF}  # noua stare finala
        prev_NFA.q0 = 0  # noua stare initiala

        self.NFA = prev_NFA
        return self.NFA


class QuestionMark(Regex):
    # Implementarea e asemantoare cu cea de la KleeneStar +
    # doar ca nu mai adaug eps-tranzitie de la ultima stare la prima stare (a NFA-ului)
    def thompson(self) -> NFA[int]:
        if self.left:
            prev_NFA = self.left.thompson()

        states_no = len(prev_NFA.K)
        # Adunam cu 1 starile din NFA (vrem sa adaugam o noua stare initiala)
        prev_NFA.remap_states(lambda x: x + 1)

        qF = states_no + 1  # noua stare finala
        init_state = prev_NFA.q0  # starea initiala a NFA-ului
        final_state = max(prev_NFA.F)  # starea finala a NFA-ului

        prev_NFA.K = prev_NFA.K.union({0, qF})
        # De la q0 (0) adaug eps-tranzitii catre starea initiala a NFA-ului si catre qF
        prev_NFA.d[(0, EPSILON)] = {init_state, qF}
        # De la ultima stare a NFA-ului adaug eps-tranzitii catre qF
        prev_NFA.d[(final_state, EPSILON)] = {qF}
        prev_NFA.F = {qF}
        prev_NFA.q0 = 0

        self.NFA = prev_NFA
        return self.NFA


class Plus(Regex):
    # Implementarea e asemantoare cu cea de la KleeneStar +
    # doar ca nu mai adaug eps-tranzitie q0 (0) la qF +
    # asta inseamna ca trebuie sa treaca cel mult o data prin NFA
    def thompson(self) -> NFA[int]:
        if self.left:
            prev_NFA = self.left.thompson()

        states_no = len(prev_NFA.K)
        prev_NFA.remap_states(lambda x: x + 1)

        qF = states_no + 1
        init_state = prev_NFA.q0
        final_state = max(prev_NFA.F)

        prev_NFA.K = prev_NFA.K.union({0, qF})
        prev_NFA.d[(0, EPSILON)] = {init_state}
        prev_NFA.d[(final_state, EPSILON)] = {init_state, qF}
        prev_NFA.F = {qF}
        prev_NFA.q0 = 0

        self.NFA = prev_NFA
        return self.NFA


class SyntacticSugar(Regex):
    def thompson(self) -> NFA[int]:
        # eliminam parantezele si luam cele doua limite din interior
        interval = self.data[1:-1]
        values = interval.split('-')
        # generam alfabetul; avem toate elementele din intervalul respectiv
        alphabet = [chr(i) for i in range(ord(values[0]), ord(values[1]) + 1)]
        # adaugam cate o tranzitie pentru fiecare caracter din alfabet
        d = {(0, i): {1} for i in alphabet}

        self.NFA = NFA(set(alphabet), {0, 1}, 0, d, {1})
        return self.NFA


# Adaugam un nod 'Union' peste ultimul root din stiva
def insert_union(stack):
    node = Regex('|', stack.pop())
    stack.append(node)
    return node


# Adaugam un quantifier in nodul / subarborele recent adaugat
def insert_quantifier(i, last_operation, regex, stack):
    node = stack.pop()
    # Adaugam in fata nodului quantifier-ul dorit
    node.find_add(last_operation, regex[i])
    stack.append(node)
    return node


# Cauta pozitia parantezei inchise coresp. parantezei deschise de la pozitia 'opening'
def find_closing_bracket(string, opening):
    stack = []
    for i in range(opening, len(string)):
        if string[i] == '(':
            stack.append('(')
        elif string[i] == ')':
            stack.pop()
        if not stack:
            return i
    return -1


# Am intalnit un regex in paranteze -> il parsam
def insert_regex(i, regex, stack):
    # (opening + 1: closing + 1) = 'sub'regex-ul pe care il parsam
    opening = i
    closing = find_closing_bracket(regex, opening)
    inside_regex = build_tree(regex[opening + 1: closing + 1])
    # Am pre-procesat ceva din regex-ul principal
    if stack:
        # Daca inainte de ( avem | -> adaugam subregex-ul in dreapta nodului | din stiva
        # Altfel, concatenam subregex-ul cu nodul din varful stivei
        if regex[i - 1] == '|':
            node = stack.pop()
            node.right = inside_regex
            stack.append(node)
        else:
            stack.append(Regex('cc', stack.pop(), inside_regex))
    else:
        stack.append(inside_regex)  # N-am pre-procesat nimic inca!
    # Returnam pozitia lui ')' (pentru a muta i-ul in build_tree) si subregex-ul parsat
    return closing, inside_regex


def generate_expression(i, regex):
    # generam un nou nodn cu expresia curenta
    # daca expresia incepe cu [ -> avem syntactic sugar
    # daca expresia incepe cu \ -> avem un caracter special cu escape
    # altfel, avem un caracter normal
    match regex[i]:
        case '[':
            closing = regex.find(']', i)
            expression = regex[i: closing + 1]
            i = closing
        case '\\':
            expression = '\\' + regex[i + 1]
            i += 1
        case _:
            expression = regex[i]
    # returnam noua pozitia a lui i si noul nod
    return i, Regex(expression)


# Adauga in arbore un nod cu expresia curenta
def insert_expression(new_node, prev_i, regex, stack):
    # Am pre-procesat ceva din regex-ul principal si root-ul este |
    if stack and stack[-1].data == '|':
        main_regex = stack.pop()
        # Daca in dreapta root-ului nu avem nimic, adaugam noul nod
        if main_regex.right is None:
            main_regex.right = new_node
        # Avem cv in dreapta; daca e o expresie (nu subregex), concatenam noul nod cu aceasta
        elif regex[prev_i - 1] != ')':
            main_regex.right = Regex('cc', main_regex.right, new_node)
        # Altfel, adaugam noul nod in dreapta root-ului
        else:
            main_regex = Regex('cc', main_regex, new_node)
        stack.append(main_regex)
    else:
        # Daca nu am pre-procesat nimic din regex-ul principal, adaugam noul nod in stiva
        # Altfel, concatenam noul nod cu nodul din varful stivei
        stack.append(Regex('cc', stack.pop(), new_node) if stack else new_node)
    return new_node


def build_tree(regex: str) -> Regex:
    # stiva mentine arborele / noduri / subarbori
    stack = []
    i = 0
    # cuantifica tot ce e inainte de acesta
    quantifiers = ('?', '*', '+')
    # ignora spatiile si parantezele inchise
    ignore = (' ', ')')
    # last_operation = ultimul nod / subarbore pe care l-am adaugat in arborele nostru
    last_operation = None

    # edge-case-uri pentru bonus: regex-ul e doar ( sau )
    if regex == '(' or regex == ')':
        return Regex(regex)
    # regex-ul e o lista vida
    if regex == '()':
        return Regex('cc', Regex('('), Regex(')'))

    while i < len(regex):
        # vom lua fiec. caracter din regex si il punem in arbore in functie de cazuri
        if regex[i] == '|':
            last_operation = insert_union(stack)
        elif regex[i] in quantifiers:
            last_operation = insert_quantifier(i, last_operation, regex, stack)
        elif regex[i] == '(':
            # avem in 'sub' regex in paranteze -> il parsam
            i, last_operation = insert_regex(i, regex, stack)
        else:
            if regex[i] in ignore:
                i += 1
                continue
            # pastram pozitia veche a lui i
            prev_i = i
            # generam un nou nod cu expresia curent
            i, new_node = generate_expression(i, regex)
            last_operation = insert_expression(new_node, prev_i, regex, stack)
        i += 1
    return stack.pop()  # Regex-ul final este ultimul element din stiva


def parse_regex(regex: str) -> Regex:
    return build_tree(regex)

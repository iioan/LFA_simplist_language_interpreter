## Step 1 LFA

### Ioan Teodorescu - 333CB

This stage consists of converting from NFA to DFA using the Subset Construction algorithm.

### NFA Class

For the non-deterministic finite automaton, we implemented the stage requirements as follows:

**`epsilon_closure`**

* Receives a state of the NFA and returns a set of states, which are the states that can be reached only through epsilon-transitions from the initial state (received as a parameter).

* Using the **states** that can be reached from the **initial state** through epsilon-transitions, these states in turn have states that can be reached through epsilon-transitions, and so on. Therefore, my implementation of this function is recursive, in order to obtain all possible states.

* To keep track of the states we have visited (to avoid infinite loops), we used the `visited` list, which adds a state to the beginning. To use the list, I created a helper function to keep track of the list.

* Initially, a set `S` is initialized with the identifier of the state being analyzed.

* `next_states` contains the states that `state` can reach without consuming anything from the word. We iterate through this set and check if there are any states that have not been visited yet. If so, we recursively call the function for that `state` and its output will be **unified** with the final set `S`. Finally, we return `S`.

**`subset_construction`**

* Receives an NFA and returns a DFA. To achieve this, the Subset Construction algorithm is used.

* At the beginning of the function, a dictionary `closures` is initialized which will have the epsilon-closure of each state of the NFA. Then, we initialize some of the fields of the DFA, namely `K`, `d`, `F` and `q0`. For `K` and `F`, `frozenset` is used for each state of the new DFA. We want to have a **set of sets**, but sets are not **hashable**. The solution would be that both for the set `K` (the states of the automaton) and for the set `F` (the final states), their inner sets should be of type **frozenset**, this type being always hashable. For `q0`, the epsilon-closure of the initial state of the NFA is used (which we also add as a state of the automaton and check if a subset of that set belongs to `F`). For `d`, an empty dictionary is initialized.

* To implement the algorithm, we use the list `verify_states`, representing the states that need to be analyzed. Initially, it contains only the epsilon-closure of the initial state. Then, in `while`, a state is extracted from the list.

* We will work with the current state `curr_closure`. For each letter in the alphabet of the automaton, `next_states` will be determined, which represents the states that can be reached from `curr_closure` by the respective letter. For each state in `next_states`, the epsilon-closure of each subset will be calculated, and this is the new state of the DFA (`new_state`) (in case it has not appeared before). If the **new state** is not in `K`, then it is added to it and to `verify_states`, so that it can also be analyzed. We also check if the **new state** is a final state (the intersection of the two sets is not an empty set). If so, then it is added to `F`.

* Finally, a new entry is added to `d` with the key tuple between `curr_closure` (from which we started) and the letter used, and the value is `new_state` (the state we reached).

* Finally, the DFA is returned.

**`remap_states`**

* Receives an NFA and returns the NFA with the states remapped.

* Using the `f` function, we modify the states of the automaton. For the sets `K` and `F`, the `map` function is used, which receives the function and the iterable (the old sets) as parameters. For the transition function, we initialize a new dictionary `d` and for each entry in the old transition function (dictionary), the `f` function is applied to the states before and after the transition. The NFA with the remapped states is returned.

### DFA Class

For the deterministic finite automaton, we implemented the stage requirements as follows:

**`accept`**

* Receives a word and returns True if the word is accepted by the automaton, False otherwise.

* We iterate through each letter in the word and each transition in the automaton. If we find a transition that has the current state (`current_state`) as the start state and the input is the current letter (`letter`), then the current state becomes the final state. We use break for avoiding transitions' traversal for the same letter and a different current state. 
* After finishing the word traversal, we check if the state we are in right now is a final state (belongs to self.F) and if the word has been consumed. If yes, we will return True, else, False. 


**`remap_states`**

* For this function, we assume that the received automaton has passed through the Subset Construction algorithm,
so its states are of type frozenset. To remap the states, each frozenset is taken, transformed into a list,
the function `f` is applied to each element in the list, using the `map` function, and it is transformed back into a frozenset.
The DFA with the remapped states is returned.



## Etapa 1 LFA 
Ioan Teodorescu - 333CB

Această etapa consta in conversia de la NFA la DFA, folosind algoritmul Subset Construction.
### Clasa NFA
Pentru automatul finit nedeterminist, am implementat cerintele etapei astfel:

`epsilon_closure` - Primeste o stare a NFA-ului si returneaza un set de stari, acestea fiind fix starile la care se poate 
ajunge doar prin epsilon-tranzitii de la starea initiala (e primita ca parametru).

Prin intermediul **starilor** cu care putem ajunge de la **starea initiala** prin epsilon-tranzitii, acestea la randul 
lor _au si ele stari_ prin care pot ajunge tot prin epsilon-tranzitii, si asa mai departe. De aceea, implementarea mea a 
acestei functii este una recursiva, pentru a obtine toate state-urile posibile. 

De asemenea, pentru a tine cont de starile pe care le-am vizitat (pentru a evita bucle infinite), am folosit lista `visited`, 
care adauga cate o stare la inceput. Pentru folosirea listei, mi-am creat o functie helper pentru a tine cont de lista. 
La inceput se initializeaza un set `S` cu identificatorul starii pe care o analizam.
In `next_states` se afla starile in care `state` poate ajunge fara a consuma ceva din cuvant. Parcurgem acest set si 
verificam daca avem stari ce nu au fost vizitate inca. Daca da, reapelam functia pentru acel `state` si output-ul acesteia
se va **unifica** cu setul final `S`. La final, returnam `S`.

`subset_construction` - Primeste un NFA si returneaza un DFA. Pentru a realiza acest lucru, se folosteste algoritmul Subset 
Construction.

La inceputul functiei, se initializeaza un dictionar `closures` care va avea pentru fiecare stare a NFA-ului, epsilon-closure-ul
acesteia. Apoi initializez o parte din campurile DFA-ului, si anume `K`, `d`, `F` si `q0`. Pentru `K` si `F` se foloseste 
frozenset pentru fiecare stare din noul DFA. Dorim sa avem un _**set cu mai multe seturi**_, insa seturile nu sunt **hashable**.
Solutia ar fi ca atat pentru setul K (starile automatului), cat si pentru setul F (starile finale), inner set-urile acestora
sa fie de tipul **frozenset**, acest tip fiind intotdeauna hashable. Pentru `q0` se foloseste epsilon-closure-ul starii 
initiale a NFA-ului (pe care o adaugam si ca stare a automatului si se verifica daca o substare din acea multime apartine 
lui F). Pentru `d`, se initializeaza un dictionar gol. 

Pentru a realiza algoritmul, ma folosesc de lista `verify_states`, reprezentand starile pe care trebuie sa le analizez. 
La inceput, aceasta contine doar epsilon-closure-ul starii initiale. Apoi, in `while`, este extrasa o stare din lista.

Vom lucra cu starea curenta `curr_closure`. Pentru fiecare litera din alfabetul automatului, se va determina `next_states`,
care reprezinta starile in care se poate ajunge din `curr_closure` prin litera respectiva. Pentru fiecare stare din 
`next_states`, se va calcula epsilon-closure-ul fiecarei substari, si aceasta este noua stare a DFA-ului (`new_state`) 
(in cazul in care nu a mai aparut). Daca **starea noua** nu se afla in `K`, atunci este adaugata in ea si in `verify_states`,
astfel incat sa fie analizata si ea. De asemenea, verificam daca **starea noua** este stare finala (intersectia celor doua
multimi nu este multimea vida). Daca da, atunci este adaugata in `F`.

La final, se adauga in `d` o noua intrare, cu cheia tuplu dintre `curr_closure` (de la ea am pornit) si litera folosita, 
iar valoarea este `new_state` (starea in care am ajuns).

La final, se returneaza DFA-ul.

`remap_states` - Primeste un NFA si intoarce NFA-ul cu starile remapate. 
Cu ajutorul functiei f, modificam starile automatului. Pentru multimile `K` si `F`, se foloseste functia map, care primeste
ca parametru functia si iterable-ul (multimile vechi). Pentru functia de tranzitie, initializam un nou dictionar `d` 
si pentru fiecare intrare din functia de tranzitie veche (dictionar), se aplica functia `f` pe  starile de inainte si dupa
tranzitie. Se returneaza NFA-ul cu starile remapate.

### Clasa DFA
Pentru automatul finit determinist, am implementat cerintele etapei astfel:

`accept` - Primeste un cuvant si returneaza True daca cuvantul este acceptat de automat, False altfel.
Parcurg fiecare litera din cuvant, si fiecare tranzitie din automat. Daca am gasit o tranzitie care are ca stare de inceput
starea curenta (`current_state`) si input-ul este litera curenta (`letter`), atunci starea curenta devine starea de final 
a tranzitiei. Se foloseste `break` pentru a evita parcurgerea tranzitiilor pe aceeasi litera si stare de inceput diferita.
Dupa terminarea parcurgerii cuvantului, se verifica daca starea la care am ajuns este o stare finala (apartine lui self.F).
Daca da, returnam True, altfel False.

`remap_states` - Pentru aceasta functie, am presupus ca automatul primit a trecut prin algoritmul Subset Construction,
deci starile sale sunt de tip frozenset. Pentru a remapa starile, se ia fiecare frozenset, se transforma in lista,
se aplica functia `f` pe fiecare element din lista, prin intermediul functiei `map` si se transforma inapoi in frozenset.
Se returneaza DFA-ul cu starile remapate.




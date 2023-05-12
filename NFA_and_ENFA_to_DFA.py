# Epsilon NFA to NFA

initialState = ""
final_trans = {}
states = set()
alpha = set()
finalState = set()
DFA_finalState = set()
trans_full = []


def Alter_states(states, max_l):
    states = list(states)
    for i in states:
        x = i
        while len(x) < len(max_l):
            x = '0' + x
        states[states.index(i)] = x
    return set(states)


def All_States(states, alpha):  # gets all possible states
    for i in states:  # full states
        for j in alpha:
            trans_full.append((i, j))


transition = {}
DFA_transition = {}


def SetToString(s):
    # initialize an empty string
    str1 = ""
    s = sorted(s)
    # traverse in the string
    for ele in s:
        str1 += ele

    # return string
    return str1


def ENFA_DFA(transition, states, start_state, finalState):
    trans_eps = {}
    # get epsilon for each state
    for i in states:
        temp_state = set()
        temp_state.add(i)
        if (i, '^') in transition:
            temp_state.update(transition[(i, '^')])
            x = transition[(i, '^')]
            j = set()
            while x != j:
                j = x
                for z in x:
                    if (z, '^') in transition:
                        temp_state.update(transition[(z, '^')])
                        x = x | transition[(z, '^')]
        trans_eps[(i, '^')] = temp_state
    # alpha transition for the state then epsilon closure
    finalState_t = set()
    finalState_t.add(SetToString(trans_eps[(start_state, '^')]))
    current = list(finalState_t)[0]
    temp_tran = set()
    list_t = []
    while True:
        temp_tran.add(current)
        for j in alpha:
            temp_state = set()
            # iterate on state to get extra transition
            curent = [current[i:i + len(list(states)[0])] for i in range(0, len(current), len(list(states)[0]))]
            for i in curent:
                if (i, j) in transition:
                    temp = set()
                    for l in transition[(i, j)]:
                        temp.update(trans_eps[(l, '^')])
                    temp_state.update(temp)
            if temp_state:
                curr_state = SetToString(temp_state)
                final_trans[(current, j)] = {curr_state}
                if curr_state not in finalState_t:
                    list_t.append(curr_state)
                finalState_t.add(curr_state)

        if list_t:
            current = list_t[0]
            list_t.remove(current)
        else:
            break

    NFA_FinalState = set()  # output final states
    for FS in finalState:
        for val in finalState_t:
            if FS in val:
                NFA_FinalState.add(val)
    return final_trans, NFA_FinalState


def update_full(new_state, alpha, trans_full):  # this function is to create the new options in case new state is added
    for i in alpha:
        trans_full.append((new_state, alpha))


def new_state_trans(trans_i, transition, alpha, new_state):  # transition[i] and transition
    temp_d = {}
    for i in alpha:
        temp_set = set()
        for j in trans_i:
            temp_set.update(transition[(j, i)])
        if 'Dead' in temp_set and len(temp_set) > 1:  # check in case both dead
            temp_set.remove("Dead")
        temp_d[(new_state, i)] = temp_set

        # transition[(new_state,j)].append(transition[(i,j)])
    return temp_d


def NFA_to_DFA(states, alpha, transition, finalState, initialState):
    All_States(states, alpha)
    for i in trans_full:  # dead states handling
        if i not in transition.keys():
            transition[i] = {"Dead"}
            states.add('Dead')
            for j in alpha:
                transition[('Dead', j)] = {'Dead'}

    trans_temp = {}
    while trans_temp != transition:
        trans_temp = transition
        for i in transition:  # multiple output handling

            if len(transition[i]) == 1:
                DFA_transition[i] = transition[i]
            else:
                new_state = SetToString(transition[i])
                DFA_transition[i] = {new_state}
                states.add(new_state)
                update_full(new_state, alpha, trans_full)
                x = new_state_trans(transition[i], transition, alpha, new_state)
                transition = transition | x
    # handle the extra single state removing
    st_temp = set()
    temp30 = set()
    while st_temp != states:
        st_temp = states
        for st in states:
            flag = False
            for val in DFA_transition:
                if st == ''.join(DFA_transition[val]) and st != "Dead":
                    flag = True
            if flag == False:
                if st != initialState:
                    temp30.add(st)
                    for a in alpha:
                        DFA_transition.pop((st, a))
        states = states - temp30
    for i in DFA_transition:
        if DFA_transition[i] == 'Dead' and "Dead" not in states:
            states.add('Dead')
            for j in alpha:
                transition[('Dead', j)] = {'Dead'}

    # handling the final state
    for FS in finalState:
        for val in DFA_transition:
            if FS in ''.join(DFA_transition[val]):
                DFA_finalState.add(''.join(DFA_transition[val]))
    return DFA_transition, DFA_finalState


def main():
    global states, alpha, finalState
    key = ("state1", "0")
    value = {"state2"}
    value2 = {"state3","state4"}

    transition[key]=value
    transition[key].update(value2)

    for key in transition:
        for value in transition[key]:
            print(value)
            print(key)

    print(transition)
    '''print('1 NFA OR 2 ENFA  ')
    choice = input()
    if choice == '1':
        states_number = int(input("Enter states no."))
        for i in range(states_number):
            states.add(input())

        alpha_number = int(input("Enter alpha no."))
        for i in range(alpha_number):
            alpha.add(input())

        initialState = input("input the initial state")

        finalState_number = int(input("Enter finalState no."))  # check final state must be in states already
        for i in range(finalState_number):
            finalState.add(input())
        print(states)
        print(alpha)
        print(finalState)
        temp_key = 'start'
        temp_key = tuple(input("enter transition key and e x for exit").split())
        while (temp_key != ('e', 'x')):
            input_str = input()
            user_set = set(input_str.split(","))
            transition[temp_key] = user_set
            temp_key = tuple(input("enter transition").split())
            print(temp_key)
        print(transition)

        output, fi = NFA_to_DFA(states, alpha, transition, finalState, initialState)
        print(output)
        print(fi)
    else:
        states_number = int(input("Enter states no."))
        for i in range(states_number):
            states.add(input())
        max_l = max(states, key=len)
        print(max_l)
        # in case input states of different length, it make them equal
        states = Alter_states(states, max_l)
        print("here are your states:")  # the states user would use
        print(states)
        alpha_number = int(input("Enter alpha no."))
        for i in range(alpha_number):
            alpha.add(input())

        initialState = input("input the initial state")

        finalState_number = int(input("Enter finalState no."))  # check final state must be in states already
        for i in range(finalState_number):
            finalState.add(input())
        print(states)
        print(alpha)
        print(finalState)
        temp_key = 'start'
        temp_key = tuple(input("enter transition key and e x for exit").split())
        while (temp_key != ('e', 'x')):
            input_str = input()
            user_set = set(input_str.split(","))
            transition[temp_key] = user_set
            temp_key = tuple(input("enter transition").split())
        print(transition)
        output, fi = ENFA_DFA(transition, states, initialState, finalState)
        print(output)  # final transitions
        print(fi)  # final states of DFA
'''''

#main()

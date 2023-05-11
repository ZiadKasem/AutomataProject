#will be final Epsilon NFA to NFA


final_trans={}
states = set()
alpha = set()
finalState = set()
DFA_finalState= set()
trans_full=[]
def All_States(states,alpha):
    for i in states: # full states
        for j in alpha:
            trans_full.append((i,j))



transition = {
}
DFA_transition={}

def SetToString(s):
    # initialize an empty string
    str1 = ""
    s=sorted(s)
    # traverse in the string
    for ele in s:
        str1 += ele

    # return string
    return str1

def ENFA_DFA(transition,states,start_state,finalState):
    trans_eps={}
    #get_first_epsilon
    for i in states:
        temp_state=set()
        temp_state.add(i)
        if (i, '^') in transition:
            x=''.join(transition[(i,'^')])
            j= x
            while (j,'^') in transition:
                j=''.join(transition[j,'^'])
                temp_state.add(j)
            print(x)
            temp_state.add(x)
        trans_eps[(i,'^')]=temp_state
    print(trans_eps)
    #alpha_transition
    finalState_t=set()
    finalState_t.add(SetToString(trans_eps[(start_state,'^')]))
    current = list(finalState_t)[0]
    temp_tran= set()
    list_t=[]
    while True:
        temp_tran.add(current)
        for j in alpha:
            temp_state = set()
            curent = [current[i:i + len(list(states)[0])] for i in range(0, len(current), len( list(states)[0]))]  # OUTPUT: ['three', 'seven', 'eight', 'forty', 'fifty']
            print(curent)
            for i in curent:
                print(i)
                if (i, j) in transition:
                    temp = set()
                    for l in transition[(i, j)]:
                        temp.update(trans_eps[(l, '^')])
                    temp_state.update(temp)
            print(temp_state)
            if temp_state:
                   curr_state= SetToString(temp_state)
                   print(curr_state)
                   final_trans[(current,j)]={curr_state}
                   if curr_state not in finalState_t:
                    list_t.append(curr_state)
                    print("this is list")
                    print(list_t)
                   finalState_t.add(curr_state)

        if list_t:
            current=list_t[0]
            list_t.remove(current)
        else:
            break
    print(finalState_t)

    NFA_FinalState=set()
    for FS in finalState:
        for val in finalState_t:
            if FS in val:
                NFA_FinalState.add(val)
    return final_trans , NFA_FinalState



def update_full(new_state,alpha,trans_full):# this function is to create the new options in case new state is added
    for i in alpha:
        trans_full.append((new_state,alpha))



def new_state_trans(trans_i,transition,alpha,new_state): # transition[i] and transition
    temp_d= {}
    for i in alpha:
        temp_set=set()
        for j in trans_i:
            temp_set.update(transition[(j,i)])
        if 'Dead' in temp_set and len(temp_set)>1: #check in case both dead
            temp_set.remove("Dead")
        temp_d[(new_state,i)]=temp_set

            #transition[(new_state,j)].append(transition[(i,j)])
    return temp_d







def NFA_to_DFA(states,alpha,transition,finalState,initialState):
    All_States(states,alpha)
    for i in trans_full: # dead states handling
        if i not in transition.keys():
            transition[i]={"Dead"}
            states.add('Dead')
            for j in alpha:
                transition[('Dead',j)]={'Dead'}

    trans_temp={}
    while trans_temp != transition:
        trans_temp=transition
        for i in transition: # multiple output handling


            if len(transition[i]) == 1:
                DFA_transition[i]=transition[i]
            else:
                new_state = SetToString(transition[i])
                DFA_transition[i] = {new_state}
                states.add(new_state)
                update_full(new_state, alpha, trans_full)
                x=new_state_trans(transition[i], transition, alpha, new_state)
                transition= transition | x
#handle the extra single state removing
    st_temp=set()
    temp30=set()
    while st_temp != states:
        st_temp=states
        for st in states:
            flag = False
            for val in DFA_transition:
                if st == ''.join(DFA_transition[val]) and st!="Dead":
                    flag = True
            if flag == False:
                if st != initialState:
                     temp30.add(st)
                     for a in alpha:
                        DFA_transition.pop((st, a))
        states=states-temp30
    for i in DFA_transition:
        if DFA_transition[i]=='Dead' and "Dead" not in states:
            states.add('Dead')
            for j in alpha:
                transition[('Dead', j)] = {'Dead'}



    #handling the final state
    for FS in finalState:
        for val in DFA_transition:
            if FS in ''.join(DFA_transition[val]):
                DFA_finalState.add(''.join(DFA_transition[val]))
    print(DFA_transition)
    print(DFA_finalState)



def main():
  global states, alpha, finalState
  print('1 NFA OR 2 ENFA  ')
  choice=input()
  states_number=int(input("Enter states no."))
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
  temp_key='start'
  temp_key = tuple(input("enter transition key and e x for exit").split())
  while (temp_key !=('e','x')):
      input_str = input()
      user_set = set(input_str.split(","))
      transition[temp_key]=user_set
      temp_key = tuple(input("enter transition").split())
      print(temp_key)
  print(transition)
  if choice =='1':
     print('22')
     NFA_to_DFA(states,alpha,transition,finalState,initialState)
  else:
      output,fi=ENFA_DFA(transition, states, initialState, finalState)
      print(output)
      print(fi)
main()
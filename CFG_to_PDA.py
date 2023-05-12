#final
from collections import defaultdict

rules = ["S -> aSa|bSb|aPb|bPa","P -> aP|bP|#"]
transitions = defaultdict(list)
nonterm_userdef = ['S','P']
term_userdef = ['a','b']
start_symbol = 'S'

def grammarAugmentation(rules, nonterm_userdef,start_symbol):
    # newRules stores processed output rules
    newRules = []

    # create unique 'symbol' to
    # - represent new start symbol
    newChar = start_symbol + "'"
    while (newChar in nonterm_userdef):  # whyy comma
        newChar += "'"

    # adding rule to bring start symbol to RHS


    # new format => [LHS,[.RHS]],
    # can't use dictionary since
    # - duplicate keys can be there
    for rule in rules:

        # split LHS from RHS
        k = rule.split("->")
        lhs = k[0].strip()
        rhs = k[1].strip()

        # split all rule at '|'
        # keep single derivation in one rule
        multirhs = rhs.split('|')
        for rhs1 in multirhs:
            rhs1 = rhs1.strip().split()

           # ADD dot pointer at start of RHS
            #rhs1.insert(0, '.')
            newRules.append([lhs, ' '.join(rhs1)])
    print(newRules)
    for rule in newRules:
        print(f"{rule[0]} ->"
              f" {(rule[1])}")
    return newRules
def Push_down(rules,nonterm_userdef,start_symbol,term_userdef):
    rules_n = grammarAugmentation(rules,nonterm_userdef,start_symbol)


    #stack steps implementation------------------ read , push -> pop
    myStack=""
    #key(current state ,read) value(pop,push,next state)
    transitions[("Q0","#")].append(("#","$","Q1"))
    myStack="$"+myStack

    transitions[("Q1","#")].append(("#","S","Qloop"))
    myStack= start_symbol +myStack

    #now i am in q loop
    #write the productive rules of terminal state
    for rule in term_userdef:
        transitions[("Qloop",rule )].append((rule, "#", "Qloop"))



    #write the productive rules of Non-terminal state
    #key(current state ,read) value(pop,push,next state)
    state_counter = 1
    "pop non-terminal , push and increment state counter until the last one its next state is Qloop"
    for ntvalue in nonterm_userdef:
        transitions[("Qloop","#" )].append((ntvalue, "#", "Q"+str(state_counter+1)))
        state_counter=state_counter+1
        #add fixed counter
        ntValueNstate = state_counter
        #print(ntValueNstate)
        for rule in rules_n:
            if rule[0] == ntvalue:
                #handle the first element
                if  (len(rule[1])>1) :  # inorder not to handle the epthron twise
                    transitions[("Q" + str(ntValueNstate), "#")].append(("#", rule[1][len(rule[1]) - 1], "Q" + str(state_counter + 1)))
                    state_counter = state_counter + 1
                    for i in range(len(rule[1]) - 2):
                        # modify the q state
                        transitions[("Q" + str(state_counter), "#")].append(("#", rule[1][len(rule[1]) - 1 - i - 1], "Q" + str(state_counter + 1)))
                        state_counter = state_counter + 1
                    transitions[("Q" + str(state_counter), "#")].append(("#", rule[1][0], "Qloop"))
                    state_counter = state_counter + 1
                else:
                    transitions[("Q" + str(ntValueNstate), "#")].append(("#", rule[1][len(rule[1]) - 1], "Qloop"))

    #write the exit states after the Qloop
    #key(current state ,read) value(pop,push,next state)
    transitions["Qloop","#"].append(("$","#","Qfinal"))

    print("The Transitions")
    for tran in transitions:
        print("key:")
        print("current state,read")
        print(tran)
        print("value:")
        print("pop,push,next state")
        print(transitions[tran])
        for n in transitions[tran]:
            print(n[2])
        print("----------------")
def main():
    """print("Enter number of rules")
    num=int(input())
    print("rules")
    for i in range(num):
        rules.append(input())
    print("nonterm_userdef")
    st=input()
    nonterm_userdef= st.split(",")
    print(nonterm_userdef)
    print("term_userdef")
    st = input()
    term_userdef = st.split(",")
    print("start symbol")
    start_symbol=input()
    Push_down(rules,nonterm_userdef,start_symbol,term_userdef)
    print(transitions[1])"""
    Push_down(rules, nonterm_userdef, start_symbol, term_userdef)
#main()


# <METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Sudoku"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['Z. Guo', 'W. Dai']
PROBLEM_CREATION_DATE = "27-APR-2015"
PROBLEM_DESC= \
    '''
    Sudoku puzzle with heuristics functions
    '''
# </METADATA>

# <COMMON_CODE>
def DEEP_EQUALS(s1, s2):
    result = True
    for i in range(9):
        result = result and s1[i] == s2[i]
    return result


def DESCRIBE_STATE(state):
    # Produces a textual description of a state.
    # Might not be needed in normal operation with GUIs.
    txt = "\n"
    for i in range(9):
        txt += str(state[i]) + " "
        if i % 3 == 2:
            txt += "\n"
    return txt


def HASHCODE(s):
    '''The result should be an immutable object such as a string
    that is unique for the state s.'''
    return str(s)


def copy_state(s):
    news = []
    for i in s:
        news.append(i)
    return news


def can_move(s, steps):
    '''Tests whether it's legal to move a disk in state s
       from the From peg to the To peg.'''
    try:
        index = s.index(0)
        if index + steps < 0 or index + steps > 8: return False
        if index % 3 == 0 and steps == -1: return False
        if index % 3 == 2 and steps == 1: return False
        return True
    except (Exception) as e:
        print(e)


def move(s, steps):
    '''Assuming it's legal to make the move, this computes
       the new state resulting from moving the topmost disk
       from the From peg to the To peg.'''
    news = copy_state(s)  # start with a deep copy.
    index = s.index(0)
    news[index] = s[index + steps]
    news[index + steps] = 0
    return news  # return new state


def goal_test(s):
    '''If the first two pegs are empty, then s is a goal state.'''
    return s == [0, 1, 2, 3, 4, 5, 6, 7, 8]

#def which_box()

def goal_message(s):
    return "The 8 Puzzle is solved!"

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


def h_euclidean(s):
    result = 0
    goal = GOAL_STATE
    for i in s:
        index = s.index(i)
        g_index = goal.index(i)
        row = index / 3
        col = index % 3
        g_row = g_index / 3
        g_col = g_index % 3
        result += sqrt(pow(g_row - row, 2) + pow(g_col - col, 2))
    return result


def h_hamming(s):
    result = 0
    goal = GOAL_STATE
    for i in s:
        index = s.index(i)
        if goal[index] != i:
            result += 1
    return result


def h_manhattan(s):
    result = 0
    goal = GOAL_STATE
    for i in s:
        index = s.index(i)
        g_index = goal.index(i)
        row = index / 3
        col = index % 3
        g_row = g_index / 3
        g_col = g_index % 3
        result += abs(row - g_row) + abs(col - g_col)
    return result

# </COMMON_CODE>

GOAL_STATE = [0, 1, 2, 3, 4, 5, 6, 7, 8]

# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>

#  <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# </GOAL_MESSAGE_FUNCTION>


# <OPERATORS>
numbers = range(1, 9)
locations = [(row, col) for row in range(9) for col in range(9)]
OPERATORS = [Operator("Place " + str(i) + " at " + str(l),
                      lambda s, i=i: can_move(s, i),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s, i=i: move(s, i))
             for i in numbers for l in locations]
# </OPERATORS>

HEURISTICS = {'h_euclidean': h_euclidean, 'h_hamming':h_hamming, 'h_manhattan':h_manhattan}
from math import sqrt
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

# creates an initial state
CREATE_INITIAL_STATE = lambda : [[5, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0], [0, 9, 8, 0, 0, 0, 0, 6, 0], [8, 0, 0, 0, 6, 0, 0, 0, 3], [4, 0, 0, 8, 0, 3, 0, 0, 1], [7, 0, 0, 0, 2, 0, 0, 0, 6], [0, 6, 0, 0, 0, 0, 2, 8, 0], [0, 0, 0, 4, 1, 9, 0, 0, 5], [0, 0, 0, 0, 8, 0, 0, 7, 9]]

# <COMMON_CODE>
'''def DEEP_EQUALS(s1, s2):
    result = True
    for i in range(9):
        result = result and s1[i] == s2[i]
    return result'''

def DEEP_EQUALS(s1,s2):
  for i in range(9):
      for j in range(9):
          if s2[i][j] != s1[i][j]:
              return False
  return True

def HASHCODE(s):
    txt = ''
    for i in range(9):
        txt += str(s[i])
    return txt

def copy_state(s):
  copy = []
  for i in range(9):
      innerCopy = []
      for j in range(9):
          innerCopy.append(s[i][j])
      copy.append(innerCopy)
  return copy
  
def goal_test(s):
    # Test whether there is 0 at the goal state, if there is, return false; otherwise return true;
    for i in range(9):
        if 0 in s[i]:
            return False

'''    for h in range(9):
        sum = 0
        for j in range(9):
            sum += s[h][j]
        if sum != 45:
            return False
        
    for x in range(9):
        total = 0
        for y in range(9):
            total += s[y][x]
        if total != 45:
            return False
    for p in range(0, 8, 3):
        for q in range(0, 8, 3):
            box = box_array(s, p, q)
            for index in range(9):
                sum += box[index]
            if (sum != 45):
                return False'''
    return True

def DESCRIBE_STATE(state):
    # Produces a textual description of a state.
    # Might not be needed in normal operation with GUIs.
    txt = "\n"
    for i in range(9):
        txt += str(state[i]) + " "
        if i % 3 == 2:
            txt += "\n"
    return txt


'''def HASHCODE(s):
    '''The result should be an immutable object such as a string
    that is unique for the state s.'''
    return str(s)'''


def copy_state(s):
    news = []
    for i in s:
        newl = []
        for j in i:
            newl.append(j)
        news.append(newl)
    return news


def can_place(s, number, location):
    '''Tests whether it's legal to move a disk in state s
       from the From peg to the To peg.'''
    try:
        row = location[0]
        col = location[1]
        if s[row][col] != 0: return False
        if number in s[row]: return False
        row_array = []
        for i in range(9):
            row_array[i] = s[i][col]
        if number in row_array: return False
        box_number = which_box(row, col)
        box = box_array(s, box_number)
        if number in box: return False
        return True
    except (Exception) as e:
        print(e)


def move(s, number, location):
    '''Assuming it's legal to make the move, this computes
       the new state resulting from moving the topmost disk
       from the From peg to the To peg.'''
    news = copy_state(s)  # start with a deep copy.
    row = location[0]
    col = location[1]
    news[row][col] = number
    return news  # return new state

def which_box(row, col):
    return 3 * (row // 3) + (col // 3)

def box_array(s, box):
    array = []
    start_row = box // 3 * 3
    start_col = box % 3 * 3
    for i in range(start_row, start_row + 3):
        array.append(s[i][start_col])
        array.append(s[i][start_col+1])
        array.append(s[i][start_col+2])
    return array


def goal_message(s):
    return "Hooray! The Sudoku is solved!"

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


'''def h_euclidean(s):
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
    return result'''

# </COMMON_CODE>

# <STATE_VIS>
def render_state(s):
    txt = "\n"
    for i in s:
        txt += "| "
        for j in range(3):
            txt += str(i[3*j]) + " | " + str(i[3*j+1]) + " | " + str(i[3*j+2]) + " | "
        txt += "\n"
    return txt
# </STATE_VIS>

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
                      lambda s, i=i, l=l: can_place(s, i, l),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s, i=i, l=l: move(s, i, l))
             for i in numbers for l in locations]
# </OPERATORS>

HEURISTICS = {'h_euclidean': h_euclidean, 'h_hamming':h_hamming, 'h_manhattan':h_manhattan}

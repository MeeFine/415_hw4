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
CREATE_INITIAL_STATE = lambda: [[9, 2, 0, 6, 3, 1, 0, 4, 0],
                                [0, 6, 3, 4, 0, 7, 5, 0, 9],
                                [7, 1, 4, 0, 9, 5, 0, 6, 2],
                                [0, 7, 1, 5, 0, 3, 2, 0, 6],
                                [5, 3, 0, 2, 0, 0, 0, 8, 4],
                                [2, 0, 9, 0, 6, 0, 1, 0, 3],
                                [1, 5, 0, 3, 4, 6, 0, 7, 8],
                                [0, 4, 7, 0, 5, 0, 6, 2, 0],
                                [0, 9, 8, 1, 0, 2, 4, 3, 5]]

# <COMMON_CODE>

def DESCRIBE_STATE(s):
    txt = "\n"
    for i in range(9):
        if i % 3 == 0:
            txt += box_line()
        txt += "| "
        for j in range(9):
            txt += str(s[i][j]) + " "
            if j % 3 == 2:
                txt += "| "
        txt += "\n"
    txt += box_line()
    return txt
    

def box_line():
    txt = ""
    for k in range(25):
        if k % 8 == 0:
            txt += "+"
        else:
            txt += "-"
    txt += "\n"
    return txt

def DEEP_EQUALS(s1,s2):
    for i in range(9):
        for j in range(9):
            if s2[i][j] != s1[i][j]:
                return False
    return True

def HASHCODE(s):
    text = ''
    for i in s:
        text += str(i)
    return text
  
def goal_test(s):
    # Test whether there is 0 at the goal state, if there is, return false; otherwise return true;
    for i in s:
        if 0 in i:
            return False
    return True


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
            row_array.append(s[i][col])
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


def h_constraint(s):
    row_count = 0
    col_count = 0
    box_count = 0
    for i in s:
        for n in i:
            if n == 0:
                row_count += 1
    for i in range(9):
        box = box_array(s, i)
        for n in box:
            if n == 0:
                box_count += 1
    for i in range(9):
        for j in range(9):
            if s[j][i] == 0:
                col_count += 1
    return pow(row_count, 2) + pow(box_count, 2) + pow(col_count, 2)


def h_mrv(s):
    maxCount = 0
    nine = 0
    for x in s:
        valueCount = 0
        for val in x:
            if val != 0:
                valueCount += 1
        if valueCount == 9:
            valueCount = 0
            nine += 1
        if maxCount < valueCount:
            maxCount = valueCount

    for i in range(9):
        box = box_array(s, i)
        numberCount = 0
        for value in box:
            if value != 0:
                numberCount += 1
              #  lst.append(value)
        if numberCount == 9:
            numberCount = 0
            nine += 1
        if maxCount < numberCount:
            maxCount = numberCount


    for p in range(9):
        totalCount = 0
        for q in range(9):
            if s[q][p] != 0:
                totalCount += 1
        if totalCount == 9:
            totalCount = 0
            nine += 1
        if maxCount < totalCount:
            maxCount = totalCount

    return (9 - maxCount - nine) * 10

# </COMMON_CODE>


# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>

#  <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# </GOAL_MESSAGE_FUNCTION>


# <OPERATORS>
numbers = range(1, 10)
locations = [(row, col) for row in range(9) for col in range(9)]
OPERATORS = [Operator("Place " + str(i) + " at " + str(l),
                      lambda s, i=i, l=l: can_place(s, i, l),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s, i=i, l=l: move(s, i, l))
             for i in numbers for l in locations]
# </OPERATORS>

HEURISTICS = {'h_constraint': h_constraint, 'h_mrv': h_mrv}

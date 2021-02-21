from queue import PriorityQueue
import itertools
import time

# Board states are represented as lists of size 9, where the blank slot is represented by 0 and the puzzle is read 
# left to right, top to bottom. For example, the solved 8-puzzle will be represented as [1,2,3,4,5,6,7,8,0].

# The Node class contains 4 instance variables, a board state represented as a list shown above (board), its parent
# state which is also represented as a list (prev_board), and a pair of integers which correspond to the g(n) and h(n)
# values discussed in class (g and h). There are three accessor methods: get_board() which returns the Node's board 
# state, get_prev_board() which returns the stored parent board state, and get_g() which returns the stored value of g(n).
# There is no accessor for h, as a similar method introduced later will suffice for the scope of our program. The
# same class is used for all three algorithms, with its values determined on instantiation.
class Node:
    def __init__(self, board, prev_board, g, h):
        self.board = board
        self.prev_board = prev_board
        self.g = g
        self.h = h

    def get_board(self):
        return self.board
    
    def get_prev_board(self):
        return self.prev_board

    def get_g(self):
        return self.g

# The get_h() function takes two parameters, a board state represented as a list (board) and a search type represented as
# a string (search), and returns the appropriate h(n) value for 3 different heuristics. The uniform_cost heuristic is
# hardcoded as a 0. The misplaced_tile heuristic checks each position in the board against the goal board,
# [1,2,3,4,5,6,7,8,0], and if the correct number is not in the slot, it adds 1 to the h(n) value. The manhattan
# heuristic sums up the distances each individual tile is from its correct slot, called the manhattan distance. 
# In a 2-D structure, the manhattan distance uses the differences in x and y components of a tile's current and 
# goal slot, takes their absolute values, and sums them together. We can employ this formula for our 1-D board 
# representation using the mod function (%), where the horizontal component of a tile's current slot is the 
# [tile's index mod 3], the horizontal component of a tile's correct slot is [(tile's value - 1) mod 3], the 
# vertical component of a tile's current slot is [tile's index integer divided by 3], and the vertical component 
# of a tile's correct slot is [(tile's value - 1) integer divided by 3]. Taking their absolute values and summing 
# them together, we can calculate the manhattan distance for one tile, which we will sum with the rest of the tiles.
def get_h(board, search):
    if(search == 'uniform_cost'):
        return 0
    if(search == 'misplaced_tile'):
        h = 0
        for i in range(8):
            if(board[i] != i+1):
                h += 1
        return h
    if(search == 'manhattan'):
        h = 0
        index = 0
        for i in board:
            if i != 0:
                horizontal_diff= abs((i-1)%3 - index%3)
                vertical_diff = abs((i-1)//3 - index//3)
                h = h + horizontal_diff + vertical_diff
            index += 1
        return h

# The swap() function takes a board represented as a list (board), as well as two indices represented by integers (a and b), 
# and returns a list that contains the original board with the values at the two indices swapped. This function is different 
# from a standard swap function that swaps the inputted board's actual values; it just returns the result of the swap and leaves 
# the inputted board's values along. This function represents one operation to any board state, as all 4 operations, move a tile 
# up, left, right, or down into the blank space can be represented as a swap between the blank tile and the tile that was being
# operated on. For example, in the nearly solved board [1,2,3,4,5,6,7,0,8], moving the 8 left to complete the solve would be 
# represented as swap(__our_board__, 7, 8). A single operator function makes it easier for me to visualize the board in a 1-D 
# representation verses the standard move up/left/right/down operators that might be coded. Note that we are making a shallow copy 
# of the inputted board, as Python passes arguments by object reference, so without a shallow copy, we will be swapping the actual 
# values of the input board every time this function is called. 
def swap(board, a, b):
    temp = list(board)
    temp[a], temp[b] = temp[b], temp[a]
    return temp

# The expand() function takes a Node (n), the priority queue it adds new Nodes to (q), an interator (counter), and a search type 
# represented by a string (search). The function locates the position of the blank tile, determines the possible new states to add
# to the priority queue, and adds them accordingly with the correct constructor values base on the inputted search type. The function
# makes sure that it does not add the Node's parent state and adds the other possible operations associated with the blank tile's position.
# For example, if the blank tile was at index 0, or the top left corner, the only possible moves are moving the tile underneath up into 
# the blank space or moving the tile to its right left into the blank space. This is again represented by our swap function as 
# swap(__our_board__, 0, 3) and swap(__our_board__, 0, 1) respectively. This function does not return any values.
def expand(n, q, counter, search):
    b = n.get_board()
    prev_board = n.get_prev_board()
    new_g = n.get_g() + 1

    # Blank[0] can be swapped with right (1) or down (3).
    if(b[0] == 0):
        # Check to not add a Node with the parent board to the priority queue 
        if(swap(b, 0, 1) != prev_board):
            q.put((new_g + get_h(swap(b, 0, 1), search), next(counter), Node(swap(b, 0, 1), b, new_g, get_h(swap(b, 0, 1), search))))
        if(swap(b, 0, 3) != prev_board):
            q.put((new_g + get_h(swap(b, 0, 3), search), next(counter), Node(swap(b, 0, 3), b, new_g, get_h(swap(b, 0, 3), search))))
        return

    # Blank[1] can be swapped with left (0), right (2), or down (4).
    if(b[1] == 0):
        if(swap(b, 1, 0) != prev_board):
            q.put((new_g + get_h(swap(b, 1, 0), search), next(counter), Node(swap(b, 1, 0), b, new_g, get_h(swap(b, 1, 0), search))))
        if(swap(b, 1, 2) != prev_board):
            q.put((new_g + get_h(swap(b, 1, 2), search), next(counter), Node(swap(b, 1, 2), b, new_g, get_h(swap(b, 1, 2), search))))
        if(swap(b, 1, 4) != prev_board):
            q.put((new_g + get_h(swap(b, 1, 4), search), next(counter), Node(swap(b, 1, 4), b, new_g, get_h(swap(b, 1, 4), search))))
        return

    # Blank[2] can be swapped with left (1) or down (5).
    if(b[2] == 0):
        if(swap(b, 2, 1) != prev_board):
            q.put((new_g + get_h(swap(b, 2, 1), search), next(counter), Node(swap(b, 2, 1), b, new_g, get_h(swap(b, 2, 1), search))))
        if(swap(b, 2, 5) != prev_board):
            q.put((new_g + get_h(swap(b, 2, 5), search), next(counter), Node(swap(b, 2, 5), b, new_g, get_h(swap(b, 2, 5), search))))
        return

    # Blank[3] can be swapped with up (0), right (4), or down (6). 
    if(b[3] == 0):
        if(swap(b, 3, 0) != prev_board):
            q.put((new_g + get_h(swap(b, 3, 0), search), next(counter), Node(swap(b, 3, 0), b, new_g, get_h(swap(b, 3, 0), search))))
        if(swap(b, 3, 4) != prev_board):
            q.put((new_g + get_h(swap(b, 3, 4), search), next(counter), Node(swap(b, 3, 4), b, new_g, get_h(swap(b, 3, 4), search))))
        if(swap(b, 3, 6) != prev_board):
            q.put((new_g + get_h(swap(b, 3, 6), search), next(counter), Node(swap(b, 3, 6), b, new_g, get_h(swap(b, 3, 6), search))))
        return
    
    # Blank[4] can be swapped with up (1), left (3), right (5), or down (7).
    if(b[4] == 0):
        if(swap(b, 4, 1) != prev_board):
            q.put((new_g + get_h(swap(b, 4, 1), search), next(counter), Node(swap(b, 4, 1), b, new_g, get_h(swap(b, 4, 1), search))))
        if(swap(b, 4, 3) != prev_board):
            q.put((new_g + get_h(swap(b, 4, 3), search), next(counter), Node(swap(b, 4, 3), b, new_g, get_h(swap(b, 4, 3), search))))
        if(swap(b, 4, 5) != prev_board):
            q.put((new_g + get_h(swap(b, 4, 5), search), next(counter), Node(swap(b, 4, 5), b, new_g, get_h(swap(b, 4, 5), search))))
        if(swap(b, 4, 7) != prev_board):
            q.put((new_g + get_h(swap(b, 4, 7), search), next(counter), Node(swap(b, 4, 7), b, new_g, get_h(swap(b, 4, 7), search))))
        return
    
    # Blank[5] can be swapped with up (2), left (4), or down (8).
    if(b[5] == 0):
        if(swap(b, 5, 2) != prev_board):
            q.put((new_g + get_h(swap(b, 5, 2), search), next(counter), Node(swap(b, 5, 2), b, new_g, get_h(swap(b, 5, 2), search))))
        if(swap(b, 5, 4) != prev_board):
            q.put((new_g + get_h(swap(b, 5, 4), search), next(counter), Node(swap(b, 5, 4), b, new_g, get_h(swap(b, 5, 4), search))))
        if(swap(b, 5, 8) != prev_board):
            q.put((new_g + get_h(swap(b, 5, 8), search), next(counter), Node(swap(b, 5, 8), b, new_g, get_h(swap(b, 5, 8), search))))
        return

    # Blank[6] can be swapped with up (3) or right (7).
    if(b[6] == 0):
        if(swap(b, 6, 3) != prev_board):
            q.put((new_g + get_h(swap(b, 6, 3), search), next(counter), Node(swap(b, 6, 3), b, new_g, get_h(swap(b, 6, 3), search))))
        if(swap(b, 6, 7) != prev_board):
            q.put((new_g + get_h(swap(b, 6, 7), search), next(counter), Node(swap(b, 6, 7), b, new_g, get_h(swap(b, 6, 7), search))))
        return

    # Blank[7] can be swapped with up (4), left (6), or right (8).
    if(b[7] == 0):
        if(swap(b, 7, 4) != prev_board):
            q.put((new_g + get_h(swap(b, 7, 4), search), next(counter), Node(swap(b, 7, 4), b, new_g, get_h(swap(b, 7, 4), search))))
        if(swap(b, 7, 6) != prev_board):
            q.put((new_g + get_h(swap(b, 7, 6), search), next(counter), Node(swap(b, 7, 6), b, new_g, get_h(swap(b, 7, 6), search))))
        if(swap(b, 7, 8) != prev_board):
            q.put((new_g + get_h(swap(b, 7, 8), search), next(counter), Node(swap(b, 7, 8), b, new_g, get_h(swap(b, 7, 8), search))))
        return

    # Blank[8] can be swapped with up (5) or left (7).
    if(b[8] == 0):
        if(swap(b, 8, 5) != prev_board):
            q.put((new_g + get_h(swap(b, 8, 5), search), next(counter), Node(swap(b, 8, 5), b, new_g, get_h(swap(b, 8, 5), search))))
        if(swap(b, 8, 7) != prev_board):
            q.put((new_g + get_h(swap(b, 8, 7), search), next(counter), Node(swap(b, 8, 7), b, new_g, get_h(swap(b, 8, 7), search))))
        return

# The repeated() function takes a list (board) and checks it against a list of boards (_list). repeated() returns true if the list
# contains the board and false if the list does not. This function is used to check for repeated board states that are not immediate
# parent states (e.g. moving the blank in a circle without changing the other tiles). This check is mainly for unsolvable boards, as
# normally the Nodes with lower g(n) + h(n) values will be expanded first.
def repeated(board, _list):
    for i in _list:
        if board == i:
            return True
    return False

# The uniform_cost_search() function takes an initial board (init_board) and a trace flag represented as a char (trace) and performs a uniform cost search
# for the goal state. If the goal state is found, a success message is displayed along with the depth, expanded nodes, frontier nodes,
# and the time taken. If no goal state is found, a failure message is displayed along with the expanded nodes and time taken. If the
# trace flag is '1', the trace for the solution is displayed as well. This method along with the other 2 searches use the python time library to display
# the system runtime. 
def uniform_cost_search(init_board, trace):
    start_time = time.time()
    expanded_nodes = 0
    frontier_nodes = 0

    # This iterator from python's itertools library is used to assign a unique value to each tuple, as python's priority queue compares subsequent values 
    # in tuples when prior values are equal, but I did not want to overload the '<' operator for my defined Node class. Since we can choose how to prioritize
    # Nodes with the same priority, this method is used.
    counter = itertools.count()
    repeated_states = []
    max_q_size = 0
    print('Using initial board: ' + str(init_board))

    # initial node creation using uniform cost heuristic (hardcoded as 0)
    n = Node(init_board, init_board, 0, get_h(init_board, 'uniform_cost'))
    q = PriorityQueue()

    # This is how we assign unique integers to the tuple's second value.
    q.put((n.get_g(), next(counter), n))
    
    while not q.empty():
        # update the max queue size accordingly
        if(q.qsize()>max_q_size):
            max_q_size = q.qsize()

        # we dequeue the first value from our priority queue and set it equal to temp
        temp = q.get()[2]

        # we skip the expansion process if the board is repeated.
        if(repeated(temp.get_board(),repeated_states)):
            continue

        # success state, all displayed values are appropriately calculated
        if(temp.get_board() == [1,2,3,4,5,6,7,8,0]):
            print('Final board: ' + str(temp.get_board()))
            print('Success!')
            print('Depth: ' + str(temp.get_g()))
            print('Expanded Nodes: ' + str(expanded_nodes))
            print('Frontier Nodes: ' + str(q.qsize()))
            print('Max Queue Size: '+ str(max_q_size))
            print("-- %s seconds -- were used." % (time.time() - start_time))
            return

        # trace check whether to output trace of expansion or not
        if(trace == '1'):
            print('The next state to expand has g(n) = ' + str(temp.get_g()) + ' and h(n) = ' + str(get_h(temp.get_board(), 'uniform_cost')) + ':')
            print(temp.get_board())

        # expansion of dequeued node using uniform cost heuristic
        expand(temp, q, counter, 'uniform_cost')

        # add this expanded node to repeated_states[]
        repeated_states.append(temp.get_board())
        expanded_nodes += 1
    
    # failure state, our priority queue has nothing left to check
    print('No solution exists!')
    print('Expanded Nodes: ' + str(expanded_nodes))
    print("-- %s seconds -- were used." % (time.time() - start_time))

# The misplaced_tile_search() function closely resembles our uniform_cost_search() function. The latter is documented, and as the algorithms are similar,
# only major differences will be noted.
def misplaced_tile_search(init_board, trace):
    start_time = time.time()
    expanded_nodes = 0
    frontier_nodes = 0
    counter = itertools.count()
    repeated_states = []
    max_q_size = 0
    print('Using initial board: ' + str(init_board))

    # initial node creation with misplaced tile heuristic
    n = Node(init_board, init_board, 0, get_h(init_board, 'misplaced_tile'))
    q = PriorityQueue()
    q.put((n.get_g() + get_h(n.get_board(), 'misplaced_tile'), next(counter), n))
    
    while not q.empty():
        if(q.qsize()>max_q_size):
            max_q_size = q.qsize()
        temp = q.get()[2]
        if(repeated(temp.get_board(),repeated_states)):
            continue
        if(temp.get_board() == [1,2,3,4,5,6,7,8,0]):
            print('Final board: ' + str(temp.get_board()))
            print('Success!')
            print('Depth: ' + str(temp.get_g()))
            print('Expanded Nodes: ' + str(expanded_nodes))
            print('Frontier Nodes: ' + str(q.qsize()))
            print('Max Queue Size: '+ str(max_q_size))
            print("-- %s seconds -- were used." % (time.time() - start_time))
            return
        if(trace == '1'):
            print('The next state to expand has g(n) = ' + str(temp.get_g()) + ' and h(n) = ' + str(get_h(temp.get_board(), 'misplaced_tile')) + ':')
            print(temp.get_board())

        # expansion of dequeued node using misplaced tile heuristic
        expand(temp, q, counter, 'misplaced_tile')
        repeated_states.append(temp.get_board())
        expanded_nodes += 1
    print('No solution exists!')
    print('Expanded Nodes: ' + str(expanded_nodes))
    print("-- %s seconds -- were used." % (time.time() - start_time))

# Again, the manhattan_search() function is similar to the previous two functions, using the manhattan heuristic to find the goal state.
def manhattan_search(init_board, trace):
    start_time = time.time()
    expanded_nodes = 0
    frontier_nodes = 0
    counter = itertools.count()
    repeated_states = []
    max_q_size = 0
    print('Using initial board: ' + str(init_board))

    # initial node creation using manhattan heuristic
    n = Node(init_board, init_board, 0, get_h(init_board, 'manhattan'))
    q = PriorityQueue()
    q.put((n.get_g() + get_h(n.get_board(), 'manhattan'), next(counter), n))
    
    while not q.empty():
        if(q.qsize()>max_q_size):
            max_q_size = q.qsize()
        temp = q.get()[2]
        if(repeated(temp.get_board(),repeated_states)):
            continue
        if(temp.get_board() == [1,2,3,4,5,6,7,8,0]):
            print('Final board: ' + str(temp.get_board()))
            print('Success!')
            print('Depth: ' + str(temp.get_g()))
            print('Expanded Nodes: ' + str(expanded_nodes))
            print('Frontier Nodes: ' + str(q.qsize()))
            print('Max Queue Size: '+ str(max_q_size))
            print("-- %s seconds -- were used." % (time.time() - start_time))
            return
        if(trace == '1'):
            print('The next state to expand has g(n) = ' + str(temp.get_g()) + ' and h(n) = ' + str(get_h(temp.get_board(), 'manhattan')) + ':')
            print(temp.get_board())

        # expansion of dequeued node using manhattan heuristic
        expand(temp, q, counter, 'manhattan')
        repeated_states.append(temp.get_board())
        expanded_nodes += 1
    print('No solution exists!')
    print('Expanded Nodes: ' + str(expanded_nodes))
    print("-- %s seconds -- were used." % (time.time() - start_time))

# The main() function is called when the program is run. It contains a hardcoded initial board for testing or viewing purposes as well as an option to input
# a custom board. The format for inputting a custom board is from left to right, top to bottom, with 0 as a blank tile and including spaces in between tiles.
# Next is an option to choose which algorithm to use, 1 for uniform cost, 2 for misplaced tile, and 3 for manhattan. Finally a trace of the search can be 
# included if '1' is entered. the program exits after the appropriate search finishes.
def main():
    num = input('Type "1" to use a default puzzle or "2" to enter your own puzzle.\n')
    if(num == '1'):
        init_board = [0,7,2,4,6,1,3,5,8]
    if(num == '2'):
        my_string = input('Enter a puzzle from left to right, top to bottom, using 0 for the blank tile and including spaces in between tiles. Ex: "1 2 3 4 5 6 7 8 0".\n')
        my_list = my_string.split()
        map_object = map(int, my_list)
        init_board = list(map_object)
    function = input('Enter your choice of algorithm: "1" for Uniform Cost, "2" for A* - Misplaced Tile, or "3" for A* - Manhattan.\n')
    trace = input('Would you like to display a trace of the algorithm? "1" for YES and "2" for NO\n')
    if(function == '1'):
        uniform_cost_search(init_board, trace)
    if(function == '2'):
        misplaced_tile_search(init_board, trace)
    if(function == '3'):
        manhattan_search(init_board, trace)

if __name__ == "__main__":
    main()
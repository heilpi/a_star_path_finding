import numpy as np
from timeit import default_timer as timer

class Node:

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def map_code(str):
    mapcode = str.split('\n')[1]
    return mapcode

def maze_convert(str):
    str = str.split('\n',2)[2]
    str = str.rsplit('\n',1)[0]
    str = str.split('\n')
    maze = []
    for i in str:
        i = i.strip()
        i = list(map(lambda j:j, i))
        maze.append(i)
        np_maze = np.array(maze)
    return np_maze

def starting_position(maze):
    start = np.where(maze == 'S')
    i = start[0]
    j = start[1]
    start = [*j,*i]
    maze[maze == 'S'] = '.'
    return start

def ending_position(maze):
    end = np.where(maze == 'E')
    i = end[0]
    j = end[1]
    end = [*j,*i]
    return end

def return_path(current_node, maze): 
    path = []
    no_rows, no_columns = np.shape(maze)
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    path_distance = len(path)-1

    #here we create the initialized result maze with 0 in every position
    #UNCOMMENT TO SHOW THE RESULT MAZE 
    
    # result = np.zeros((no_rows,no_columns), dtype=int)
    # path = path[::-1]
    # start_value = 0
    # for i in range(len(path)):
    #     result[path[i][1]][path[i][0]] = start_value
    #     start_value += 1
    # np.set_printoptions(threshold=np.inf, linewidth=np.inf)
    # print(result)
    # print(maze)

    return path_distance



def search(maze, cost, start, end):
    
    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, tuple(end))
    end_node.g = end_node.h = end_node.f = 0

    yet_to_visit_list = []  
    visited_list = [] 
    yet_to_visit_list.append(start_node)
    
    outer_iterations = 0
    max_iterations = (len(maze) // 2) ** 10

    move  =  [[ 0, -1],
              [-1, 0 ],               
              [ 0, 1 ],
              [ 1, 0 ],] 

    no_rows, no_columns = np.shape(maze)
    
    while len(yet_to_visit_list) > 0:
        outer_iterations += 1

        current_node = yet_to_visit_list[0]
        current_index = 0
        for index, item in enumerate(yet_to_visit_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
                
        if outer_iterations > max_iterations:
            print ("giving up on pathfinding too many iterations")
            return return_path(current_node,maze)

        yet_to_visit_list.pop(current_index)
        visited_list.append(current_node)
        if current_node == end_node:
            return return_path(current_node,maze)

        children = []

        for new_position in move: 

            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if (node_position[0] > (no_rows - 2) or 
                node_position[0] < 1 or 
                node_position[1] > (no_columns -2) or 
                node_position[1] < 1):
                continue

            if maze[node_position[0]][node_position[1]] != '.':
                continue
            
            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:
            if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                continue

            child.g = current_node.g + cost
            child.h = (((child.position[0] - end_node.position[0]) ** 2) + 
                       ((child.position[1] - end_node.position[1]) ** 2)) 

            child.f = child.g + child.h

            if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                continue

            yet_to_visit_list.append(child)


if __name__ == '__main__':

    start_timer = timer()
    str = """
    4345640
    ##################################################
    #.....#..........................................#
    #....................................#...........#
    #...........#.....#..............................#
    #.........#...#.#.........#..................#...#
    #..............#.........................#.....#.#
    #..........#.....................................#
    #....#........................................#..#
    #.......#....#...#...............................#
    #.....#....................#........#............#
    ##.............................................#.#
    #...#............................................#
    #................................................#
    #........#.......................................#
    #.........................#......................#
    #.#..............................................#
    #.........#....#........#........................#
    #..E.................#..............#............#
    #..#...#....................................#....#
    #..................................#..........#..#
    #.............#..................................#
    #.............#.S................................#
    #.......................................#........#
    #.....................#..........................#
    #......................................#.........#
    #....#...............#...........................#
    #........#...............#.......................#
    ##...............................................#
    #...................#..#.........................#
    ##################################################
    """
    maze = maze_convert(str)

    start = starting_position(maze)
    end = ending_position(maze)
    cost = 1 

    path = search(maze, cost, start, end)

    mapcode = map_code(str)
    print('starting at', start, ', ending', end)
    print("{}:{}".format(mapcode,path))
    end_timer = timer()
    print(end_timer - start_timer)



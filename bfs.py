from collections import deque
import copy
class Path:
    def __init__(self):
        self.path = []

    def __repr__(self):
        return str(self.path)

def get_neighbors(point, map):

    neigh = [(point[0], point[1] + 1),
             (point[0], point[1] - 1),
             (point[0] + 1, point[1]),
             (point[0] - 1, point[1])
             ]
    valid_neigh = []
    for pt in neigh:
        if pt[0] >= 0 and pt[0] < len(map) and pt[1] >= 0 and pt[1] < len(map[0]):
            if map[pt[0]][pt[1]] == 0:
                valid_neigh.append(pt)

    return valid_neigh


def bfs(map, start, goal):
    seen = [] # Seen positions, first path enters. If new path hits seen, pop it
    queue = deque()
    start_path = Path()
    start_path.path.append(start)
    queue.append(start_path)

    while len(queue) > 0:
        current = queue.popleft()
        #print("Current path: " + str(current))
        seen.append(current.path[-1])
        if (current.path[-1] == goal):
            print("Done!")
            print("Length = " + str(len(current.path)))
            return current.path

        neighbors = get_neighbors(current.path[-1], map)
        for neigh in neighbors:
            if not neigh in seen:
                #print("New neighbor: " + str(neigh))
                neigh_path = copy.deepcopy(current)
                neigh_path.path.append(neigh)
                #print("New path in queue: " + str(neigh_path))
                queue.append(neigh_path)
                seen.append(neigh)

        #print("Current queue: " + str(queue))

if __name__=="__main__":
    map = [[0, 0, 0, 0],
           [0, 0, 1, 0],
           [0, 1, 0, 0],
           [0, 1, 0, 0],
           [0, 0, 0, 0]]

    start = (0,0)
    goalx = 2
    goaly = 4
    goal = (goaly, goalx)

    path = bfs(map, start, goal)
    print(path)

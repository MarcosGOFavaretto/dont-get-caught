import heapq
from ...utils import heuristic
class Node:
    def __init__(self, position, parent=None, g=0, h=0):
        self.position = position  # (x, y)
        self.parent = parent
        self.g = g  # Cost from start to this node
        self.h = h  # Heuristic cost to goal
        self.f = g + h  # Total cost

    def __lt__(self, other):
        return self.f < other.f  # For priority queue sorting

def get_neighbors(position, grid):
    x, y = position
    neighbors = [
        (x+1, y), (x-1, y), (x, y+1), (x, y-1)
    ]
    return [(nx, ny) for nx, ny in neighbors if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and not grid[nx][ny].is_student_desk]

def a_star(grid, start, goal):
    open_list = []
    heapq.heappush(open_list, Node(start, None, 0, heuristic(start, goal)))
    closed_set = set()

    while open_list:
        current = heapq.heappop(open_list)

        if current.position == goal:
            path = []
            while current:
                path.append(current.position)
                current = current.parent
            return path[::-1][1:]  # Return reversed path

        closed_set.add(current.position)

        for neighbor in get_neighbors(current.position, grid):
            if neighbor in closed_set:
                continue

            g_cost = current.g + 1
            h_cost = heuristic(neighbor, goal)
            neighbor_node = Node(neighbor, current, g_cost, h_cost)

            # Avoid duplicate nodes with worse paths
            if any(n.position == neighbor and n.f <= neighbor_node.f for n in open_list):
                continue

            heapq.heappush(open_list, neighbor_node)

    return None  # No path found

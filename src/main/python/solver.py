"""Importable water pouring solver."""

#I tried this first without guidance - as you can tell, it's pretty bad
#Here's a more elegant solution:
#https://www.geeksforgeeks.org/water-jug-problem-using-memoization/?ref=rp
#But this is the first time I've ever done work with recursion so at least it's better than nothing

#A container object would work much better
#At first it didn't work because all the functions referred to the same three containers
#So I rewrote everything to just represent a container as [fill, capacity]
#I forgot that creating new Container objects existed
#I'll rewrite to use Container objects one day
class Container():
    """Represents a water container."""

    def __init__ (self, capacity, initial_fill=0):
        """Initialize container."""
        self.capacity = capacity
        self.fill = initial_fill
    def empty(self):
        self.fill = 0
    def fill_max(self):
        self.fill = self.capacity

def resolve_current(action_id, acted_on, containers, target, already_tried, path):
    """Determine if the target volume has been reached and act accordingly.
    If either container - `current_1` or `current_2` - is at the target volume, then return all
    data involved getting there, stored in `path`. Else, check if this combination of volumes has
    already been evaluated earlier (which means that a dead end has been reached). If it has
    already been evaluated, kill this branch; if not, start another branch and perform all six
    possible actions on the current containers.
    """
    
    current_fill_states = []
    current_container_states = []
    for container in containers:
        current_fill_states.append(container[0])
        current_container_states.append([container[0], container[1]])
    #print(current_fill_states)
    if target in current_fill_states:
        path.append([action_id, acted_on, current_container_states, len(path)])
        return path
    if current_fill_states in already_tried:
        #print(already_tried)
        #print(f'{current_fill_states} failed')
        return None
    else:
        already_tried.append(current_fill_states)
        path.append([action_id, acted_on, current_container_states, len(path)])
        result = branch(containers, target, already_tried, path)
        if result:
            return result
        else:
            return None
def empty_container(containers, act_on, target, already_tried, path):
    """Empty container and call `resolve_current`."""
    print(f"Emptied container {act_on}")
    containers[act_on][0] = 0
    return resolve_current(1, act_on, containers, target, already_tried, path)
def fill_container(containers, act_on, target, already_tried, path):
    """Fill container to capacity and call `resolve_current`."""
    print(f"Filled container {act_on}")
    containers[act_on][0] = containers[act_on][1]
    return resolve_current(2, act_on, containers, target, already_tried, path)
def fill_1_from_2(containers, act_on, target, already_tried, path):
    """Fill container 1 with the liquid from container 2.

    Either empty container 2 if its contents are greater than the negative space of container
    1, or fill container 1 to capacity (leaving some liquid in container 2).
    """
    print(f"Filled container {act_on[0]} from {act_on[1]}")
    '''
    #...

    container_1_fill = containers[act_on[0]][0]
    container_2_fill = containers[act_on[1]][0]
    container_1_capacity = containers[act_on[0]][1]
    container_2_capacity = containers[act_on[1]][1]
    '''
    #print(container_1_fill)
    #print(container_2_fill)
    if containers[act_on[0]][1] - containers[act_on[0]][0] > containers[act_on[1]][0]:
        containers[act_on[0]][0] += containers[act_on[1]][0]
        containers[act_on[1]][0] = 0
    else:
        containers[act_on[1]][0] -= containers[act_on[0]][1] - containers[act_on[0]][0]
        containers[act_on[0]][0] = containers[act_on[0]][1] = containers[act_on[0]][1]
    #print(container_1.fill)
    #print(container_2.fill)
    return resolve_current(3, act_on, containers, target, already_tried, path)
def branch(containers, target, already_tried, path):
    """Perform all possible actions on the current set of containers.
    
    The order matters here, so all possible connections are tested.
    """
    for container_1_index in range(0, len(containers)):
        a = empty_container(containers, container_1_index, target, already_tried, path)
        if a:
            return a
        b = fill_container(containers, container_1_index, target, already_tried, path)
        if b:
            return b
        for container_2_index in range(0, len(containers)):
            if container_1_index == container_2_index:
                continue
            c = fill_1_from_2(containers, [container_1_index, container_2_index], target, already_tried, path)
            if c:
                return c
            d = fill_1_from_2(containers, [container_2_index, container_1_index], target, already_tried, path)
            if d:
                return d
    return None

def solve(containers, target):
    """Solve (and validate) a given water pouring problem.

    `containers` is an array of Container objects.
    """
    try:
        resulting_path = branch(containers, target, [], [])
    except RecursionError:
        return 1
    if resulting_path:
        return resulting_path
    else:
        return 2

def enumerate_str(containers):
    return_str = ""
    for container in containers:
        return_str += f'{container[0]}/{container[1]}, '
    return_str = return_str[:-2]
    return return_str

def to_readable(final_path):
    """Output the process into a human-readable format."""
    final = ""
    final += (f'Start: {enumerate_str(final_path[0][2])}\n')
    for step in final_path:
        action = step[0]
        acted_on = step[1]
        containers = step[2]
        index = step[3]+1
        if action == 1:
            final += (f'{index} - Empty container {acted_on}: {enumerate_str(containers)}\n')
        elif action == 2:
            final += (f'{index} - Fill container {acted_on}: {enumerate_str(containers)}\n')
        elif action == 3:
            final += (f'{index} - Fill container {acted_on[0]} from {acted_on[1]}: {enumerate_str(containers)}\n')
    final += (f'Target reached: {enumerate_str(containers)}\n')
    return final

def action_str(index):
    """Return a string describing the action associated with `index`."""
    actions = {
        0:"Empty container 1.",
        1:"Empty container 2.",
        2:"Fill container 1 to capacity.",
        3:"Fill container 2 to capacity.",
        4:"Fill container 1 from 2.",
        5:"Fill container 2 from 1."
    }
    return actions[index]

if __name__ == "__main__":
    c1 = [0, 69]
    c2 = [0, 42]
    c3 = [0, 31]
    c4 = [0, 25]
    aa = solve([c1, c2, c3, c4], 10)
    print(aa)
    if aa not in (1, 2):
        bb = to_readable(aa)
        print(bb)


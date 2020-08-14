"""Importable water pouring solver."""

#I tried this first without guidance - as you can tell, it's pretty bad
#Here's a more elegant solution:
#https://www.geeksforgeeks.org/water-jug-problem-using-memoization/?ref=rp
#But this is the first time I've ever done work with recursion so at least it's better than nothing

#A container object would work much better

def resolve_current(action_id, current_1, size_1, current_2, size_2, target, already_tried, path):
    """Determine if the target volume has been reached and act accordingly.
    If either container - `current_1` or `current_2` - is at the target volume, then return all
    data involved getting there, stored in `path`. Else, check if this combination of volumes has
    already been evaluated earlier (which means that a dead end has been reached). If it has
    already been evaluated, kill this branch; if not, start another branch and perform all six
    possible actions on the current containers.
    """
    if target in (current_1, current_2):
        #print(f'Found a solution at path length {len(path)}; {current_1}/{size_1}, {current_2}/{size_2}')
        path.append([action_id, current_1, current_2, len(path)])
        return path
    else:
        if [current_1, current_2] in already_tried:
            #print(already_tried)
            #print(f'killing {current_1}/{size_1}, {current_2}/{size_2} with a path length of {len(path)-1}')
            return None
        else:
            already_tried.append([current_1, current_2])
            path.append([action_id, current_1, current_2, len(path)])
            result = branch(current_1, size_1, current_2, size_2, target, already_tried, path)
            if result:
                return result
def empty_1(current_1, size_1, current_2, size_2, target, already_tried, path):
    """Empty container 1 and call `resolve_current`."""
    current_1 = 0
    return resolve_current(0, current_1, size_1, current_2, size_2, target, already_tried, path)
def empty_2(current_1, size_1, current_2, size_2, target, already_tried, path):
    """Empty container 2 and call `resolve_current`."""
    current_2 = 0
    return resolve_current(1, current_1, size_1, current_2, size_2, target, already_tried, path)
def fill_1(current_1, size_1, current_2, size_2, target, already_tried, path):
    """Fill container 1 to capacity and call `resolve_current`."""
    current_1 = size_1
    return resolve_current(2, current_1, size_1, current_2, size_2, target, already_tried, path)
def fill_2(current_1, size_1, current_2, size_2, target, already_tried, path):
    """Fill container 2 to capacity and call `resolve_current`."""
    current_2 = size_2
    return resolve_current(3, current_1, size_1, current_2, size_2, target, already_tried, path)
def fill_1_from_2(current_1, size_1, current_2, size_2, target, already_tried, path):
    """Fill container 1 with the liquid from container 2.
    Either empty container 2 if its contents are greater than the negative space of container
    1, or fill container 1 to capacity (leaving some liquid in container 2).
    """
    if size_1 - current_1 > current_2:
        current_1 += current_2
        current_2 = 0
    else:
        current_2 -= size_1 - current_1
        current_1 = size_1
    return resolve_current(4, current_1, size_1, current_2, size_2, target, already_tried, path)
def fill_2_from_1(current_1, size_1, current_2, size_2, target, already_tried, path):
    """Fill container 2 with the liquid from container 1.

    Either empty container 1 if its contents are greater than the negative space of container
    1, or fill container 2 to capacity (leaving some liquid in container 1).
    """
    if size_2 - current_2 > current_1:
        current_2 += current_1
        current_1 = 0
    else:
        current_1 -= size_2 - current_2
        current_2 = size_2
    return resolve_current(5, current_1, size_1, current_2, size_2, target, already_tried, path)
def branch(current_1, size_1, current_2, size_2, target, already_tried, path):
    """Perform all possible actions on the current set of containers."""
    a = empty_1(current_1, size_1, current_2, size_2, target, already_tried, path)
    if a:
        return a
    b = empty_2(current_1, size_1, current_2, size_2, target, already_tried, path)
    if b:
        return b
    c = fill_1(current_1, size_1, current_2, size_2, target, already_tried, path)
    if c:
        return c
    d = fill_2(current_1, size_1, current_2, size_2, target, already_tried, path)
    if d:
        return d
    e = fill_1_from_2(current_1, size_1, current_2, size_2, target, already_tried, path)
    if e:
        return e
    f = fill_2_from_1(current_1, size_1, current_2, size_2, target, already_tried, path)
    if f:
        return f
    else:
        return None

def solve(size_1, size_2, target, initial_1=0, initial_2=0):
    """Solve (and validate) a given water pouring problem.

    `size_1` is the capacity of container 1, and `size_2` is the capacity of container 2.
    `target` is the desired volume in either container. Both containers are empty to begin
    by default.
    """
    #check if this problem is even solvable
    if initial_1 > size_1 or initial_2 > size_2 or (target > size_1 and target > size_2):
        return 0
    #below are always invalid states and should always kill a branch
    invalid = [[initial_1, initial_2], [size_1, size_2]]
    try:
        resulting_path = branch(initial_1, size_1, initial_2, size_2, target, invalid, [])
    except RecursionError:
        return 1
    if resulting_path:
        return resulting_path

def to_readable(size_1, size_2, final_path, initial_1=0, initial_2=0):
    """Output the process into a human-readable format."""
    current_1 = initial_1
    current_2 = initial_2
    final = ""
    final += (f'Start: {current_1}/{size_1}, {current_2}/{size_2}\n')
    index = 0
    for element in final_path:
        action = element[0]
        current_1 = element[1]
        current_2 = element[2]
        index = element[3]+1

        if action == 0:
            current_1 = 0
            final += (f'{index} - Empty container 1: {current_1}/{size_1}, {current_2}/{size_2}\n')
        elif action == 1:
            current_2 = 0
            final += (f'{index} - Empty container 2: {current_1}/{size_1}, {current_2}/{size_2}\n')
        elif action == 2:
            current_1 = size_1
            final += (f'{index} - Fill container 1 to full: {current_1}/{size_1}, {current_2}/{size_2}\n')
        elif action == 3:
            current_2 = size_2
            final += (f'{index} - Fill container 2 to full: {current_1}/{size_1}, {current_2}/{size_2}\n')
        elif action == 4:
            if size_1 - current_1 > current_2:
                current_1 += current_2
                current_2 = 0
            else:
                current_2 -= size_1 - current_1
                current_1 = size_1
            final += (f'{index} - Fill container 1 from 2: {current_1}/{size_1}, {current_2}/{size_2}\n')
        elif action == 5:
            if size_2 - current_2 > current_1:
                current_2 += current_1
                current_1 = 0
            else:
                current_1 -= size_2 - current_2
                current_2 = size_2
            final += (f'{index} - Fill container 2 from 1: {current_1}/{size_1}, {current_2}/{size_2}\n')
    final += (f'Target reached: {current_1}/{size_1}, {current_2}/{size_2}\n')
    return final

def action(index):
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
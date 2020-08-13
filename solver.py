'''Empty 1 - 0 
Empty 2 - 1
Fill 1 - 2
Fill 2 - 3
Fill 1 from 2 - 4
Fill 2 from 1 - 5

Kill conditions:

- If both are empty after performing an action, destroy that branch
- If both are full after performing an action, destroy that branch
- If a previous state (set at global level in the format [[<1>,<2>],...] is reached after performing an action, destroy that branch
- If either is the desired fill level, return that branch'''

def resolve_current(action_id, current_1, size_1, current_2, size_2, target, already_tried, path):
    if target in (current_1, current_2):
        print(f'Found a solution at path length {len(path)}; {current_1}/{size_1}, {current_2}/{size_2}')
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
    current_1 = 0
    #print(f'empty 1:{current_1}/{size_1}, {current_2}/{size_2}')
    #in theory there is no way you should ever reach a target by emptying a container
    #but i guess it's here anyways
    return resolve_current(0, current_1, size_1, current_2, size_2, target, already_tried, path)
def empty_2(current_1, size_1, current_2, size_2, target, already_tried, path):
    current_2 = 0
    #print(f'empty 2:{current_1}/{size_1}, {current_2}/{size_2}')
    return resolve_current(1, current_1, size_1, current_2, size_2, target, already_tried, path)
def fill_1(current_1, size_1, current_2, size_2, target, already_tried, path):
    current_1 = size_1
    #print(f'fill 1:{current_1}/{size_1}, {current_2}/{size_2}')
    return resolve_current(2, current_1, size_1, current_2, size_2, target, already_tried, path)
def fill_2(current_1, size_1, current_2, size_2, target, already_tried, path):
    print(f'fill 2:{current_1}/{size_1}, {current_2}/{size_2} - {len(path)}')
    current_2 = size_2
    print(f'fill 2:{current_1}/{size_1}, {current_2}/{size_2}')
    return resolve_current(3, current_1, size_1, current_2, size_2, target, already_tried, path)
def fill_1_from_2(current_1, size_1, current_2, size_2, target, already_tried, path):
    #print(f'1 from 2 start:{current_1}/{size_1}, {current_2}/{size_2}')
    if size_1 - current_1 > current_2:
        current_1 += current_2
        current_2 = 0
    else:
        current_2 -= size_1 - current_1
        current_1 = size_1
    #print(f'1 from 2 end:{current_1}/{size_1}, {current_2}/{size_2}')
    #print(f'1 from 2:{current_1}/{size_1}, {current_2}/{size_2}')
    return resolve_current(4, current_1, size_1, current_2, size_2, target, already_tried, path)
def fill_2_from_1(current_1, size_1, current_2, size_2, target, already_tried, path):
    if size_2 - current_2 > current_1:
        current_2 += current_1
        current_1 = 0
    else:
        current_1 -= size_2 - current_2
        current_2 = size_2
    #print(f'2 from 1:{current_1}/{size_1}, {current_2}/{size_2}')
    return resolve_current(5, current_1, size_1, current_2, size_2, target, already_tried, path)
def branch(current_1, size_1, current_2, size_2, target, already_tried, path):
    #print(f'{current_1}/{size_1}, {current_2}/{size_2}')
    a = empty_1(current_1, size_1, current_2, size_2, target, already_tried, path)
    if a:
        #print("returning a")
        return a
    b = empty_2(current_1, size_1, current_2, size_2, target, already_tried, path)
    if b:
        #print("returning b")
        return b
    c = fill_1(current_1, size_1, current_2, size_2, target, already_tried, path)
    if c:
        #print("returning c")
        return c
    d = fill_2(current_1, size_1, current_2, size_2, target, already_tried, path)
    if d:
        #print("returning d")
        return d
    e = fill_1_from_2(current_1, size_1, current_2, size_2, target, already_tried, path)
    if e:
        #print("returning e")
        return e
    f = fill_2_from_1(current_1, size_1, current_2, size_2, target, already_tried, path)
    if f:
        #print("returning f")
        return f
    else:
        return None

def solve(size_1, size_2, target):
    #below are always invalid and should always kill a branch
    invalid = [[0, 0], [size_1, size_2]]
    resulting_path = branch(0, size_1, 0, size_2, target, invalid, [])
    if resulting_path:
        turn_into_human_language(size_1, size_2, resulting_path)
        print(resulting_path)

def turn_into_human_language(size_1, size_2, final_path):
    current_1 = 0
    current_2 = 0
    print(f'Start: {current_1}/{size_1}, {current_2}/{size_2}')
    for element in final_path:
        action = element[0]
        current_1 = element[1]
        current_2 = element[2]

        if action == 0:
            current_1 = 0
            print(f'Empty container 1: {current_1}/{size_1}, {current_2}/{size_2}')
        elif action == 1:
            current_2 = 0
            print(f'Empty container 2: {current_1}/{size_1}, {current_2}/{size_2}')
        elif action == 2:
            current_1 = size_1
            print(f'Fill container 1 to full: {current_1}/{size_1}, {current_2}/{size_2}')
        elif action == 3:
            current_2 = size_2
            print(f'Fill container 2 to full: {current_1}/{size_1}, {current_2}/{size_2}')
        elif action == 4:
            if size_1 - current_1 > current_2:
                current_1 += current_2
                current_2 = 0
            else:
                current_2 -= size_1 - current_1
                current_1 = size_1
            print(f'Fill container 1 from 2: {current_1}/{size_1}, {current_2}/{size_2}')
        elif action == 5:
            if size_2 - current_2 > current_1:
                current_2 += current_1
                current_1 = 0
            else:
                current_1 -= size_2 - current_2
                current_2 = size_2
            print(f'Fill container 2 from 1: {current_1}/{size_1}, {current_2}/{size_2}')
    print(f'Target reached: {current_1}/{size_1}, {current_2}/{size_2}')


try:
    solve(7, 4, 3)
except RecursionError:
    print("failed...")

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

def empty_1(current_1, size_1, current_2, size_2, target, already_tried, path):
    current_1 = 0
    path.append([0, current_1, current_2, len(path)])
    #print(f'empty 1:{current_1}/{size_1}, {current_2}/{size_2}')
    #in theory there is no way you should ever reach a target by emptying a container
    #but i guess it's here anyways
    if target in (current_1, current_2):
        return path
    else:
        if [current_1, current_2] in already_tried:
            print(already_tried)
            print(f'killing {current_1}/{size_1}, {current_2}/{size_2} with a path length of {len(path)-1}')
            del path[-1]
            return None
        else:
            already_tried.append([current_1, current_2])
            result = branch(current_1, size_1, current_2, size_2, target, already_tried, path)
            if result:
                return result
def empty_2(current_1, size_1, current_2, size_2, target, already_tried, path):
    current_2 = 0
    path.append([1, current_1, current_2, len(path)])
    #print(f'empty 2:{current_1}/{size_1}, {current_2}/{size_2}')
    if target in (current_1, current_2):
        return path
    else:
        if [current_1, current_2] in already_tried:
            print(already_tried)
            print(f'killing {current_1}/{size_1}, {current_2}/{size_2} with a path length of {len(path)-1}')
            del path[-1]
            return None
        else:
            already_tried.append([current_1, current_2])
            result = branch(current_1, size_1, current_2, size_2, target, already_tried, path)
            if result:
                return result
def fill_1(current_1, size_1, current_2, size_2, target, already_tried, path):
    current_1 = size_1
    path.append([2, current_1, current_2, len(path)])
    #print(f'fill 1:{current_1}/{size_1}, {current_2}/{size_2}')
    if target in (current_1, current_2):
        return path
    else:
        if [current_1, current_2] in already_tried:
            print(already_tried)
            print(f'killing {current_1}/{size_1}, {current_2}/{size_2} with a path length of {len(path)-1}')
            del path[-1]
            return None
        else:
            already_tried.append([current_1, current_2])
            result = branch(current_1, size_1, current_2, size_2, target, already_tried, path)
            if result:
                return result
def fill_2(current_1, size_1, current_2, size_2, target, already_tried, path):
    current_2 = size_2
    path.append([3, current_1, current_2, len(path)])
    #print(f'fill 2:{current_1}/{size_1}, {current_2}/{size_2}')
    if target in (current_1, current_2):
        return path
    else:
        if [current_1, current_2] in already_tried:
            print(already_tried)
            print(f'killing {current_1}/{size_1}, {current_2}/{size_2} with a path length of {len(path)-1}')
            del path[-1]
            return None
        else:
            already_tried.append([current_1, current_2])
            result = branch(current_1, size_1, current_2, size_2, target, already_tried, path)
            if result:
                return result
def fill_1_from_2(current_1, size_1, current_2, size_2, target, already_tried, path):
    #print(f'1 from 2 start:{current_1}/{size_1}, {current_2}/{size_2}')
    if size_1 - current_1 > current_2:
        current_1 += current_2
        current_2 = 0
    else:
        current_2 -= size_1 - current_1
        current_1 = size_1
    path.append([4, current_1, current_2, len(path)])
    #print(f'1 from 2 end:{current_1}/{size_1}, {current_2}/{size_2}')
    #print(f'1 from 2:{current_1}/{size_1}, {current_2}/{size_2}')
    if target in (current_1, current_2):
        return path
    else:
        if [current_1, current_2] in already_tried:
            print(already_tried)
            print(f'killing {current_1}/{size_1}, {current_2}/{size_2} with a path length of {len(path)-1}')
            del path[-1]
            return None
        else:
            already_tried.append([current_1, current_2])
            result = branch(current_1, size_1, current_2, size_2, target, already_tried, path)
            if result:
                return result
def fill_2_from_1(current_1, size_1, current_2, size_2, target, already_tried, path):
    if size_2 - current_2 > current_1:
        current_2 += current_1
        current_1 = 0
    else:
        current_1 -= size_2 - current_2
        current_2 = size_2
    path.append([5, current_1, current_2, len(path)])
    #print(f'2 from 1:{current_1}/{size_1}, {current_2}/{size_2}')
    if target in (current_1, current_2):
        return path
    else:
        if [current_1, current_2] in already_tried:
            print(already_tried)
            print(f'killing {current_1}/{size_1}, {current_2}/{size_2} with a path length of {len(path)-1}')
            del path[-1]
            return None
        else:
            already_tried.append([current_1, current_2])
            result = branch(current_1, size_1, current_2, size_2, target, already_tried, path)
            if result:
                return result
def branch(current_1, size_1, current_2, size_2, target, already_tried, path):
    #print(f'{current_1}/{size_1}, {current_2}/{size_2}')
    a = empty_1(current_1, size_1, current_2, size_2, target, already_tried, path)
    b = empty_2(current_1, size_1, current_2, size_2, target, already_tried, path)
    c = fill_1(current_1, size_1, current_2, size_2, target, already_tried, path)
    d = fill_2(current_1, size_1, current_2, size_2, target, already_tried, path)
    e = fill_1_from_2(current_1, size_1, current_2, size_2, target, already_tried, path)
    f = fill_2_from_1(current_1, size_1, current_2, size_2, target, already_tried, path)
    #only ever return one
    if a:
        #print("returning a")
        return a
    elif b:
        #print("returning b")
        return b
    elif c:
        #print("returning c")
        return c
    elif d:
        #print("returning d")
        return d
    elif e:
        #print("returning e")
        return e
    elif f:
        #print("returning f")
        return f
    #else:
        #print("all branches failed")

def solve(size_1, size_2, target):
    #below are always invalid and should always kill a branch
    invalid = [[0, 0], [size_1, size_2]]
    resulting_path = branch(0, size_1, 0, size_2, target, invalid, [])
    if resulting_path:
        #turn_into_human_language(size_1, size_2, resulting_path)
        print(resulting_path)

def turn_into_human_language(size_1, size_2, final_path):
    current_1 = 0
    current_2 = 0
    print(f'Start: {current_1}/{size_1}, {current_2}/{size_2}')
    for action in final_path:
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

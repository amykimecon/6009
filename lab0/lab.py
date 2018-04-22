# Representation of a gas:
#
# gas_3 = { "width": 3,
#           "height": 4,
#           "state": [ ["w"], ["w"], ["w"],
#                      ["w"], ["r","l"], ["w"],
#                      ["w"], [ ], ["w"],
#                      ["w"], ["w","d"], ["w"] ] }

states = ["u","r","d","l"]

def step(gas):
    state = gas["state"]
    w = gas["width"]
    h = gas["height"]
    new_state = []
    for cell in state:
        if len(cell)>1:
            if "w" in cell:
                new_state.append(wall_collision(cell))
            else:
                new_state.append(particle_collision(cell))
        else:
            new_state.append(cell)

    new_state = propogate(new_state,w,h)
    gas["state"] = new_state
    return gas


def wall_collision(cell):
    result = []
    for elem in cell:
        if elem == "w":
            result.append(elem)
        else:
            result.append(states[(states.index(elem)+2)%4])
    return result

def particle_collision(cell):
    result = []
    if len(cell)==2:
        ind0 = states.index(cell[0])
        ind1 = states.index(cell[1])
        if (ind0 + ind1) % 2 == 0:
            result.append(states[(ind0 + 1)%4])
            result.append(states[(ind1 + 1)%4])
            return result
        else:
            return cell
    else:
        return cell


def propogate(state,width,height):
    new_state = []
    for elem in state:
        new_state.append([])
    for i in range(width*height):
        for elem in state[i]:
            if elem == "w":
                new_state[i].append("w")
            elif elem == "r":
                new_state[i+1].append("r")
            elif elem == "l":
                new_state[i-1].append("l")
            elif elem == "u":
                new_state[i-width].append("u")
            elif elem == "d":
                new_state[i+width].append("d")
    return new_state

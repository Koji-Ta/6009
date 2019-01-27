# Representation of a gas:
#
# gas_3 = { "width": 3,
#           "height": 4,
#           "state": [ ["w"], ["w"], ["w"],
#                      ["w"], ["r","l"], ["w"],
#                      ["w"], [ ], ["w"],
#                      ["w"], ["w","d"], ["w"] ] }

# opposite gas states, for a wall opposite state is a wall
opposite = {"l": "r", "r": "l", "u": "d", "d": "u", "w": "w"}
# state turned by 90 degree, need for collisions compute
turned = {"l": "u", "u": "r", "r": "d", "d": "l"}

def step(gas):
    """
    Compute next state of the gas
    
    Parameters
    ----------
    gas : dict
        Initial state of the gas

    Returns
    -------
    dict
        Next state of the gas.
    """
    after_collision = collide(gas)
    new_gas = propagate(after_collision)
    return new_gas


def collide(gas):
    """
    Compute collisions at the gas
    
    Parameters
    ----------
    gas : dict
        Gas befor collisions
        
    Returns
    -------
    dict
        Gas after collisions
    """
    state = gas["state"][:]
    for cell in state:
        # collisions with wall
        if 'w' in cell:
            for n, item in enumerate(cell):
                cell[n] = opposite[item]
        # pair collisions
        if len(cell) == 2 and opposite[cell[0]] == cell[1]:
            for n, item in enumerate(cell):
                cell[n] = turned[item]
    return {"width": gas["width"], 
            "height": gas["height"], 
            "state": state}


def propagate(gas):
    """
    Compute propagation at the gas
    
    Parameters
    ----------
    gas : dict
        Gas befor propagation
        
    Returns
    -------
    dict
        Gas after propagation
    """
    new_state = [[] for _ in range(gas["width"] * gas["height"])]
    for i, cell in enumerate(gas["state"]):
        for item in cell:
            new_index = get_index(i, item, gas)
            if 0 <= new_index < len(new_state):
                new_state[new_index].append(item)
    return {"width": gas["width"],
            "height": gas["height"],
            "state": new_state}


def get_index(index, item, gas):
    """
    Return index of the item in new stat of the gas
    
    Parameters
    ----------
    index : int
        Index of the item in the current gas state
    item : str
        Wall presents or particle direction
    gas : dict
        Current gas state
        
    Returns
    -------
    int
        Index of wall or particle in next gas state
    """
    if item == "w":
        new_index = index
    elif item == 'l':
        # left boundary check
        if index % gas["width"] == 0:
            new_index = -1
        else:
            new_index = index - 1
    elif item == "r":
        # right boundary check
        if index % gas["width"] == gas["width"] - 1:
            new_index = -1
        else:
            new_index = index + 1
    elif item == "u":
        new_index = index - gas["width"]
    elif item == "d":
        new_index = index + gas["width"]
    else:
        raise ValueError("Unknown cell state")
    # valid inexes in range from 0 to gas["width"] * gas["height"]
    return new_index

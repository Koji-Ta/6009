# Representation of a gas:
#
# gas_3 = { "width": 3,
#           "height": 4,
#           "state": [ ["w"], ["w"], ["w"],
#                      ["w"], ["r","l"], ["w"],
#                      ["w"], [ ], ["w"],
#                      ["w"], ["w","d"], ["w"] ] }

opposite = {"l": "r", "r": "l", "u": "d", "d": "u", "w": "w"}
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
    raise NotImplementedError

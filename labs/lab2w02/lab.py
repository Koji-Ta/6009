# NO IMPORTS ALLOWED!

import json

BACON_NUMBER = 4724

def did_x_and_y_act_together(data, actor_id_1, actor_id_2):
    """Do two actors play in the same move?"""
    for id_1, id_2, _ in data:
        if id_1 == actor_id_1 and id_2 == actor_id_2 or \
           id_1 == actor_id_2 and id_2 == actor_id_1:
            return True
    return False


def get_actor_id(data, name):
    """Return actor id in data by his/her name. Actor present in data"""
    return data[name]


def get_actor_name(data, actor_id):
    """Return actor name in data by his/her id. Actor present in data"""
    for name, other_id in data.items():
        if actor_id == other_id:
            return name


def get_actors_with_bacon_number(data, n):
    """Return set of actor ids with Bacon number of n"""
    # if Bacon number is 0 return Bacon id
    if n == 0:
        return {BACON_NUMBER}
    # actors graph is {actor_id: {set of other_actor_ids act with actor}}
    id_graph = get_actors_graph(data)
    id_set = closed = {BACON_NUMBER}
    for i in range(n):
        aux = set()
        for actor_id in id_set:
            aux |= set(id_graph[actor_id])
        id_set = aux - closed
        # if actors set empty stop computing
        if len(id_set) == 0:
            break
        closed |= id_set
    return id_set


def get_actors_graph(data):
    """Create graph of actors as {actor_id: {set of other_actor_id, which act with that actor}}"""
    actors_graph = {}
    for id_1, id_2, _ in data:
        for a, b in ((id_1, id_2), (id_2, id_1)):
            actors_graph.setdefault(a, set()).add(b)
    return actors_graph


def get_bacon_path(data, actor_id):
    """Create a list of actor ids detailing a Bacon path to actor_id"""
    id_graph = get_actors_graph(data)
    closed = set()
    add_fringe = set()
    # in fringe (id, path)
    fringe = {(BACON_NUMBER, (BACON_NUMBER,))}
    while not (len(fringe) == 0 and len(add_fringe) == 0):
        if len(fringe) == 0:
            fringe = add_fringe
            add_fringe = set()
        other_id, path = fringe.pop()
        if other_id == actor_id:
            return list(path)
        if other_id not in closed:
            closed.add(other_id)
            for new_id in id_graph[other_id]:
                new_path = path + (new_id,)
                add_fringe.add((new_id, new_path))
    return None


def get_path(data, actor_id_1, actor_id_2):
    raise NotImplementedError("Implement me!")

if __name__ == '__main__':
    with open('resources/small.json') as f:
        smalldb = json.load(f)

    with open('resources/large.json') as f:
        largedb = json.load(f)

    with open('resources/names.json') as f:
        names = json.load(f)

    print('Acting Together')
    actors = (('Barbara Flynn', 'Kurtwood Smith'),
              ('David Stevens', 'Folke Lind'),
              ('Dominique Reymond', 'Eduardo Yanez'),
              ('Chris Hogan', 'Charles Berling'))
    for actor_1, actor_2 in actors:
        print(f'Did {actor_1} and {actor_2} acted together?',
              did_x_and_y_act_together(smalldb,
                                       get_actor_id(names, actor_1),
                                       get_actor_id(names, actor_2)))
    print()
    print('Bacon Number')
    data = (('small', 3), ('small', 4), ('large', 5), ('large', 6))
    db = {'small': smalldb, 'large': largedb}
    for namedb, bacon_number in data:
        print(f'Set of actors with Bacon number {bacon_number} in the {namedb}.json:')
        print(', '.join(get_actor_name(names, actor_id)
            for actor_id in get_actors_with_bacon_number(db[namedb], bacon_number)))
    print()
    print('Bacon path')
    for actor in ('Karen Allen', 'Si Jenks', 'Iva Ilakovac'):
        print(f'Path of actors from Kevin Vacon to {actor} in large.json:')
        print(', '.join(get_actor_name(names, actor_id)
            for actor_id in get_bacon_path(largedb, get_actor_id(names, actor))))

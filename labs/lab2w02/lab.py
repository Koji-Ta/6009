# NO IMPORTS ALLOWED!

import json

def did_x_and_y_act_together(data, actor_id_1, actor_id_2):
    """Do two actors play in the same move?"""
    for id_1, id_2, _ in data:
        if id_1 == actor_id_1 and id_2 == actor_id_2 or \
           id_1 == actor_id_2 and id_2 == actor_id_1:
            return True
    return False


def get_actor_id(data, name):
    """Return actor id in data by his/her name"""
    return data[name]


def get_actors_with_bacon_number(data, n):
    raise NotImplementedError("Implement me!")

def get_bacon_path(data, actor_id):
    raise NotImplementedError("Implement me!")

def get_path(data, actor_id_1, actor_id_2):
    raise NotImplementedError("Implement me!")

if __name__ == '__main__':
    with open('resources/small.json') as f:
        smalldb = json.load(f)

    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    with open('resources/names.json') as f:
        names = json.load(f)

    print('Did Barbara Flynn and Kurtwood Smith acted together?',
          did_x_and_y_act_together(smalldb,
                                   get_actor_id(names, 'Barbara Flynn'),
                                   get_actor_id(names, 'Kurtwood Smith')))
    print('Did David Stevens and Folke Lind acted together?',
          did_x_and_y_act_together(smalldb,
                                   get_actor_id(names, 'David Stevens'),
                                   get_actor_id(names, 'Folke Lind')))
    print('Did Dominique Reymond and Eduardo Yanez acted together?',
          did_x_and_y_act_together(smalldb,
                                   get_actor_id(names, 'Dominique Reymond'),
                                   get_actor_id(names, 'Eduardo Yanez')))
    print('Did Chris Hogan and Charles Berling acted together?',
          did_x_and_y_act_together(smalldb,
                                   get_actor_id(names, 'Chris Hogan'),
                                   get_actor_id(names, 'Charles Berling')))

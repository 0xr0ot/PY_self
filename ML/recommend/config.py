##Example:

prefs = {
    'user1': {'goods1': 2.5, 'goods2': 3.5, 'goods3': 3.0, 'goods4': 3.5, 'goods5': 2.5, 'goods6': 3.0},
    'user2': {'goods1': 3.0, 'goods2': 3.5, 'goods3': 1.5, 'goods4': 5.0, 'goods5': 3.0, 'goods6': 3.5},
    'user3': {'goods1': 2.5, 'goods4': 3.5, 'goods6': 4.0},
    'user4': {'goods1': 3.5, 'goods3': 3.0},
    'vllen': {}
}


load_file(path):
	##todo
	pass


def transform(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            
            result[item][person] = prefs[person][item] ## transform
    return result

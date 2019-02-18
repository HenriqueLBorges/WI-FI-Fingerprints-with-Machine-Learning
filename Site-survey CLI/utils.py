def findInDict (list, key, value):
    cont = 0
    for dict in list:
        if dict[key] == value:
            return cont
        cont += 1
    return None
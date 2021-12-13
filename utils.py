
def clear_file(filename):
    with open(filename, 'w'):
        pass


def my_sorted(it, *, key=lambda x: x, reverse=False):

    for i in range(len(it)-1):
        for j in range(i+1, len(it)):
            if key(it[j]) < key(it[i]) and \
                    reverse is False:
                it[i], it[j] = it[j], it[i]
            if key(it[j]) > key(it[i]) and \
                    reverse is True:
                it[i], it[j] = it[j], it[i]
    return it

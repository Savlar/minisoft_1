import pickle


def save_data(filename, edges, vertices, options):
    with open(filename + '.pickle', 'wb') as output:
        pickle.dump([edges, vertices, options], output)


def load_data():
    with open('data.pickle', 'rb') as read:
        return pickle.load(read)

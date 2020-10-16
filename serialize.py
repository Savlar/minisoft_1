import pickle


def save_data(edges, vertices):
    with open('data.pickle', 'wb') as output:
        pickle.dump([edges, vertices], output)


def load_data():
    with open('data.pickle', 'rb') as read:
        return pickle.load(read)

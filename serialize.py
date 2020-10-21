import pickle
from tkinter import filedialog


def save_data(edges, vertices):
    file = filedialog.asksaveasfile("wb", filetypes=[("Serialized python structure",
                                                      "*.pickle")], defaultextension="*.pickle", )
    pickle.dump([edges, vertices], file)


def load_data(file_name):
    if file_name is None:
        file_name = './misc/data.pickle'
    with open(file_name, 'rb') as read:
        return pickle.load(read)

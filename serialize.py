import pickle
from tkinter import filedialog


def save_data(edges, vertices):
    file = filedialog.asksaveasfile("wb", filetypes=[("Serialized python structure",
                                                      "*.pickle")], defaultextension="*.pickle", initialdir="./misc")

    if file is not None and not isinstance(file, tuple):
        pickle.dump([edges, vertices], file)
    return file


def load_data(file_name):
    if file_name is None or file_name == '' or isinstance(file_name, tuple):
        file_name = './misc/data.pickle'
    with open(file_name, 'rb') as read:
        return pickle.load(read)

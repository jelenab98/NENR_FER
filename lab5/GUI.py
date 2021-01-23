import tkinter as tk
import numpy as np


class GenerateLettersApp(tk.Tk):
    """
    GUI for collection of Handwritten Greek letters dataset.
    """
    def __init__(self):

        tk.Tk.__init__(self)

        self.points_recorded = []
        self.all_points = {"alpha": [], "beta": [], "gamma": [], "delta": [], "epsilon": []}
        self.name = tk.StringVar()
        self.title("Handwritten Greek Letters Generator")
        self.canvas = tk.Canvas(self, width=600, height=600, bg="white", cursor="heart")
        self.var_states = tk.Label(self, text="alpha: {}, beta: {}, gamma: {}, delta: {}, epsilon: {}".format(
            len(self.all_points["alpha"]), len(self.all_points["beta"]), len(self.all_points["gamma"]),
            len(self.all_points["delta"]), len(self.all_points["epsilon"])), background='plum1')
        self.var_name = tk.Entry(self, width=15, textvariable=self.name, background="plum2")
        self.button_clear = tk.Button(self, text="Clear canvas", command=self.clear_all, background='plum4')
        self.button_save = tk.Button(self, text="Save canvas", command=self.save, background='plum3')

        self.set_up()

    def set_up(self):
        self.canvas.pack(side="top", fill="both", expand=True)
        self.var_states.pack(side='top', fill='both', expand=True)
        self.var_name.pack(side="top", fill="both", expand=True)
        self.button_save.pack(side="left", fill="both", expand=True)
        self.button_clear.pack(side="right", fill="both", expand=True)
        self.canvas.bind("<B1-Motion>", self.draw_from_where_you_are)

    def save(self):
        if self.name.get().lower() in ("alpha", "beta", "gamma", "delta", "epsilon"):
            print("Saving to {}".format(self.name.get()))
            self.all_points[self.name.get().lower()].append(self.points_recorded)
        self.var_states.configure(text="alpha: {}, beta: {}, gamma: {}, delta: {}, epsilon: {}".format(
            len(self.all_points["alpha"]), len(self.all_points["beta"]), len(self.all_points["gamma"]),
            len(self.all_points["delta"]), len(self.all_points["epsilon"])))

    def clear_all(self):
        self.canvas.delete("all")
        self.points_recorded = []

    def draw_from_where_you_are(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill="")
        self.points_recorded.append((event.x, event.y))


class ClassifierApp(tk.Tk):
    """
    GUI for classification of Handwritten Greek letters.
    """
    def __init__(self, model, data_set):
        tk.Tk.__init__(self)
        self.labels = {0: "alpha", 1: "beta", 2: "gamma", 3: "delta", 4: "epsilon"}
        self.model = model
        self.data_set = data_set
        self.points_recorded = []
        self.name = tk.StringVar()
        self.title("Handwritten Greek Letters Classifier")
        self.canvas = tk.Canvas(self, width=600, height=600, bg="white", cursor="heart")
        self.prediction = tk.Label(self, text="Predicted letter: {}".format(" "), background='plum1')
        self.var_states = tk.Label(self, text="alpha: {}, beta: {}, gamma: {}, delta: {}, epsilon: {}".format(
            0, 0, 0, 0, 0), background='plum2')
        self.button_clear = tk.Button(self, text="Clear canvas", command=self.clear_all, background='plum4')
        self.button_predict = tk.Button(self, text="Predict", command=self.predict, background='plum3')

        self.set_up()

    def set_up(self):
        self.canvas.pack(side="top", fill="both", expand=True)
        self.prediction.pack(side='top', fill='both', expand=True)
        self.var_states.pack(side='top', fill='both', expand=True)
        self.button_predict.pack(side="left", fill="both", expand=True)
        self.button_clear.pack(side="right", fill="both", expand=True)
        self.canvas.bind("<B1-Motion>", self.draw_from_where_you_are)

    def predict(self):
        self.data_set.process_for_test(self.points_recorded)
        x = self.data_set.X.reshape((1, 2*self.data_set.m))
        predictions = self.model.predict(x.T)
        max_lab = int(np.argmax(predictions))
        self.prediction.configure(text="Predicted letter: {}".format(self.labels[max_lab]))
        self.var_states.configure(text="alpha: {}, beta: {}, gamma: {}, delta: {}, epsilon: {}".format(
            predictions[0], predictions[1], predictions[2], predictions[3], predictions[4]))

    def clear_all(self):
        self.canvas.delete("all")
        self.prediction.configure(text="Predicted letter: {}".format(" "))
        self.var_states.configure(text="alpha: {}, beta: {}, gamma: {}, delta: {}, epsilon: {}".format(
            0, 0, 0, 0, 0))
        self.points_recorded = []

    def draw_from_where_you_are(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill="")
        self.points_recorded.append((event.x, event.y))

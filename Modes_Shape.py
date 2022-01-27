from tkinter import *
import function
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


def main():
    root = Tk()
    gui = Window(root, 0)
    gui.root.mainloop()
    return None


class Window:
    def __init__(self, root, local_or_global):
        self.root = root
        if local_or_global == 0:
            self.root.title("Mode Shapes")
            self.root.geometry("800x550")
        else:
            self.root.title("Discrete Oscillatory System")
            self.root.geometry("1600x850")

        self.degree_freedom = 3
        self.start_modes = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.modes = {
            "mod1": 0,
            "mod2": 0,
            "mod3": 0,
            "mod4": 0,
            "mod5": 0,
            "mod6": 0,
            "mod7": 0,
            "mod8": 0,
            "mod9": 0,
            "mod10": 0,
        }
        self.K_equivalent = 1500  # Stiffnes Equivalent in N/m
        self.M_equivalent = 1.5  # Mass Equivalent in Kg
        self.boundries = ["firm", "firm"]

        # Degree of Freedom
        Label(self.root, text="Degrees of freedom", font="Helvatica", background="#76b5c5").grid(row=0, column=0)
        self.degree_freedom_entry = Entry(self.root, width=5)
        self.degree_freedom_entry.grid(row=0, column=1, sticky=W)

        # Modes
        Label(self.root, text="Modes", font="Helvatica", background="#76b5c5").grid(row=0, column=3)
        dic_rows = {
            "mod1": 0,
            "mod2": 1,
            "mod3": 2,
            "mod4": 3,
            "mod5": 4,
            "mod6": 5,
            "mod7": 6,
            "mod8": 7,
            "mod9": 8,
            "mod10": 9,
        }

        for mod in self.modes:
            self.modes[mod] = IntVar()
            mod_checkbox = Checkbutton(self.root, text=mod, variable=self.modes[mod], background="#76b5c5")
            mod_checkbox.grid(row=dic_rows[mod] + 1, column=3)

        # Boundrie
        self.check = IntVar()
        firm_free = Checkbutton(self.root, text="Check for free boundrie", variable=self.check, background="#76b5c5", pady=10)
        firm_free.grid(row=0, column=2)

        # Update Button
        button1 = Button(self.root, text="Calculate", command=self.update_values, background="#abdbe3")
        button1.grid(row=11, column=3)
        self.root.bind("<Return>", self.update_values)
        self.plot_values()

        # Responsive
        self.root.grid_rowconfigure(11, weight=1)
        self.root.grid_columnconfigure(3, weight=1)
        self.root.configure(background="#76b5c5")

        pass

    def update_values(self, event=None):

    	#Update Degree of Freedom
        self.degree_freedom = int(self.degree_freedom_entry.get())

        #Update Modes to display
        self.modes_list = []
        for i in self.modes.values():
            self.modes_list.append(int(i.get()))

        self.start_modes = self.modes_list

        #Update border condition
        if int(self.check.get()) == 1:
            self.boundries = ["", ""]
        if int(self.check.get()) == 0:
            self.boundries = ["firm", "firm"]

        self.plot_values()

        return None

    def plot_values(self):
        figure = plt.figure()

        w, dmod = function.frecs_and_dmod(
            self.degree_freedom,
            self.K_equivalent,
            self.M_equivalent,
            BOUNDRIES=self.boundries,
        )
        x = np.linspace(0, 1, self.degree_freedom + 2)

        s = 300 * 1 / (self.degree_freedom / 2)  #Size of the scatter

        for index, i in enumerate(self.start_modes):
            if i == 1:
                plt.plot(x, dmod[index], label=f"Mode {index + 1}")
                plt.scatter(x[1:-1], dmod[index, 1:-1], s=s)

        display = FigureCanvasTkAgg(figure, master=self.root)
        display.get_tk_widget().grid(row=1, rowspan=10, column=0, columnspan=3)

        plt.legend()
        plt.axis('off')
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        figure.patch.set_facecolor("#bff2ff")

        return None

    pass


if __name__ == "__main__":
    main()

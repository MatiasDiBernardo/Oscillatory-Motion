from tkinter import *
import function
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


def main():
    root = Tk()
    gui = Window(root,0)
    gui.root.mainloop()
    return None


class Window:
    def __init__(self, root,local_or_global):
        self.root = root
        if local_or_global == 0:
            self.root.title("Discrete Oscillatory System Animation")
            self.root.geometry("810x800")
        

        self.num_dotes = 3
        self.current_amplitude = [0, 0]
        self.current_fase = [0, 0]

        # Number of Dots
        Label(self.root, text="Add  ", font="Helvetica", background="#76b5c5").grid(row=0, column=11, pady=5, sticky=W)
        Button(self.root, text="+", command=self.add_button, background='#abdbe3', height=2, width=4, font=('Arial',10)).grid(row=0, column=12, pady=5, sticky=W)
        Button(self.root, text="-", command=self.subtract_button, background='#abdbe3',height=2, width=4,font=('Arial',10)).grid(row=0, column=13, pady=5, sticky=W)


        # Animation Buttons
        Button(self.root, text="Start", command=self.start, background='#abdbe3').grid(row=2, column=11, pady=5)
        Button(self.root, text="Restart", command=self.restart, background='#abdbe3').grid(row=2, column=0, pady=5)
        Button(self.root, text="Stop", command=self.stop, background='#abdbe3').grid(row=2, column=12, pady=5)
        Label(self.root, text='', background='#76b5c5').grid(row=2,column=14)


        #Amplitude
        self.dicc_amplitudes = {
            "Amp 1": 0,
            "Amp 2": 0,
            "Amp 3": 0,
            "Amp 4": 0,
            "Amp 5": 0,
            "Amp 6": 0,
            "Amp 7": 0,
            "Amp 8": 0,
            "Amp 9": 0,
            "Amp 10": 0,
        }

        for i, amp in enumerate(self.dicc_amplitudes):

            amp_value = Scale(self.root, from_=1.0, to=0, resolution=0.1,background="#76b5c5")
            amp_value.grid(row=4, column=i, padx=10)

            self.dicc_amplitudes[amp] = amp_value

        #Fase
        self.dicc_fase = {
            "Fase 1": 0,
            "Fase 2": 0,
            "Fase 3": 0,
            "Fase 4": 0,
            "Fase 5": 0,
            "Fase 6": 0,
            "Fase 7": 0,
            "Fase 8": 0,
            "Fase 9": 0,
            "Fase 10": 0,
        }

        for i, fase in enumerate(self.dicc_fase):

            fase_value = Scale(self.root, from_=np.pi, to=-np.pi, resolution=0.1,background="#76b5c5")
            fase_value.grid(row=6, column=i,padx=10)

            self.dicc_fase[fase] = fase_value

        # Plot just two sliders
        self.subtract_button()

        # Responsive
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_columnconfigure(9, weight=1)
        self.root.configure(background="#76b5c5")

        # Update Button
        button1 = Button(self.root, text="Update", command=self.update_values, background='#abdbe3')
        button1.grid(row=2, column=13, pady=5)
        self.root.bind("<Return>", self.update_values)
        self.plot_values()
        pass

    def add_button(self):
        self.num_dotes += 1

        if self.num_dotes > 10:
            self.num_dotes = 10

        self.clear_text()
        self.show_only_active_slides_up(self.dicc_amplitudes, self.dicc_fase)
        self.list_text()

        self.update_values()

    def subtract_button(self):
        self.num_dotes -= 1

        if self.num_dotes < 1:
            self.num_dotes = 1

        self.clear_text()
        self.show_only_active_slides_down(self.dicc_amplitudes, self.dicc_fase)
        self.list_text()

        self.update_values()

    def list_text(self):
        self.text_modes = []
        self.text_fase = []

        if self.num_dotes > 0 and self.num_dotes < 11:
            for i in range(self.num_dotes):
                modes = Label(self.root, text= f'Mode {i + 1}',background="#76b5c5")
                modes.grid(row=3, column=i,padx=10)
                self.text_modes.append(modes)

            for i in range(self.num_dotes):
                fase = Label(self.root, text= f'Fase {i + 1}',background="#76b5c5")
                fase.grid(row=5, column=i,padx=10, sticky=S,pady=10)
                self.text_fase.append(fase)

    def clear_text(self):
        try:
            self.text_modes
        except AttributeError:
            start = False
        else:
            start = True

        if start:
            for i in range(len(self.text_modes)):
                self.text_modes[i].grid_forget()

            for j in range(len(self.text_fase)):
                self.text_fase[j].grid_forget()

    def show_only_active_slides_down(self, dicc1, dicc2):
        amp_values = list(dicc1.values())
        fase_values2 = list(dicc2.values())

        if self.num_dotes > 0:

            for i in range(1,11 - self.num_dotes):
                amp_values[-i].grid_forget()


            for i in range(1,11 - self.num_dotes):
                fase_values2[-i].grid_forget()

    def show_only_active_slides_up(self, dicc1,dicc2):
        amp_values = list(dicc1.values())
        amp_values2 = list(dicc2.values())

        if self.num_dotes < 11:
            amp_values[self.num_dotes - 1].grid(row=4, column=self.num_dotes - 1)
            amp_values2[self.num_dotes - 1].grid(row=6, column=self.num_dotes - 1)


    def start(self):
        self.ani = anim.FuncAnimation(self.fig, self.animation, interval=20)
        self.display.draw()

    def stop(self):
        self.ani.event_source.stop()

    def restart(self):
        self.ani.event_source.start()

    def oscilation(self, animation, num_free, w_nat, amplitude, fase):
        list_amplitud = []
        animation_rate = 1500
        new_dmod = self.dmod[:,1:-1]
        new_dmod = np.rot90(new_dmod) #Si no roto se modela la situación de borde libre

        for j in range(num_free):
            x1 = 0
            for i in range(num_free):
                x1 += (amplitude[i] * np.cos(w_nat[i] * (animation / animation_rate) + fase[i]) * new_dmod[j, i])
            list_amplitud.append(x1)

        list_amplitud.insert(0, 0)
        list_amplitud.append(0)

        return list_amplitud

    def animation(self, i):
        self.line.set_ydata(self.oscilation(i, self.num_dotes, self.w, self.current_amplitude, self.current_fase))

        return self.line

    def update_values(self, event=None):

        # Update Amplitude
        final_new_amplitud = []
        new_amplitudes = list(self.dicc_amplitudes.values())

        for i in range(self.num_dotes):
            final_new_amplitud.append((new_amplitudes[i].get()))

        self.current_amplitude = final_new_amplitud

        # Update Fase
        final_new_fase = []
        new_fase = list(self.dicc_fase.values())

        for i in range(self.num_dotes):
            final_new_fase.append((new_fase[i].get()))

        self.current_fase = final_new_fase

        self.plot_values()

        return None

    def plot_values(self):

        self.fig, ax = plt.subplots()
        x = np.linspace(0, 1, self.num_dotes + 2)

        self.w, self.dmod = function.frecs_and_dmod(self.num_dotes, 1500, 0.2)

        amplitud_of_points = self.oscilation(0, self.num_dotes, self.w, self.current_amplitude, self.current_fase)

        (self.line,) = ax.plot(x, amplitud_of_points, color='red', ls='dashed', marker='8', ms=12, mfc='green', mec='green', markevery=slice(1, self.num_dotes + 1))

        ax.set(title="Coupled Oscillator Animation", ylim=[-3, 3])
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        self.fig.patch.set_facecolor("#76b5c5")
        plt.axis('off')

        self.display = FigureCanvasTkAgg(self.fig, master=self.root)
        self.display.get_tk_widget().grid(row=0, rowspan=2, column=0, columnspan=10)

        return None

    pass

if __name__ == "__main__":
    main()

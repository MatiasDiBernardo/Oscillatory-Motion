from tkinter import *
import Modes_Shape
import Coupled_System_Animation

def main():
	main_root = Tk()
	
	modes_shape = Modes_Shape.Window(main_root,1)
	Label(main_root, text='   ',background="#76b5c5").grid(row=0,column=4)

	second_root = Frame(main_root)
	second_root.grid(row=0, column=5, rowspan=11)

	coupled_system = Coupled_System_Animation.Window(second_root,1)

	main_root.mainloop()

	return None

main()
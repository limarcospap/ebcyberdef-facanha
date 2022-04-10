from threading import Thread
import os
import datetime
from tkinter import *
import time
import subprocess

from numpy import var

class Checkbar(Frame):
   def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
      Frame.__init__(self, parent)
      self.vars = []
      for pick in picks:
         var = IntVar()
         chk = Checkbutton(self, text=pick, variable=var)
         chk.pack(side=side, anchor=anchor, expand=YES)
         self.vars.append(var)
   def state(self):
      return map((lambda var: var.get()), self.vars)
class radiobar(Frame):
	def __init__(self, parent=None, picks=[], side=LEFT, anchor=W,models=None):
		Frame.__init__(self, parent)
		
		self.var = [IntVar()]
		for val, model in enumerate(models):
			Radiobutton(self, 
		          text=model,
		          indicatoron = 0,
		          padx = 10, 
		          variable=self.var[0], 
		          value=val).pack(side=side, anchor=anchor, expand=YES)
	def state(self):
		return map((lambda var: var.get()), self.var)

	def ShowChoice(self):
		print((lambda var: var.get()), self.var)


class InterfacePFC:

	def __init__(self,models):
		self.is_running = False
		self.counter = 0
		self.finished= True
		self.models = models
		self.root = Tk()
		self.root.title("PFC_Facanha_Rebeca")
		#self.root.iconbitmap('eb_icon.ico')
		Label(self.root, text="Chose the commite classifiers:").pack()
		self.lng = Checkbar(self.root,self.models )
		self.lng.pack(side=TOP,  fill=X)
		self.lng.config(relief=GROOVE, bd=2)
		Label(self.root, text="Chose the classifier referee type:").pack()
		self.rad =  radiobar(parent=self.root,models=self.models)
		self.rad.pack(side=TOP,  fill=X)
		self.rad.config(relief=GROOVE, bd=2)

		Label(self.root, text="Number of subsets (cross val steps):").pack()	
		self.topframe = Frame(self.root)
		self.topframe.pack( side = TOP )
		self.bottomframe = Frame(self.root)
		self.bottomframe.pack( side = BOTTOM )
		Button(self.root, text='Run', command=self.run_comitte).pack(side=LEFT)
		Button(self.root, text='Quit', command=self.root.quit).pack(side=LEFT)
		
		self.n_splits_crossval = IntVar(self.root)
		self.n_splits_crossval.set(5) # default value
		w = OptionMenu(self.topframe, self.n_splits_crossval, 1,3,5,8,10,15,20)
		w.pack()

		self.root.mainloop()

	def results(self):
		path="C:\\Users\\gusta\\Desktop\\IME\\PFC\\EB-Cyber-Def-Facanha\\Results"
		path=os.path.realpath(path)
		os.startfile(path)

	def comitte_function(self,committe_models,referee_model,n_crossval):
		self.finished= False
		self.process = subprocess.Popen("python main.py {} {} {}".format(committe_models,referee_model,n_crossval))
		self.process.wait()
		self.is_running = False
		self.finished= True
		self.counter=0
	def comitte_stop(self):
		for child in self.bottomframe.winfo_children():
			child.destroy()
		self.process.kill()
		print ("process aborted!")

	def counter_label(self,label):
		def count():
			
			#posteriormente pode ser colocado um limite de tempo para forçar o fim da função 
			if not self.is_running and self.finished:
				self.counter=0
				self.bottomframe.winfo_children()[1].destroy()
				label.config(text="finished!")
				button = Button(self.bottomframe, text='Results', width=15, command=self.results)
				button.pack()
				return
			else:
				self.counter += 1
				timer=str(datetime.timedelta(seconds=self.counter))
				label.config(text="running...\n"+timer)
				label.after(1000, count)
		count()

	def run_comitte(self):
		if not self.is_running: 
			# committe models as string to pass as argument
			x = list(self.lng.state())
			x = [str(y) for y in x]
			committe_models = "["+','.join(x)+"]"	
			referee_model=int(list(self.rad.state())[0])
			n_splits_crossval = int(self.n_splits_crossval.get())
			print(committe_models,referee_model)
			thread = Thread(target = self.comitte_function, args = (committe_models,referee_model,n_splits_crossval))
			thread.start()

			#excluindo o "finished"
			if self.bottomframe.winfo_children():
				for child in self.bottomframe.winfo_children():
					child.destroy()
			label = Label(self.bottomframe, fg="red")
			label.pack()
			self.counter_label(label)
			button = Button(self.bottomframe, text='Stop', width=25, command=self.comitte_stop)
			button.pack()
			self.is_running = True

if __name__ == '__main__':
	#inserir um novo modelo na interface basta colocar nesta lista sua sigla
	# sempre inserir ao final para combinar com a main function
	models = ['DT', 'SVM', 'KNN', 'MLP','NB']
	InterfacePFC(models)
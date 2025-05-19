from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from ttkwidgets.autocomplete import AutocompleteEntry
from tkinter.scrolledtext import ScrolledText
from tkinter import Menu, StringVar, messagebox, ttk
import matplotlib.pyplot as plt
import TKinterModernThemes as tkmt
import beerGraph as bg
import tkinter as tk
import subprocess

class beerGUI:
	def __init__(self, cur, year):
		self.year = year
		self.cur = cur
		self.message = ""

		# Sets up the GUI's window
		self.window = tkmt.ThemedTKinterFrame("Beer", "Sun-valley", "dark")
		self.window.root.geometry("900x970+700+200")
		self.window.root.title("Beer GUI")
		self.window.root.bind('<Return>', self.oneBrandTotal)
		self.window.root.bind('<Escape>', self.close)
		self.scene = "drinking"
		
		# Autocomplete
		new = False
		self.autoComplete(new)

		# Calls swap scene to create default scene
		self.swapScene(self.scene)

		# Starts window mainloop to actually function
		self.window.root.mainloop()

# --------------- Scene Functions ------------------------------------------------------------------

	def prepDrinkingScene(self) -> None:
		# Title
		self.labelTitle = ttk.Label(
			self.window.root, text="Bierstatistik", font=('Bahnschrift', 26))
		self.labelTitle.pack(padx=5, pady=5)
		
		# Gridframe
		self.gridFrame = ttk.Frame(self.window.root)
		self.gridFrame.pack(expand=True, fill='both', side='left')

		# Logframe
		self.logFrame = ttk.Frame(self.window.root)
		self.logFrame.pack(expand=True, fill='both', side='left')

		# Log
		self.labelLog = ttk.Label(
			self.logFrame, text="Update Log", font=('Bahnschrift',20))
		self.labelLog.grid(row=0, column=0, pady=5)

		self.console = ScrolledText(
			self.logFrame, width=35 ,height=60, font=("consolas", "8", "normal"))
		self.console.grid(row=2, column=0, pady=5)
		self.console.configure(state="disabled")

		# Add button
		self.addButton = ttk.Button(
			self.gridFrame, text="Hinzufügen", command=self.openAddWindow, cursor="coffee_mug")
		self.addButton.grid(row=1, column=0, pady=5, columnspan=3)

		# Statistic buttons
		self.switchLabel = ttk.Label(
			self.gridFrame, text="Statistik-Graphen", font=("Bahnschrift", 16))
		self.switchLabel.grid(row=2, column=1, pady=5)

		self.button1 = ttk.Button(
			self.gridFrame, text='Bierposts pro Jahr', command=self.postPerYear)
		self.button1.grid(row=3, column=0)
		self.button2 = ttk.Button(
			self.gridFrame, text='Top 10 Posters Total', command=self.beerWinnerTotal)
		self.button2.grid(row=3, column=1)
		self.button3 = ttk.Button(
			self.gridFrame, text='Top 10 Poster des Jahres', command=self.beerWinner)
		self.button3.grid(row=3, column=2)
		self.button4 = ttk.Button(
			self.gridFrame, text='Excel: Poster alle Jahre ', command=self.beerPosterAllYear)
		self.button4.grid(row=4, column=0)
		self.button5 = ttk.Button(
			self.gridFrame, text='Top 10 Biermarken des Jahres', command=self.brandsLastYear)
		self.button5.grid(row=4, column=1)
		self.button6= ttk.Button(
			self.gridFrame, text='Top 10 Biermarken Total', command=self.brandsTotal)
		self.button6.grid(row=4, column=2)
		
		# Graph figure
		self.fig = plt.figure(figsize=(5,6))

		self.canvas = FigureCanvasTkAgg(self.fig, master=self.gridFrame)
		self.canvas.draw()
		self.canvas.get_tk_widget().grid(row=8, column=0, columnspan=4, pady=20)

		# Navigation toolbar
		self.toolbarFrame = tk.Frame(master=self.gridFrame)
		self.toolbarFrame.grid(row=7,column=0, columnspan=3)
		self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)

		# Search Brand Graph Entry
		self.labelBrandSearch = ttk.Label(self.gridFrame, text="Marke je Jahre: ", font=('Bahnschrift', 20))
		self.labelBrandSearch.grid(row=6, column=0, pady=5)

		self.brandSearchvar = StringVar(self.window.root)
		self.brandSeachEntry = AutocompleteEntry(
			self.gridFrame, textvariable=self.brandSearchvar, completevalues=self.listOfBrands)
		self.brandSeachEntry.grid(row=6, column=1, pady=5)

		# Exit button
		self.button_quit = ttk.Button(self.logFrame, text="Aus", command=self.window.root.destroy)
		self.button_quit.grid(row=4, column=0, pady=10)

		self.gridFrame.pack(padx=10, pady=10)

# --------------- Start Functions ------------------------------------------------------------------

	def startDrinking(self, event):
		if self.brandvar.get() == "" or self.brandvar.get() == " ":
			self.missing()
		else:	
			args = [
			"python", "beerStatistic.py",
			"--brand", str(self.brandvar.get()), 
			"--name", str(self.namevar.get())
			]	
			self.output = subprocess.run(args, capture_output=True, text=True)
			self.printLog()
			
			if "Insert" in self.output.stdout:
				new = True
				self.autoComplete(new)
				
			self.nameEntry.delete(0, 'end')
			self.brandEntry.delete(0, 'end')
			
	def swapScene(self, scene: str) -> None:
		for widget in self.window.root.winfo_children():
			if not isinstance(widget, Menu):
				widget.destroy()
		self.scene = scene
		if scene == "drinking":
			self.prepDrinkingScene()

# ---------------- Open New Window for Adding-----------------------------------------------------	

	# Opens a new window with brand and name fields to add
	def openAddWindow(self):
		self.newWindow = tk.Toplevel(self.window.root)

		self.newWindow.title = ("Hinzufügen")
		self.newWindow.geometry("300x100+900+500")

		# Window Frame
		self.windowFrame = ttk.Frame(self.newWindow)
		self.windowFrame.pack(expand=True, fill='both', side='left')

		# Brand entry
		self.labelBrand = ttk.Label(self.windowFrame, text="Marke: ", font=('Bahnschrift', 20))
		self.labelBrand.grid(row=0, column=0, pady=5)
		self.brandvar = StringVar(self.newWindow)
		self.brandEntry = AutocompleteEntry(
			self.windowFrame, textvariable=self.brandvar, completevalues=self.listOfBrands)
		self.brandEntry.grid(row=0, column=1, pady=5)

		# Name entry
		self.labelName = ttk.Label(self.windowFrame, text="Poster: ", font=('Bahnschrift', 20))
		self.labelName.grid(row=1, column=0, pady=5)
		self.namevar = StringVar(self.newWindow)
		self.nameEntry = AutocompleteEntry(
			self.windowFrame, textvariable=self.namevar, completevalues=self.listOfDrinkers)
		self.nameEntry.grid(row=1, column=1, pady=5)

		self.newWindow.bind('<Return>', self.startDrinking)
		self.newWindow.bind('<Escape>', self.closeAddWindow)

	# Refreshes the add window so the autocomplete lists are updated
	def refreshAddWindow(self):
		# Brand entry
		self.labelBrand = ttk.Label(self.windowFrame, text="Marke: ", font=('Bahnschrift', 20))
		self.labelBrand.grid(row=0, column=0, pady=5)
		self.brandvar = StringVar(self.newWindow)
		self.brandEntry = AutocompleteEntry(
			self.windowFrame, textvariable=self.brandvar, completevalues=self.listOfBrands)
		self.brandEntry.grid(row=0, column=1, pady=5)

		# Name entry
		self.labelName = ttk.Label(self.windowFrame, text="Poster: ", font=('Bahnschrift', 20))
		self.labelName.grid(row=1, column=0, pady=5)
		self.namevar = StringVar(self.newWindow)
		self.nameEntry = AutocompleteEntry(
			self.windowFrame, textvariable=self.namevar, completevalues=self.listOfDrinkers)
		self.nameEntry.grid(row=1, column=1, pady=5)

	# Closes the add window
	def closeAddWindow(self, event):
		self.newWindow.destroy()
		
# -------------- Graph functions -----------------------------------------------------------------	

	# Returns a graph of overall posts per year
	def postPerYear(self):
		plt.clf()

		self.bar, self.ylabel, self.title= bg.postPerYear(self.cur)
		
		self.canvas.draw()
		self.canvas.get_tk_widget().grid(row=8, column=0, columnspan=4, pady=5)
		self.window.root.mainloop()

	# Returns graph of the beer posts last year per person
	def beerWinner(self):
		plt.clf()

		self.bar, self.sticky, self.ylabel, self.title, self.message = bg.beerWinner(self.cur, self.year)
		self.printLog()

		self.canvas.draw()
		self.canvas.get_tk_widget().grid(row=8, column=0, columnspan=4, pady=5)
		self.window.root.mainloop()
	
	# Returns graph of the beer posts per person
	def beerWinnerTotal(self):
		plt.clf()

		self.bar, self.sticky, self.ylabel, self.title, self.message = bg.beerWinnerTotal(self.cur, self.year)
		self.printLog()

		self.canvas.draw()
		self.canvas.get_tk_widget().grid(row=8, column=0, columnspan=4, pady=5)
		self.window.root.mainloop()

	# Returns Excel file with all years of drinkers' posts
	def beerPosterAllYear(self):

		self.message = bg.beerPosterAllYear(self.cur, self.year)
		self.printLog()

	# Returns a graph with all brands of the last year
	def brandsLastYear(self):
		plt.clf()

		self.bar, self.sticky, self.ylabel, self.title, self.message = bg.brandsLastYear(self.cur, self.year)
		self.printLog()

		self.canvas.draw()
		self.canvas.get_tk_widget().grid(row=8, column=0, columnspan=4, pady=5)
		self.window.root.mainloop()

	# Returns a graph with all brands over the years
	def brandsTotal(self):
		plt.clf()

		self.bar, self.sticky, self.ylabel, self.title, self.message = bg.brandsTotal(self.cur)
		self.printLog()

		self.canvas.draw()
		self.canvas.get_tk_widget().grid(row=8, column=0, columnspan=4, pady=5)
		self.window.root.mainloop()

	# Returns a graph of one beer brand over the years
	def oneBrandTotal(self, event):
		if self.brandSearchvar.get() == "" or self.brandSearchvar.get() == " ":
			self.missing()	
		else:
			plt.clf()

			self.bar, self.sticky, self.ylabel, self.title = bg.oneBrandTotal(
				self.cur, self.brandSearchvar.get())

			self.canvas.draw()
			self.canvas.get_tk_widget().grid(row=8, column=0, columnspan=4, pady=5)
			self.window.root.mainloop()

# -------------helper functions --------------------------------------------------------------------------	

	# Error message when brand is empty
	def missing(self):
		messagebox.showinfo(title="Fehler", message="Biermarke fehlt")

	# Writes the Update log
	def printLog(self):
		self.console.configure(state="normal")  # make field editable
		if self.message != "":
			self.message += "\n"
			self.console.insert("end", self.message)
			self.message = ""
		else:
			self.console.insert("end", self.output.stdout) 
		self.console.see("end")  # scroll to end
		self.console.configure(state="disabled")

	# Initiates and refreshes the autocomplete lists
	def autoComplete(self, new):
		# Autocomplete for brand names
		brands = self.cur.execute("Select distinct brand from beers")
		self.listOfBrands = []
		for rec in brands.fetchall():
			self.listOfBrands.append(rec[0])

		# Autocomplete for poster names
		names = self.cur.execute("Select distinct name from names")
		self.listOfDrinkers = []
		for rec in names.fetchall():
			self.listOfDrinkers.append(rec[0])
		if new:
			self.refreshAddWindow()
			
	# Closes the main window		
	def close(self, event):
		exit()
import json
import requests
from tkinter import *

basis_api_link = "https://opendata.rdw.nl/resource/m9d7-ebf2.json?kenteken="
brandstof_api_link = "https://opendata.rdw.nl/resource/8ys7-d773.json?kenteken="

class Application():
	def __init__(self, master):
		self.master = master
		self.master.geometry("700x700")

		self.create_widgets()


	def create_widgets(self):
		self.input_field = Entry(self.master)
		self.input_field.place(x=280,y=12)

		button = Button(self.master, text="Search", command=self.show_data)
		button.place(x=420, y=10)

		self.v = IntVar()
		self.v.set(1)
		Radiobutton(self.master, text="Basis ", variable=self.v, command=self.show_data, indicatoron=0, value=1).place(x=0, y=50)
		Radiobutton(self.master, text="Verval APK ", variable=self.v, command=self.show_data, indicatoron=0, value=2).place(x=40, y=50)
		Radiobutton(self.master, text="Brandstof ", variable=self.v, command=self.show_data, indicatoron=0, value=3).place(x=110, y=50)

		self.text = Text(self.master)
		self.text.place(x=0, y=75, height=630, width=700)


	def search_license(self, api_link, integer):
		license = self.input_field.get()
		license = license.replace("-", "")
		license = license.upper()

		if license == "":
			return

		api_info = requests.get(api_link + license)
		api_info = api_info.json()
		api_info = api_info[0]

		if integer != 2:
			pretty_text = ""
			for thing in api_info:
				pretty_text += f"{thing}: {api_info[thing]} \n"

		elif integer == 2:
			pretty_text = "vervaldatum_apk: {}".format(api_info["vervaldatum_apk"])

		return pretty_text


	def show_data(self):
		radio_button = self.v.get()

		if radio_button == 1 or radio_button == 2:
			api_info = self.search_license(basis_api_link, radio_button)
			if api_info == None:
				return

			self.text.delete(1.0, "end")
			self.text.insert(1.0, api_info)

		else:
			api_info = self.search_license(brandstof_api_link, radio_button)
			if api_info == None:
				return

			self.text.delete(1.0, "end")
			self.text.insert(1.0, api_info)


root = Tk()
Application(root)
root.mainloop()
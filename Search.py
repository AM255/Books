import tkinter as tk
from tkinter import simpledialog
import tkinter.ttk as ttk
import requests
import csv
from datetime import datetime
import os

class BookSearchGUI:

	def __init__(self, root):
		self.root = root
		self.root.title("Book Search")

		# Get the width and height of the screen
		screen_width = self.root.winfo_screenwidth()
		screen_height = self.root.winfo_screenheight()

		# Calculate the position of the window based on the screen size
		window_width = 353
		window_height = 300
		window_x = (screen_width - window_width) // 2
		window_y = (screen_height - window_height) // 2

		# Set the window's position using the geometry() method
		self.root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

		# Create an empty list to store the book information
		self.book_history = []
		self.book_history_json = []

		# Get the current date and time
		self.date_entered = datetime.now().strftime('%Y-%m-%d')

		tk.Label(text="Title:").grid(row=0, column=0, sticky=tk.W)
		tk.Label(text="Author:").grid(row=1, column=0, sticky=tk.W)
		tk.Label(text="Rating:").grid(row=2, column=0, sticky=tk.W)

		self.title_entry = tk.Entry()
		self.author_entry = tk.Entry()
		self.rating_entry = tk.Entry()

		self.title_entry.grid(row=0, column=1, padx=5, pady=5)
		self.author_entry.grid(row=1, column=1, padx=5, pady=5)
		self.rating_entry.grid(row=2, column=1, padx=5, pady=5)

		self.search_button = ttk.Button(text="Search", command=self.search)
		self.search_button.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
		self.root.bind('<Return>', lambda event: self.search_button.invoke())

		self.title_entry.focus_set()

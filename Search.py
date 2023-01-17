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
	def search(self):
		# Get the book title and author from the entry fields
		book_title = self.title_entry.get()
		book_author = self.author_entry.get()
		book_rating = self.rating_entry.get()

		# Make a request to the Open Library API to search for the book by its title and author
		response = requests.get(
		 f'https://openlibrary.org/search.json?title={book_title}&author={book_author}'
		)

		# Convert the response from JSON to a Python dictionary
		results = response.json()

		# Extract the first result from the results
		book = results['docs'][0]

		# Store the book information in a dictionary
		self.book_data = {
		 'Title':
		 book['title'],
		 'Author':
		 book['author_name'][0],
		 'Language':
		 book['language'][0] if 'language' in book else None,
		 'Date':
		 self.date_entered,
		 'Rating':
		 book_rating,
		 'Publish year':
		 book['publish_year'][-1] if 'publish_year' in book else None,
		 'Number pages':
		 book['number_of_pages_median']
		 if 'number_of_pages_median' in book else None,
		 'Key':
		 book['key'] if 'key' in book else None
		}

		# Open a new window to edit the data
		self.edit_window = tk.Toplevel(self.root)
		self.edit_window.title("Edit")

		# Create labels and entry widgets for each column
		tk.Label(self.edit_window, text="Title:").grid(row=0, column=0, sticky=tk.W)
		tk.Label(self.edit_window, text="Author:").grid(row=1, column=0, sticky=tk.W)
		tk.Label(self.edit_window, text="Language:").grid(row=2,column=0,sticky=tk.W)
		tk.Label(self.edit_window, text="Date:").grid(row=3, column=0, sticky=tk.W)
		tk.Label(self.edit_window, text="Rating:").grid(row=4, column=0, sticky=tk.W)
		tk.Label(self.edit_window, text="Publish Year:").grid(row=5,column=0,sticky=tk.W)
		tk.Label(self.edit_window, text="Number Pages:").grid(row=6,column=0,sticky=tk.W)
		tk.Label(self.edit_window, text="Key:").grid(row=7, column=0, sticky=tk.W)
		self.title_entry = tk.Entry(self.edit_window)
		self.author_entry = tk.Entry(self.edit_window)
		self.language_entry = tk.Entry(self.edit_window)
		self.date_entry = tk.Entry(self.edit_window)
		self.rating_entry = tk.Entry(self.edit_window)
		self.publish_year_entry = tk.Entry(self.edit_window)
		self.number_pages_entry = tk.Entry(self.edit_window)
		self.key_entry = tk.Entry(self.edit_window)
		self.title_entry.grid(row=0, column=1, padx=5, pady=5)
		self.author_entry.grid(row=1, column=1, padx=5, pady=5)
		self.language_entry.grid(row=2, column=1, padx=5, pady=5)
		self.date_entry.grid(row=3, column=1, padx=5, pady=5)
		self.rating_entry.grid(row=4, column=1, padx=5, pady=5)
		self.publish_year_entry.grid(row=5, column=1, padx=5, pady=5)
		self.number_pages_entry.grid(row=6, column=1, padx=5, pady=5)
		self.key_entry.grid(row=7, column=1, padx=5, pady=5)

		# Pre-populate the entry widgets with the data from the selected row
		self.title_entry.insert(0, (self.book_data["Title"]))
		self.author_entry.insert(0, (self.book_data["Author"]))
		self.language_entry.insert(0, (self.book_data["Language"]))
		self.date_entry.insert(0, (self.book_data["Date"]))
		self.rating_entry.insert(0, (self.book_data["Rating"]))
		self.publish_year_entry.insert(0, (self.book_data["Publish year"]))
		self.number_pages_entry.insert(0, (self.book_data["Number pages"]))
		self.key_entry.insert(0, (self.book_data["Key"]))

		# Create a save button
		self.add_button = tk.Button(self.edit_window, text="Add", command=self.add)
		self.add_button.grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)

		# Create a cancel button
		self.done_button = tk.Button(self.edit_window,text="Done",command=self.edit_window.destroy)
		self.done_button.grid(row=8, column=1, padx=5, pady=5, sticky=tk.E)
	def add(self):
		# Get the data from the entry widgets
		book_data = {
		 'Title': self.title_entry.get(),
		 'Author': self.author_entry.get(),
		 'Language': self.language_entry.get(),
		 'Date': self.date_entry.get(),
		 'Rating': self.rating_entry.get(),
		 'Publish year': self.publish_year_entry.get(),
		 'Number pages': self.number_pages_entry.get(),
		 'Key': self.key_entry.get()
		}

		# Add the book data to the book history lists
		self.book_history.append(book_data)
		self.book_history_json.append(book_data)

		file_path = 'book_history.csv'
		# Check if the file exists
		if not os.path.exists(file_path):
			# The file does not exist, so write the header row
			with open(file_path, 'w', newline='') as csvfile:
				fieldnames = [
				 'Title', 'Author', 'Language', 'Date', 'Rating', 'Publish year',
				 'Number pages', 'Key'
				]
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
				writer.writeheader()
				for book in self.book_history:
					writer.writerow(book)
		else:
			# The file already exists, so write the data to the file
			with open(file_path, 'a', newline='') as csvfile:
				fieldnames = [
				 'Title', 'Author', 'Language', 'Date', 'Rating', 'Publish year',
				 'Number pages', 'Key'
				]
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
				for book in self.book_history:
					writer.writerow(book)

		# Close the edit window
		self.edit_window.destroy()

		# Close the main window
		self.root.destroy()
if __name__ == "__main__":
	# Create the root window and the BookSearchGUI instance
	root = tk.Tk()
	app = BookSearchGUI(root)

	# Run the main loop to display the GUI
	root.mainloop()

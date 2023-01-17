import tkinter as tk
import tkinter.ttk as ttk
import csv

class BookViewerGUI:

	def __init__(self, root):
		self.root = root
		self.root.title("Book Viewer")

		# Get the width and height of the screen
		screen_width = self.root.winfo_screenwidth()
		screen_height = self.root.winfo_screenheight()

		# Calculate the position of the window based on the screen size
		window_width = 900
		window_height = 500
		window_x = (screen_width - window_width) // 2
		window_y = (screen_height - window_height) // 2

		# Set the window's position using the geometry() method
		self.root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

		# Hardcode the file path of the CSV file
		self.file_path = "book_history.csv"

		# Create a frame to hold the table
		self.output_frame = tk.Frame(self.root)
		self.output_frame.pack(side="top", fill="both", expand=True)

		# Create a treeview widget to display the CSV data
		self.table = tk.ttk.Treeview(self.output_frame)
		self.table["columns"] = ("title", "author", "language", "date", "rating",
		                         "publish_year", "number_pages", "key")
		self.table.column("#0", width=0, minwidth=0, stretch=tk.NO)
		self.table.column("title", width=50, minwidth=10, stretch=tk.YES)
		self.table.column("author", width=50, minwidth=10, stretch=tk.YES)
		self.table.column("language", width=10, minwidth=10, stretch=tk.YES)
		self.table.column("date", width=10, minwidth=10, stretch=tk.YES)
		self.table.column("rating", width=10, minwidth=10, stretch=tk.YES)
		self.table.column("publish_year", width=10, minwidth=10, stretch=tk.YES)
		self.table.column("number_pages", width=10, minwidth=10, stretch=tk.YES)
		self.table.column("key", width=50, minwidth=10, stretch=tk.YES)
		self.table.heading("#0", anchor=tk.W)
		self.table.heading("title", text="Title", anchor=tk.W)
		self.table.heading("author", text="Author", anchor=tk.W)
		self.table.heading("language", text="Language", anchor=tk.W)
		self.table.heading("date", text="Date", anchor=tk.W)
		self.table.heading("rating", text="Rating", anchor=tk.W)
		self.table.heading("publish_year", text="Publish Year", anchor=tk.W)
		self.table.heading("number_pages", text="Number Pages", anchor=tk.W)
		self.table.heading("key", text="Key", anchor=tk.W)
		self.table.pack(side="top", fill="both", expand=True)

		# Create a scrollbar for the treeview widget
		self.scrollbar = tk.ttk.Scrollbar(self.output_frame,
		                                  orient="vertical",
		                                  command=self.table.yview)
		self.scrollbar.pack(side="right", fill="y")
		self.table.configure(yscrollcommand=self.scrollbar.set)

		# Open the CSV file and read the data
		with open(self.file_path, newline='') as csv_file:
			csv_reader = csv.DictReader(csv_file)

			# Insert the data into the treeview widget
			for row in csv_reader:
				self.table.insert("", "end", values=tuple(row.values()))

		# Bind the edit method to a double-click event on the treeview widget
		self.table.bind("<Double-1>", self.edit)

	def edit(self, event=None):
		# Get the selected item in the treeview widget
		self.item = self.table.focus()

		# Open a new window to edit the data
		self.edit_window = tk.Toplevel(self.root)
		self.edit_window.title("Edit")

		# Create labels and entry widgets for each column
		tk.Label(self.edit_window, text="Title:").grid(row=0, column=0, sticky=tk.W)
		tk.Label(self.edit_window, text="Author:").grid(row=1, column=0, sticky=tk.W)
		tk.Label(self.edit_window, text="Language:").grid(row=2,
		                                                  column=0,
		                                                  sticky=tk.W)
		tk.Label(self.edit_window, text="Date:").grid(row=3, column=0, sticky=tk.W)
		tk.Label(self.edit_window, text="Rating:").grid(row=4, column=0, sticky=tk.W)
		tk.Label(self.edit_window, text="Publish Year:").grid(row=5,
		                                                      column=0,
		                                                      sticky=tk.W)
		tk.Label(self.edit_window, text="Median Number Pages:").grid(row=6,
		                                                             column=0,
		                                                             sticky=tk.W)
		self.title_entry = tk.Entry(self.edit_window)
		self.author_entry = tk.Entry(self.edit_window)
		self.language_entry = tk.Entry(self.edit_window)
		self.date_entry = tk.Entry(self.edit_window)
		self.rating_entry = tk.Entry(self.edit_window)
		self.publish_year_entry = tk.Entry(self.edit_window)
		self.number_pages_entry = tk.Entry(self.edit_window)
		self.title_entry.grid(row=0, column=1, padx=5, pady=5)
		self.author_entry.grid(row=1, column=1, padx=5, pady=5)
		self.language_entry.grid(row=2, column=1, padx=5, pady=5)
		self.date_entry.grid(row=3, column=1, padx=5, pady=5)
		self.rating_entry.grid(row=4, column=1, padx=5, pady=5)
		self.publish_year_entry.grid(row=5, column=1, padx=5, pady=5)
		self.number_pages_entry.grid(row=6, column=1, padx=5, pady=5)

		# Pre-populate the entry widgets with the data from the selected row
		self.title_entry.insert(0, self.table.item(self.item, "values")[0])
		self.author_entry.insert(0, self.table.item(self.item, "values")[1])
		self.language_entry.insert(0, self.table.item(self.item, "values")[2])
		self.date_entry.insert(0, self.table.item(self.item, "values")[3])
		self.rating_entry.insert(0, self.table.item(self.item, "values")[4])
		self.publish_year_entry.insert(0, self.table.item(self.item, "values")[5])
		self.number_pages_entry.insert(0, self.table.item(self.item, "values")[6])

		# Create a save button
		self.save_button = tk.Button(self.edit_window,
		                             text="Save",
		                             command=self.save_edit)
		self.save_button.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)

		# Create a cancel button
		self.cancel_button = tk.Button(self.edit_window,
		                               text="Cancel",
		                               command=self.edit_window.destroy)
		self.cancel_button.grid(row=7, column=1, padx=5, pady=5, sticky=tk.E)
	
	def save_edit(self):
		# Get the data from the entry widgets
		new_values = [
		 self.title_entry.get(),
		 self.author_entry.get(),
		 self.language_entry.get(),
		 self.date_entry.get(),
		 self.rating_entry.get(),
		 self.publish_year_entry.get(),
		 self.number_pages_entry.get(),
		]

		# Update the data in the treeview widget
		self.table.item(self.item, values=tuple(new_values))

		# Write the updated data back to the CSV file
		with open(self.file_path, "w", newline='') as csv_file:
			csv_writer = csv.DictWriter(csv_file,
			                            fieldnames=[
			                             "title", "author", "language", "date",
			                             "rating", "publish_year", "number_pages", "key"
			                            ])
			csv_writer.writeheader()
			for row in self.table.get_children():
				values = self.table.item(row)["values"]
				csv_writer.writerow({
				 "title": values[0],
				 "author": values[1],
				 "language": values[2],
				 "date": values[3],
				 "rating": values[4],
				 "first_publish_year": values[5],
				 "number_pages": values[6],
				})

		# Close the edit window
		self.edit_window.destroy()
if __name__ == "__main__":
	# Create a root window
	root = tk.Tk()

	# Create an instance of the BookViewerGUI class
	app = BookViewerGUI(root)

	# Run the main loop
	root.mainloop()

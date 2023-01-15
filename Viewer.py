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

		# Create a Label widget to display text at the bottom left of the window
		self.text_label = tk.Label(self.root, text="Credit to Clara Kwin")
		self.text_label.pack(side="left", anchor="sw")

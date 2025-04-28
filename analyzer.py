import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd

class MovieAnalyzer:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.df = self._load_data() if file_path else None

    def _load_data(self):
        """
        Loads movie data from the CSV file.
        """
        try:
            df = pd.read_csv(self.file_path)
            return df
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return None

    def get_movie_count(self):
        if self.df is not None:
            return len(self.df)
        return 0

    def get_genre_counts(self):
        if self.df is not None and "Genre" in self.df.columns:
            return self.df["Genre"].value_counts()
        return pd.Series()

    def get_average_rating_by_genre(self):
        if self.df is not None and "Genre" in self.df.columns and "Rating" in self.df.columns:
            return self.df.groupby("Genre")["Rating"].mean()
        return pd.Series()

    def get_top_n_movies(self, n=5):
        if self.df is not None and "Rating" in self.df.columns:
            return self.df.sort_values(by="Rating", ascending=False).head(n)
        return pd.DataFrame()

    def get_movies_by_genre(self, genre):
        if self.df is not None and "Genre" in self.df.columns:
            return self.df[self.df["Genre"] == genre]
        return pd.DataFrame()


class MovieAnalyzerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Analyzer")
        
        # File selection button
        self.file_path = None
        self.analyzer = None

        # Frame for file load section
        self.file_frame = tk.Frame(root)
        self.file_frame.pack(pady=10)

        self.file_button = tk.Button(self.file_frame, text="Load CSV File", command=self.load_file, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.file_button.pack(pady=5)

        # Frame for output display
        self.output_frame = tk.Frame(root)
        self.output_frame.pack(pady=10)

        self.output_text = tk.Text(self.output_frame, height=15, width=60, wrap="word", font=("Arial", 10))
        self.output_text.pack(side=tk.LEFT, fill=tk.Y)

        # Add a scrollbar to the output text box
        self.scrollbar = tk.Scrollbar(self.output_frame, command=self.output_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=self.scrollbar.set)

        # Frame for action buttons
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(pady=10)

        # Buttons for each functionality
        self.movie_count_button = tk.Button(self.buttons_frame, text="Get Movie Count", command=self.show_movie_count, bg="#2196F3", fg="white", font=("Arial", 12))
        self.movie_count_button.grid(row=0, column=0, padx=5, pady=5)

        self.genre_counts_button = tk.Button(self.buttons_frame, text="Get Genre Counts", command=self.show_genre_counts, bg="#FF5722", fg="white", font=("Arial", 12))
        self.genre_counts_button.grid(row=0, column=1, padx=5, pady=5)

        self.avg_rating_button = tk.Button(self.buttons_frame, text="Get Average Rating", command=self.show_average_rating, bg="#9C27B0", fg="white", font=("Arial", 12))
        self.avg_rating_button.grid(row=1, column=0, padx=5, pady=5)

        self.top_movies_button = tk.Button(self.buttons_frame, text="Get Top N Movies", command=self.show_top_movies, bg="#8BC34A", fg="white", font=("Arial", 12))
        self.top_movies_button.grid(row=1, column=1, padx=5, pady=5)

        self.genre_input_label = tk.Label(self.buttons_frame, text="Enter Genre:", font=("Arial", 12))
        self.genre_input_label.grid(row=2, column=0, padx=5, pady=5)

        self.genre_input = tk.Entry(self.buttons_frame, font=("Arial", 12))
        self.genre_input.grid(row=2, column=1, padx=5, pady=5)

        self.genre_movies_button = tk.Button(self.buttons_frame, text="Get Movies by Genre", command=self.show_movies_by_genre, bg="#FF9800", fg="white", font=("Arial", 12))
        self.genre_movies_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Status bar at the bottom
        self.status_bar = tk.Label(root, text="Welcome to Movie Analyzer", bd=1, relief="sunken", anchor="w", font=("Arial", 10))
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, ipady=5)

    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.file_path:
            self.analyzer = MovieAnalyzer(self.file_path)
            self.output_text.insert(tk.END, f"File Loaded: {self.file_path}\n\n")
            self.status_bar.config(text=f"File loaded successfully: {self.file_path}")

    def show_movie_count(self):
        if self.analyzer:
            count = self.analyzer.get_movie_count()
            self.output_text.insert(tk.END, f"Total Number of Movies: {count}\n")
            self.status_bar.config(text=f"Total number of movies: {count}")
        else:
            messagebox.showerror("Error", "No file loaded!")

    def show_genre_counts(self):
        if self.analyzer:
            genre_counts = self.analyzer.get_genre_counts()
            self.output_text.insert(tk.END, f"Genre Counts:\n{genre_counts}\n")
            self.status_bar.config(text="Genre counts displayed")
        else:
            messagebox.showerror("Error", "No file loaded!")

    def show_average_rating(self):
        if self.analyzer:
            avg_ratings = self.analyzer.get_average_rating_by_genre()
            self.output_text.insert(tk.END, f"Average Ratings by Genre:\n{avg_ratings}\n")
            self.status_bar.config(text="Average ratings displayed")
        else:
            messagebox.showerror("Error", "No file loaded!")

    def show_top_movies(self):
        if self.analyzer:
            top_movies = self.analyzer.get_top_n_movies()
            self.output_text.insert(tk.END, f"Top 5 Movies by Rating:\n{top_movies[['Title', 'Genre', 'Rating']]}\n")
            self.status_bar.config(text="Top movies displayed")
        else:
            messagebox.showerror("Error", "No file loaded!")

    def show_movies_by_genre(self):
        if self.analyzer:
            genre = self.genre_input.get().strip()
            if genre:
                genre_movies = self.analyzer.get_movies_by_genre(genre)
                if not genre_movies.empty:
                    self.output_text.insert(tk.END, f"Movies in '{genre}' Genre:\n{genre_movies[['Title', 'Rating']]}\n")
                    self.status_bar.config(text=f"Movies in '{genre}' genre displayed")
                else:
                    self.output_text.insert(tk.END, f"No movies found in the genre '{genre}'.\n")
                    self.status_bar.config(text=f"No movies found in '{genre}' genre")
            else:
                messagebox.showerror("Error", "Please enter a genre!")
        else:
            messagebox.showerror("Error", "No file loaded!")

if __name__ == "__main__":
    root = tk.Tk()
    ui = MovieAnalyzerUI(root)
    root.mainloop()

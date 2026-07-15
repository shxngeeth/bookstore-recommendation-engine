import tkinter as tk
from tkinter import ttk, scrolledtext
import json


# --- 1. Object-Oriented Models ---
class Book:
    """Represents a book with a unique ID and a title."""
    def __init__(self, book_id, title):
        self.book_id = book_id
        self.title = title


class User:
    def __init__(self, name):
        self.name = name
        # Using a SET for O(1) average time complexity for lookups and fast intersection/union
        self.purchased_books = set() 

    def add_purchase(self, book):
        self.purchased_books.add(book.book_id)


# --- 2. Recommendation Algorithm (Jaccard Similarity) ---
class RecommendationEngine:
    """Calculates similarity between users and generates recommendations."""
    def __init__(self, users, books):
        self.users = users
        self.books = books

    def similarity(self, user_a, user_b):
        """Calculates Jaccard Similarity (Intersection / Union)."""
        a = user_a.purchased_books
        b = user_b.purchased_books

        # Jaccard = |A intersect B| / |A union B|
        # This is the core algorithm logic (O(M), where M is number of books)
        return len(a & b) / len(a | b)

    def find_best_neighbor(self, target_user):
        """Finds the single most similar user based on Jaccard score (O(N*M))."""
        best_user = None
        best_score = -1

        # O(N) loop over all other users (N = number of users)
        for user in self.users.values():
            if user.name == target_user.name:
                continue

            score = self.similarity(target_user, user)
            if score > best_score:
                best_score = score
                best_user = user

        return best_user, best_score

    def recommend(self, target_user):
        """Generates recommendations based on the best neighbor's unique purchases."""
        neighbor, score = self.find_best_neighbor(target_user)

        if neighbor is None:
            return None, set()

        # Recommendation = Neighbor's books MINUS Target User's books (Set Difference)
        recommended = neighbor.purchased_books - target_user.purchased_books
        return (neighbor.name, score), recommended


# --- 3. Tkinter GUI Application ---
class RecommendationApp:
    def __init__(self, root, engine):
        self.root = root
        self.engine = engine

        root.title("Bookstore Recommendation Engine")
        root.geometry("700x500")

        main = ttk.Frame(root, padding=10)
        main.pack(fill="both", expand=True)

        # User selection
        tk.Label(main, text="Select User:", font=("Arial", 12)).pack(anchor="w")
        self.user_var = tk.StringVar()
        self.user_box = ttk.Combobox(
            main, textvariable=self.user_var,
            values=list(engine.users.keys()), state="readonly"
        )
        self.user_box.pack(pady=5)
        self.user_box.current(0)

        ttk.Button(main, text="Generate Recommendations",
                   command=self.show_recommendations).pack(pady=10)

        # Output areas
        ttk.Label(main, text="Purchase History:", font=("Arial", 10, 'bold')).pack(anchor="w", pady=(5,0))
        self.info_area = scrolledtext.ScrolledText(main, height=6)
        self.info_area.pack(fill="both", expand=True, pady=5)
        
        ttk.Label(main, text="Recommendations:", font=("Arial", 10, 'bold')).pack(anchor="w", pady=(5,0))
        self.reco_area = scrolledtext.ScrolledText(main, height=8)
        self.reco_area.pack(fill="both", expand=True, pady=5)

    def show_recommendations(self):
        username = self.user_var.get()
        user = self.engine.users[username]

        # Clear areas
        self.info_area.delete("1.0", tk.END)
        self.reco_area.delete("1.0", tk.END)

        # Show purchase history
        self.info_area.insert(tk.END, f"User: {username}\n\n")
        self.info_area.insert(tk.END, "Purchased Books:\n")
        
        # Format the purchased books output
        if user.purchased_books:
            for book_id in sorted(list(user.purchased_books)):
                self.info_area.insert(tk.END, f"• {self.engine.books[book_id].title}\n")
        else:
             self.info_area.insert(tk.END, "(No purchases recorded)\n")


        # Generate recommendation
        neighbor_info, recommended_ids = self.engine.recommend(user)

        if neighbor_info:
            neighbor_name, score = neighbor_info
            
            self.reco_area.insert(
                tk.END,
                f"📈 Most Similar User: {neighbor_name}\n"
            )
            self.reco_area.insert(
                tk.END,
                f"   Similarity Score (Jaccard): {score:.4f}\n\n"
            )

            if recommended_ids:
                self.reco_area.insert(tk.END, "Recommended Books (Neighbor's Unique Purchases):\n")
                # Sort for clean display
                for book_id in sorted(list(recommended_ids)): 
                    title = self.engine.books[book_id].title
                    self.reco_area.insert(tk.END, f"• {title}\n")
            else:
                self.reco_area.insert(tk.END, "No new books to recommend (Target user already owns all of neighbor's books).\n")
        else:
            self.reco_area.insert(tk.END, "No similar users found in the database.\n")


# --- DATA SETUP (Includes 5 New Records) ---

# 8 Book Records
books = {
    "B101": Book("B101", "The Algorithm Myth"),
    "B102": Book("B102", "Data Structure Guide"),
    "B103": Book("B103", "A Tale of Two Queues"),
    "B104": Book("B104", "The Greedy Programmer"),
    "B105": Book("B105", "OOP for Dummies"),
    "B106": Book("B106", "The Recursive Dream"),
    "B107": Book("B107", "Advanced Graph Theory"),       # NEW
    "B108": Book("B108", "Python Design Patterns"),      # NEW
}

# 6 User Records
users = {
    "Alice": User("Alice"),
    "Bob": User("Bob"),
    "Charlie": User("Charlie"),
    "David": User("David"),                             # NEW
    "Eve": User("Eve"),                                 # NEW
    "Fiona": User("Fiona"),                             # NEW
}

# Purchases
# Alice: B101, B102, B103
users["Alice"].add_purchase(books["B101"])
users["Alice"].add_purchase(books["B102"])
users["Alice"].add_purchase(books["B103"])

# Bob: B101, B102, B105
users["Bob"].add_purchase(books["B101"])
users["Bob"].add_purchase(books["B102"])
users["Bob"].add_purchase(books["B105"])

# Charlie: B101, B104
users["Charlie"].add_purchase(books["B101"])
users["Charlie"].add_purchase(books["B104"])

# David (NEW): B101, B102, B105, B108 - Highly similar to Bob
users["David"].add_purchase(books["B101"])
users["David"].add_purchase(books["B102"])
users["David"].add_purchase(books["B105"])
users["David"].add_purchase(books["B108"]) 

# Eve (NEW): B103, B106, B107 - Forms a new cluster
users["Eve"].add_purchase(books["B103"])
users["Eve"].add_purchase(books["B106"])
users["Eve"].add_purchase(books["B107"]) 

# Fiona (NEW): B101, B102, B103, B104, B106 - Generalist/Super User
users["Fiona"].add_purchase(books["B101"])
users["Fiona"].add_purchase(books["B102"])
users["Fiona"].add_purchase(books["B103"])
users["Fiona"].add_purchase(books["B104"])
users["Fiona"].add_purchase(books["B106"]) 


# --- EXECUTION ---
if __name__ == "__main__":
    engine = RecommendationEngine(users, books)
    root = tk.Tk()
    app = RecommendationApp(root, engine)
    root.mainloop()
    # --- Save data to JSON ---
def save_to_json(books, users, filename="prob5.json"):
    data = {
        "books": {book_id: {"book_id": book.book_id, "title": book.title} for book_id, book in books.items()},
        "users": {user_name: {"name": user.name, "purchased_books": list(user.purchased_books)} for user_name, user in users.items()}
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"JSON file '{filename}' has been created successfully!")

# Call the function
save_to_json(books, users)

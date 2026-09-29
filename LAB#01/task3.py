# Task 3: Personalized Book Recommendation Analyzer (Beginner Version)
# AI-2002 Lab

import numpy as np

# ---------- Data ----------
# Each row: [Rating, Views, Popularity]
books = np.array([
    [4.5, 120, 80],
    [4.2, 200, 65],
    [4.8, 150, 95],
    [3.9, 300, 55],
    [4.6, 180, 88]
])

print("=== Book Data Loaded ===")
print("Books array:")
print(books)
print("\n")

# ---------- 1. Display shape, size, and data type ----------
print("--- Array Information ---")
print("Shape (rows, columns):", books.shape)
print("Size (total elements):", books.size)
print("Data type:", books.dtype)
print("\n")

# ---------- 2. Calculate mean of each column ----------
print("--- Mean Values ---")
col_means = np.mean(books, axis=0)  # axis=0 means column-wise
print("Average Rating:", col_means[0])
print("Average Views:", col_means[1])
print("Average Popularity:", col_means[2])
print("\n")

# ---------- 3. Normalize each column between 0 and 1 (Min-Max) ----------
print("--- Normalization ---")
print("Formula: (x - min) / (max - min)")

# Find min and max for each column
col_mins = np.min(books, axis=0)
col_maxs = np.max(books, axis=0)

print("\nColumn minimums:", col_mins)
print("Column maximums:", col_maxs)

# Normalize all columns at once
normalized_books = (books - col_mins) / (col_maxs - col_mins)

print("\nNormalized data (all values between 0 and 1):")
print(normalized_books)

# Show what each book's normalized values are
print("\n--- Normalized Values for Each Book ---")
for i in range(len(books)):
    print("Book", i+1, "→ Rating:", round(normalized_books[i][0], 3), 
          "Views:", round(normalized_books[i][1], 3), 
          "Popularity:", round(normalized_books[i][2], 3))
print("\n")

# ---------- 4. Calculate Recommendation Score ----------
# Score = 0.5 × Rating + 0.2 × Views + 0.3 × Popularity
print("--- Recommendation Scores ---")
print("Formula: 0.5 × Rating + 0.2 × Views + 0.3 × Popularity")
print("(Using normalized values)")

# Calculate score for each book
recommendation_scores = []
for i in range(len(normalized_books)):
    score = (0.5 * normalized_books[i][0]) + \
            (0.2 * normalized_books[i][1]) + \
            (0.3 * normalized_books[i][2])
    recommendation_scores.append(score)

print("\nRecommendation scores for each book:")
for i in range(len(recommendation_scores)):
    print("Book", i+1, "→ Score:", round(recommendation_scores[i], 4))

print("\n")

# ---------- 5. & 6. Rank books using argsort ----------
# argsort gives indices sorted from lowest to highest
# We want highest first, so we reverse the order
sorted_indices = np.argsort(recommendation_scores)[::-1]

print("--- Ranking (Highest to Lowest) ---")
print("Position | Book | Score")
print("-" * 30)
for position, idx in enumerate(sorted_indices, start=1):
    print(position, "      | Book", idx+1, "|", round(recommendation_scores[idx], 4))

print("\n")

# ---------- 7. Identify the book with the highest recommendation score ----------
best_book_index = sorted_indices[0]  # first index is the best
best_score = recommendation_scores[best_book_index]

print("--- Best Book Recommendation ---")
print("Book", best_book_index+1, "has the highest score:", round(best_score, 4))
print("Original data for this book:")
print("  Rating:", books[best_book_index][0])
print("  Views:", books[best_book_index][1])
print("  Popularity:", books[best_book_index][2])
print("\n")

# ---------- 8. Use slicing to display rating and popularity separately ----------
print("--- Slicing Data ---")

# Extract all ratings (column 0)
ratings = books[:, 0]
print("All Ratings:", ratings)

# Extract all popularity scores (column 2)
popularity = books[:, 2]
print("All Popularity Scores:", popularity)

# Extract first 3 books (rows 0,1,2) and all columns
first_three_books = books[0:3, :]
print("\nFirst 3 books (all features):")
print(first_three_books)

# Extract only columns 0 and 2 (Rating and Popularity) for all books
rating_popularity = books[:, [0, 2]]
print("\nRating and Popularity (all books):")
print(rating_popularity)

print("\n")

# ---------- Summary ----------
print("="*50)
print("          RECOMMENDATION SUMMARY")
print("="*50)
print("Total books analyzed:", books.shape[0])
print("Best book:", "Book", best_book_index+1)
print("Best book score:", round(best_score, 4))
print("\n--- Complete Ranking ---")
for position, idx in enumerate(sorted_indices, start=1):
    print(position, ". Book", idx+1, "- Score:", round(recommendation_scores[idx], 4))
print("="*50)
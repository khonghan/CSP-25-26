#If you do not have pandas or matplotlib installed you will need to 
#import pandas in Terminal.  Open VS Code, open Terminal and type: 
#py -m pip install pandas matplotlib


import pandas as pd
import matplotlib.pyplot as plt

# Input your dataset
data = {
   
# 5 movies
# "The Hunger Games", "Despicable Me", "Spiderman: Into the Spiderverse"
# "Fantastic Four", "10 Things I Hate About You"

 "Movie": [
        "Despicable Me", "The Hunger Games", "10 Things I Hate About You", "The Hunger Games",
        "Despicable Me", "10 Things I Hate About You", "Despicable Me", "Despicable Me",
        "Spiderman: Into the Spiderverse", "Spiderman: Into the Spiderverse", "The Hunger Games", "Spiderman: Into the Spiderverse",
        "The Hunger Games", "Spiderman: Into the Spiderverse", "Despicable Me", "The Hunger Games",
        "Spiderman: Into the Spiderverse", "The Fantastic Four", "Spiderman: Into the Spiderverse", "The Hunger Games",
        "Despicable Me", "Despicable Me", "Spiderman: Into the Spiderverse", "Despicable Me", 
        "Spiderman: Into the Spiderverse"
        ],
    
# Action, Drama, Comedy, Adventure, Suspense, Horror
"Genre": [
        "Drama", "Drama", "Comedy", "Adventure",
        "Suspense", "Drama", "Comedy", "Suspense", 
        "Comedy", "Action", "Comedy", "Action", 
        "Comedy", "Action", "Action", "Adventure", 
        "Suspense", "Action", "Action", "Comedy", 
        "Comedy", "Comedy", "Action", "Comedy", 
        "Action"
        ],
    
"Grade": [
        10, 10, 10, 10,
        10, 10, 10, 10,
        10, 10, 10, 10,
        10, 10, 10, 10,
        12, 10, 10, 10,
        10, 11, 11, 12,
        10 
        ],
    
"MoviesPerWeek": [
        0, 2, 1, 1,
        2, 1, 1, 1,
        1, 1, 1, 0,
        4, 1, 0, 0,
        3, 0, 1, 1,
        2, 0, 1, 0,
        2
        ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Display first few rows
print("Movie Preference Dataset (25 Students):")
print(df)


# Bar Graph of Genres
# ---------------------------
genre_counts = df["Genre"].value_counts()

plt.figure()
genre_counts.plot(kind="bar", color="skyblue")
plt.title("Favorite Movie Genres (25 Students)")
plt.xlabel("Genre")
plt.ylabel("Number of Students")
plt.tight_layout()
plt.show()

# Scatter Plot - Movies Watched vs Grade
# ---------------------------
plt.figure()
plt.scatter(df["Grade"], df["MoviesPerWeek"], color="green")
plt.xlabel("Grade Level")
plt.ylabel("Movies Watched Per Week")
plt.title("Movies Watched vs Grade Level")
plt.grid(True)
plt.tight_layout()
plt.show()

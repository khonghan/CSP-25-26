#If you do not have pandas or matplotlib installed you will need to 
#import pandas in Terminal.  Open VS Code, open Terminal and type: 
#py -m pip install pandas matplotlib


import pandas as pd
import matplotlib.pyplot as plt

# Input your dataset
data = {
   
# Taylor Swift, Malcom Todd, Clairo, Michael Jackson, Drake

 "Artist": [
        "Clairo", "Drake", "Micheal Jackson", "Micheal Jackson",
        "Malcom Todd", "Malcom Todd", "Malcom Todd", "Micheal Jackson",
        "Drake", "Malcom Todd", "Micheal Jackson", "Drake",
        "Drake", "Malcom Todd", "Micheal Jackson", "Clairo",
        "Malcom Todd", "Clairo", "Clairo", "Clairo",
        "Micheal Jackson", "Malcom Todd", "Michael Jackson", "Clairo", 
        "Clairo"
        ],
    
# Hip-Hop, Pop, Rock, Country, EDM
"Genre": [
        "Pop", "Hip-Hop", "Pop", "Pop",
        "Pop", "Hip-Hop", "Pop", "Hip-Hop", 
        "Pop", "Hip-Hop", "Hip-Hop", "Hip-Hop", 
        "Pop", "Pop", "Pop", "Pop", 
        "Pop", "Pop", "EDM", "Pop", 
        "Pop", "Hip-Hop", "Pop", "Pop", 
        "Hip-Hop"
        ],
    

# 0, 1, 2, 3, 4+
"HoursPerDay": [
        1, 2, 1, 3,
        1, 4, 4, 1,
        4, 3, 1, 0,
        2, 3, 2, 4,
        3, 4, 3, 2,
        1, 3, 2, 2,
        2
        ],
    
# Morning, Afternoon, Evening, Night, Throughout the Day
"TimeOfDay": [
        "Night", "Afternoon", "Night", "Throughout the Day",
        "Evening", "Throughout the Day", "Throughout the Day", "Night",
        "Throughout the Day", "Afternoon", "Night", "Morning",
        "Night", "Throughout the Day", "Night", "Evening",
        "Night", "Evening", "Throughout the Day", "Evening",
        "Night", "Evening", "Evening", "Night",
        "Morning"
        ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Display first few rows
print("Music Preference Dataset (25 Students):")
print(df)


# Bar Graph of Favorite Artists
# ---------------------------
artist_counts = df["Artist"].value_counts()

plt.figure()
artist_counts.plot(kind="bar", color="mediumpurple")
plt.title("Favorite Artists (25 Students)")
plt.xlabel("Artist")
plt.ylabel("Number of Students")
plt.tight_layout()
plt.show()

# Bar Graph of Genres
# ---------------------------
genre_counts = df["Genre"].value_counts()

plt.figure()
genre_counts.plot(kind="bar", color="lightcoral")
plt.title("Favorite Music Genres (25 Students)")
plt.xlabel("Genre")
plt.ylabel("Number of Students")
plt.tight_layout()
plt.show()

# Bar Graph of Time of Day Listened
# ---------------------------
time_counts = df["TimeOfDay"].value_counts()

plt.figure()
time_counts.plot(kind="bar", color="skyblue")
plt.title("When Students Listen to Music (25 Students)")
plt.xlabel("Time of Day")
plt.ylabel("Number of Students")
plt.tight_layout()
plt.show()

# Scatter Plot - Hours Listened vs Genre
# ---------------------------
plt.figure()
plt.scatter(df["HoursPerDay"], df["Genre"], color="green", s=100, alpha=0.6)
plt.xlabel("Hours Listening Per Day")
plt.ylabel("Genre")
plt.title("Hours Listened Per Day by Genre")
plt.grid(True)
plt.tight_layout()
plt.show()

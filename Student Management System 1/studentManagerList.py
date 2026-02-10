# Student Management System (No Classes)
# Project 1 - Console-based program for managing students using LISTS only

import re



# ======================== #
#    STUDENT DATA SETUP    #
# ======================== #
# These lists store corresponding student data
studentIDs = []
studentNames = []
studentGrades = []



# ======================== #
#     CORE FUNCTIONS       #
# ======================== #

# Add a new student after checking for duplicate IDs
def addStudent():
    try:
        studentID = inputInt("Enter Student ID: ")
        if studentID in studentIDs:
            print(f"Student with ID {studentID} already exists.")
            return

        name = inputString("Enter Student Name: ")
        grade = inputFloat("Enter Student Grade: ")

        studentIDs.append(studentID)
        studentNames.append(name)
        studentGrades.append(grade)

        print("Student added successfully.")
    except ValueError:
        print("Invalid input. Please enter valid data.")

# Display all students currently stored
def viewAllStudents():
    if not studentIDs:
        print("No students found.")
        return
    for i in range(len(studentIDs)):
        print(f"ID: {studentIDs[i]}, Name: {studentNames[i]}, Grade: {studentGrades[i]}")


# Find and display a student by their ID
def findStudentByID():
    studentID = inputInt("Enter Student ID to find: ")
    if studentID in studentIDs:
        i = studentIDs.index(studentID)
        print(f"ID: {studentIDs[i]}, Name: {studentNames[i]}, Grade: {studentGrades[i]}")
        return i
    else:
        print("Student not found.")
        return None

# Remove a student by their ID
def removeStudentByID():
    studentID = inputInt("Enter Student ID to remove: ")
    if studentID in studentIDs:
        i = studentIDs.index(studentID)
        del studentIDs[i], studentNames[i], studentGrades[i]
        print("Student removed successfully.")
    else:
        print("Student not found.")


# Update a student's grade by their ID
def updateStudentGrade():
    studentID = inputInt("Enter Student ID to update grade: ")
    if studentID in studentIDs:
        i = studentIDs.index(studentID)
        new_grade = inputFloat("Enter new grade: ")
        studentGrades[i] = new_grade
        print("Student grade updated successfully.")
    else:
        print("Student not found.")

# Sort students by name or grade
def sortStudentsBy():
    key = input("Sort by 'name' or 'grade': ").strip().lower()
    if not studentIDs:
        print("No students to sort.")
        return

    if key == "name":
        combined = sorted(zip(studentIDs, studentNames, studentGrades), key=lambda x: x[1].lower())
    elif key == "grade":
        combined = sorted(zip(studentIDs, studentNames, studentGrades), key=lambda x: x[2], reverse=True)
    else:
        print("Invalid sort key. Use 'name' or 'grade'.")
        return

    # unzip combined back into the lists (convert tuples to lists)
    ids, names, grades = zip(*combined)
    studentIDs[:] = list(ids)
    studentNames[:] = list(names)
    studentGrades[:] = list(grades)
    print(f"\nStudents sorted by {key} successfully.\n")
    for i in range(len(studentIDs)):
        print(f"ID: {studentIDs[i]}, Name: {studentNames[i]}, Grade: {studentGrades[i]}")

# Search for student by name
def searchStudents():
    keyword = input("Enter name keyword to search: ").lower()
    found = False
    for i in range(len(studentNames)):
        if keyword in studentNames[i].lower():
            print(f"ID: {studentIDs[i]}, Name: {studentNames[i]}, Grade: {studentGrades[i]}")
            found = True
    if not found:
        print("No matching students found.")


# ======================== #
#     INPUT VALIDATION     #
# ======================== #
def inputInt(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def inputFloat(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def inputString(prompt):
    pattern = r"^[A-Za-z][A-Za-z\s-]*[A-Za-z]$"
    while True:
        name = input(prompt).strip()
        if re.match(pattern, name):
            return name
        else:
            print("Invalid input. Use only letters, spaces, or hyphens (e.g., John Doe, Mary-Anne).")



# ======================== #
#        MAIN LOOP         #
# ======================== #
def main():
    """Main console menu loop for Student Management."""
    while True:
        print("\n\\==== Student Management System ====/")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Find Student by ID")
        print("4. Remove Student by ID")
        print("5. Update Student Grade")
        print("6. Sort Students")
        print("7. Search Students")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ").strip()
        if choice == '1':
            addStudent()
        elif choice == '2':
            viewAllStudents()
        elif choice == '3':
            findStudentByID()
        elif choice == '4':
            removeStudentByID()
        elif choice == '5':
            updateStudentGrade()
        elif choice == '6':
            sortStudentsBy()
        elif choice == '7':
            searchStudents()
        elif choice == '8':
            print("Exiting Student Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")
            
if __name__ == "__main__":
    main()



# ======================== #
#        TEST CASES        #
# ======================== #
'''
\==== Student Management System ====/
1. Add Student
2. View All Students
3. Find Student by ID
4. Remove Student by ID
5. Update Student Grade
6. Sort Students
7. Search Students
8. Exit
Enter your choice (1-8): 1
Enter Student ID: 1
Enter Student Name: bob
Enter Student Grade: 54
Student added successfully.

Enter your choice (1-8): 1
Enter Student ID: 2
Enter Student Name: jim
Enter Student Grade: 90
Student added successfully.

Enter your choice (1-8): 1
Enter Student ID: 3
Enter Student Name: mary
Enter Student Grade: 98
Student added successfully.

Enter your choice (1-8): 2
ID: 1, Name: bob, Grade: 54.0
ID: 2, Name: jim, Grade: 90.0
ID: 3, Name: mary, Grade: 98.0

Enter your choice (1-8): 6
Sort by 'name' or 'grade': grade
Students sorted by grade successfully.
ID: 3, Name: mary, Grade: 98.0
ID: 2, Name: jim, Grade: 90.0
ID: 1, Name: bob, Grade: 54.0

Enter your choice (1-8): 7
Enter name keyword to search: bob
ID: 1, Name: bob, Grade: 54.0

Enter your choice (1-8): 4
Enter Student ID to remove: 1
Student removed successfully.

Enter your choice (1-8): 3
Enter Student ID to find: 1
Student not found.

Enter your choice (1-8): 5
Enter Student ID to update grade: 2
Enter new grade: 78
Student grade updated successfully.

Enter your choice (1-8): 2
ID: 2, Name: jim, Grade: 78.0
ID: 3, Name: mary, Grade: 98.0

\==== Student Management System ====/
1. Add Student
2. View All Students
3. Find Student by ID
4. Remove Student by ID
5. Update Student Grade
6. Sort Students
7. Search Students
8. Exit
Enter your choice (1-8): 8
Exiting Student Management System. Goodbye!
'''
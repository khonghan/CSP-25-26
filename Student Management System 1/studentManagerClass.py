# Student Management System using Class
# Project 2 - Console-based program for managing student 

import re



# ======================== #
#      STUDENT CLASS       #
# ======================== #
class student:
    def __init__(self, studentID: int, name: str, grade: float):
        self.studentID = studentID
        self.name = name
        self.grade = grade

    # Getter and Setter methods
    def getID(self) -> int:
        return self.studentID
        
    def setID(self, studentID: int):
        self.studentID = studentID

    def getName(self) -> str:
        return self.name
        
    def setName(self, name: str):
        self.name = name

    def getGrade(self) -> float:
        return self.grade
        
    def setGrade(self, grade: float):
        self.grade = grade
        
    # Display student info
    def displayInfo(self):
        print(f"ID: {self.studentID}, Name: {self.name}, Grade: {self.grade}")



# ======================== #
#    STUDENT MANAGEMENT    #
# ======================== #
class studentManager:
    def __init__(self):
        self.students = [] # List to store student objs

    # Add a new student
    def addStudent(self, studentID: int, name: str, grade: float):
        # Check if student ID already exists
        for existingStudent in self.students:
            if existingStudent.getID() == studentID:
                print(f"Student with ID {studentID} already exists.")
                return
        # Create a new student instance and add it to the list
        newStudent = student(studentID, name, grade)
        self.students.append(newStudent)
        print(f"Student added successfully.")

    # View all students
    def viewAllStudents(self):
        if not self.students:
            print("No students found.")
            return
        for student in self.students:
            student.displayInfo()

    # Find a student by ID
    def findStudentByID(self, studentID: int):
        for student in self.students:
            if student.getID() == studentID:
                student.displayInfo()
                return student
            print("Student not found.")
            return None
        
    # Remove a student by ID
    def removeStudentByID(self, studentID: int):
        for student in self.students:
            if student.getID() == studentID:
                self.students.remove(student)
                print("Student removed successfully.")
                return
            print("Student not found.")

    # Update student grade by ID
    def updateStudentGrade(self, studentID: int, newGrade: float):
        for student in self.students:
            if student.getID() == studentID:
                student.setGrade(newGrade)
                print("Student grade updated successfully.")
                return
            print("Student not found.")
    
    # Sort students by key
    def sortStudentsBy(self, key: str):
        if not self.students:
            print("No students to sort.")
            return
        if key == "name":
            self.students.sort(key=lambda x: x.getName().lower())
        elif key == "grade":
            self.students.sort(key=lambda x: x.getGrade(), reverse = True)
        else:
            print("Invalid sort key. Use 'name' or 'grade'.")
            return
        
        print(f"\nStudents sorted by {key} successfully.\n")
        for student in self.students:
            student.displayInfo()

    # Search student by name
    def searchStudents(self, keyword):
        results = [s for s in self.students if keyword.lower() in s.getName().lower()]
        if results:
            for s in results:
                s.displayInfo()
        else:
            print("No matching students found.")



# ======================== #
#     INPUT VALIDATION     #
# ======================== #
# Safely get the integer input from user
def inputInt(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            continue
        
# Safely get the float input from user
def inputFloat(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

# Safely get the string input from user
def inputString(prompt):
    pattern = r"^[A-Za-z][A-Za-z/s-]*[A-Za-z]$" # Allows letters, spaces, and hyphens, but not starting/ending with them
    while True:
        name = input(prompt).strip()
        if re.match(pattern, name):
            return name
        else:
            print("Invalid input. Use only letters, spaces, hyphens (e.g., John Doe or Mary-Anne).")
            continue



# ======================== #
#        MAIN LOOP         #
# ======================== #
def main():
    manager = studentManager()
    while True:
        print("\n\==== Student Management System ====/")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Find Student by ID")
        print("4. Remove Student by ID")
        print("5. Update Student Grade")
        print("6. Sort Students")
        print("7. Search Students")
        print("8. Exit")
        
        choice = inputInt("Enter your choice (1-8): ").strip()
        
        if choice == '1':
            studentID = inputInt("Enter Student ID: ")
            name = inputString("Enter Student Name: ")
            grade = inputFloat("Enter Student Grade: ")
            manager.addStudent(studentID, name, grade)
        
        elif choice == '2':
            manager.viewAllStudents()
        
        elif choice == '3':
            studentID = inputInt("Enter Student ID to find: ")
            manager.findStudentByID(studentID)
        
        elif choice == '4':
            studentID = inputInt("Enter Student ID to remove: ")
            manager.removeStudentByID(studentID)
        
        elif choice == '5':
            studentID = inputInt("Enter Student ID to update grade: ")
            newGrade = inputFloat("Enter new grade: ")
            manager.updateStudentGrade(studentID, newGrade)
        
        elif choice == '6':
            key = input("Sort by 'name' or 'grade': ").strip().lower()
            manager.sortStudentsBy(key)
        
        elif choice == '7':
            keyword = input("Enter name to search: ")
            manager.searchStudents(keyword)
        
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
Enter Student ID: 2
Enter Student Name: jim
Enter Student Grade: 90
Student added successfully.

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
Enter Student ID: 3
Enter Student Name: mary
Enter Student Grade: 98
Student added successfully.

\==== Student Management System ====/
1. Add Student
2. View All Students
3. Find Student by ID
4. Remove Student by ID
5. Update Student Grade
6. Sort Students
7. Search Students
8. Exit
Enter your choice (1-8): 2
ID: 1, Name: bob, Grade: 54.0
ID: 2, Name: jim, Grade: 90.0
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
Enter your choice (1-8): 6
Sort by 'name' or 'grade': name

Students sorted by name successfully.

ID: 1, Name: bob, Grade: 54.0
ID: 2, Name: jim, Grade: 90.0
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
Enter your choice (1-8): 6
Sort by 'name' or 'grade': grade

Students sorted by grade successfully.

ID: 3, Name: mary, Grade: 98.0
ID: 2, Name: jim, Grade: 90.0
ID: 1, Name: bob, Grade: 54.0

\==== Student Management System ====/
1. Add Student
2. View All Students
3. Find Student by ID
4. Remove Student by ID
5. Update Student Grade
6. Sort Students
7. Search Students
8. Exit
Enter your choice (1-8): 7
Enter name keyword to search: bob
ID: 1, Name: bob, Grade: 54.0

\==== Student Management System ====/
1. Add Student
2. View All Students
3. Find Student by ID
4. Remove Student by ID
5. Update Student Grade
6. Sort Students
7. Search Students
8. Exit
Enter your choice (1-8): 4
Enter Student ID to remove: 1
Student removed successfully.

\==== Student Management System ====/
1. Add Student
2. View All Students
3. Find Student by ID
4. Remove Student by ID
5. Update Student Grade
6. Sort Students
7. Search Students
8. Exit
Enter your choice (1-8): 3
Enter Student ID to find: 1
Student not found.

\==== Student Management System ====/
1. Add Student
2. View All Students
3. Find Student by ID
4. Remove Student by ID
5. Update Student Grade
6. Sort Students
7. Search Students
8. Exit
Enter your choice (1-8): 5
Enter Student ID to update grade: 2
Enter new grade: 78
Student grade updated successfully.

\==== Student Management System ====/
1. Add Student
2. View All Students
3. Find Student by ID
4. Remove Student by ID
5. Update Student Grade
6. Sort Students
7. Search Students
8. Exit
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
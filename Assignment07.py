# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   MClark,8/11/2024,Created Person class
#   MClark,8/12/2024,Added functions
#   MClark,8/16/2024,Fixed reading and writing to file
#   MClark,8/12/2024,Fixed another read file issue, added format changes
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Data --------------------------------------- #
class Person:
    """
    A class representing person data.

    Properties:
    - first_name (str): The student's first name.
    - last_name (str): The student's last name.

    ChangeLog:
    - MClark, 8/11/2024: Created the class.
    - MClark, 8/12/2024: Added functions
    """

    def __init__(self, first_name: str = '', last_name: str = ''):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self):
        """
        Returns first name with first letter capitalized
        :return:first_name
        """
        return self.__first_name.title()

    @first_name.setter
    def first_name(self, value: str):
        """
        Sets and validates first name
        :param value:first_name set to value
        """
        if value.isalpha() or len(value) < 2:
            self.__first_name = value
        else:
            raise ValueError("First name should only contain letters and be at least 2 characters.")

    @property
    def last_name(self):
        """
        first name with last letter capitalized
        :return:last_name
        """
        return self.__last_name.title()

    @last_name.setter
    def last_name(self, value: str):
        """
        Sets and validates last name
        :param value:last_name set to value
        """
        if value.isalpha() or len(value) < 2:
            self.__last_name = value
        else:
            raise ValueError("Last name should only contain letters and be at least 2 characters.")

    def __str__(self):
        """
        Formatted string
        :return:
        :rtype:
        """
        return f"{self.first_name},{self.last_name}"


class Student(Person):
    """
    A class representing student data.

    Properties:
    - first_name (str): The student's first name.
    - last_name (str): The student's last name.
    - course_name (str): The student's course name.

    ChangeLog:
    - MClark, 8/12/2024: Created the class, added functions
    """

    def __init__(self, first_name: str = "", last_name: str = "", course_name: str = ""):
        super().__init__(first_name, last_name)
        self.course_name = course_name

    @property
    def course_name(self):
        """
        Returns course name
        :return:course_name
        """
        return self.__course_name.title()

    @course_name.setter
    def course_name(self, value: str):
        """
        Sets and validates course name
        :param value:course_name set to value
        """
        if len(value) > 2:
            self.__course_name = value
        else:
            raise ValueError("Course name must be at least 3 characters.")

    def __str__(self):
        """
        Formatted string
        :return:
        :rtype:
        """
        return f"{super().__str__()}, {self.course_name}"


# Processing --------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with Json files

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list[Student]):
        """ This function reads data from a json file and loads it into a list of dictionary rows

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :param file_name: string data with name of file to read from
        :param student_data: list of dictionary rows to be filled with file data

        :return: list
        """
        file_dict = []
        file = None
        try:
            file = open(file_name, "r")
            file_dict = json.load(file)
            file.close()
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with reading the file.", error=e)
        finally:
            if file is not None and not file.closed:
                file.close()
        for row in file_dict:
            student_data.append(Student(row["FirstName"],
                                        row["LastName"],
                                        row["CourseName"])
                                )
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list[Student]):
        """ This function writes data to a json file with data from a list of dictionary rows

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :param file_name: string data with name of file to write to
        :param student_data: list of dictionary rows to be writen to the file

        :return: None
        """
        file_dict = []
        for student in student_data:
            file_dict.append({"FirstName": student.first_name,
                              "LastName": student.last_name,
                              "CourseName": student.course_name}
                             )
        file = None
        try:

            file = open(file_name, "w")
            json.dump(file_dict, file, indent=1)
            file.close()
            print("The following students have been registered:\n")
            IO.output_student_and_course_names(student_data=student_data)
        except Exception as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message, error=e)
        finally:
            if file is not None and not file.closed:
                file.close()


# Presentation --------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    RRoot,1.2.2030,Added menu output and input functions
    RRoot,1.3.2030,Added a function to display the data
    RRoot,1.4.2030,Added a function to display custom error messages
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays the a custom error messages to the user

        ChangeLog: (Who, When, What)
        RRoot,1.3.2030,Created function

        :param message: string with message data to display
        :param error: Exception object with technical message to display

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function


        :return: None
        """
        print()  # Adding extra space to make it look nicer.
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :return: string with the users choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ").strip()
            if choice not in ("1", "2", "3", "4"):  # Note these are strings
                raise Exception("Please choose \033[1m1\033[0m, \033[1m2\033[0m, \033[1m3\033[0m, or \033[1m4\033[0m")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing e to avoid the technical message

        return choice

    @staticmethod
    def output_student_and_course_names(student_data: list[Student]):
        """ This function displays the student and course names to the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :param student_data: list of dictionary rows to be displayed

        :return: None
        """

        print("-" * 50)
        for student in student_data:
            print(f'{student.first_name} {student.last_name} is enrolled in {student.course_name}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list[Student]):
        """ This function gets the student's first name and last name, with a course name from the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :param student_data: list of dictionary rows to be filled with input data

        :return: list
        """

        try:
            student_first_name = input("Enter the student's \033[1mfirst name\033[0m: ").strip()
            student_last_name = input("Enter the student's \033[1mlast name\033[0m: ").strip()
            course_name = input("Please enter the \033[1mcourse name\033[0m: ").strip()
            student = Student(student_first_name,
                              student_last_name,
                              course_name)
            student_data.append(student)
            print()
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(message="One of the values was the correct type of data!", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
        return student_data


# Define the Data Variables
students: list[Student] = []  # a table of student data
menu_choice: str  # Hold the choice made by the user.

# Start of main body

# When the program starts, read the file data into a list of lists (table)
# Extract the data from the file
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
while (True):

    # Present the menu of choices
    IO.output_menu(menu=MENU)

    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":  # This will not work if it is an integer!
        students = IO.input_student_data(student_data=students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_and_course_names(students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop

print("Program Ended")
# Sean Kennedy 
# Student GPA Checker App
# Version 1.0
# Last Updated: 2022-02-20
# The app will check students GPAs and tell you if the made deans list or honor roll. 

def get_student_info():
    # Get student's last name, first name, and GPA
    last_name = input("Enter student's last name (or 'ZZZ' to quit): ")
    if last_name.upper() == 'ZZZ':
        return None, None, None
    first_name = input("Enter student's first name: ")
    gpa = float(input("Enter student's GPA: "))
    return last_name, first_name, gpa

def check_deans_list(gpa):
    # Check if student's GPA qualifies for Dean's List
    return gpa >= 3.5

def check_honor_roll(gpa):
    # Check if student's GPA qualifies for Honor Roll
    return gpa >= 3.25

def main():
    while True:
        last_name, first_name, gpa = get_student_info()
        if last_name is None:
            break
        print(f"Student: {first_name} {last_name}, GPA: {gpa:.2f}")
        if check_deans_list(gpa):
            print("Congratulations! You have made the Dean's List.")
        elif check_honor_roll(gpa):
            print("Congratulations! You have made the Honor Roll.")

if __name__ == '__main__':
    main()
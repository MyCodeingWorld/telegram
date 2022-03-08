import mysql.connector as SQL
import requests
database = SQL.connect(host = 'localhost',
                       database = "hkbk_cse_student",
                       user = 'root',
                       password = '12345678')

def Query_Execute():
    USN_Query = input("Enter the USN of Student: ").upper()
    cursor = database.cursor()
    cursor.execute(f"select chat_id, name from Stud_Record where usn = \'{USN_Query}\'")
    result = cursor.fetchall()
    if len(result) >= 1:
        string = input("Enter the Message: ")
        base_url = "https://api.telegram.org/bot5027808497:AAHo8-FtHIeOCcP_hv72MdZbTHOgxZPg9D0/sendMessage"
        parameters = {
            "chat_id" : str(result[0][0]),
            "text" : f"Dear {result[0][1]},\n{string}"
        }
        requests.get(base_url, data=parameters)
        print("Message Sent")
    else:
        print("NO SUCH USN")

if __name__ == '__main__':
    value = None
    while True:
        print("="*40)
        print("\t\t👉👉MAIN MENU👈👈")
        print("1. Sent a particular message to Student")
        print("2. Update Students Attendance")
        print("3. Update Latest IA Marks")
        print("4. Update New Circular for students")
        value = int(input("Enter the Option From above: "))
        if value == 1:
            print("\t👨‍🎨Send The Message in Private👩‍🎨")
            Query_Execute();
        elif value == 2:
            print("\t👨‍🎨Update Student Attendance👩‍🎨")
        elif value == 3:
            print("\t👨‍🎨Update Latest IA Marks👩‍🎨")
        elif value == 4:
            print("\t👨‍🎨Update New Circular for students👩‍🎨")
        else:
            print("Invalid Option")
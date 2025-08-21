import pandas as pd
from datetime import datetime
import sys

#Example problem for Assessment #2
#Creating a Slowly Changing Dimenstion Type 2 in Python


# Read the csv file prepared and show the table
Employee_DB = pd.read_csv("Employee_Database.csv")

print("\n--- Current Employee Records ---")
print(Employee_DB[["Employee_ID", "Position", "Name", "Company_Location", "Start_Date", "End_Date"]].to_markdown(index=False))

#Adding an input function for an interactive approach
choice = input("\nDo you want to update an employee's data? (yes/no): ").strip().lower()

if choice == "yes":
    Current_Employees = (Employee_DB[Employee_DB["Is_Current"] == 1]).reset_index() #Taking only the current employees and disregard the rest
    print("\nCurrent Employees:")
    for i, row in Current_Employees.iterrows(): # Creating a loop for names output
        print(f"{i+1}. {row['Name']}")

else :
    print("\nThank you for your time. Byee")
    sys.exit()

# Loop for the input question of the specific employee needed to be changed.
loop_employee=0
while loop_employee == 0:
    employee_choice = int(input("\nSelect an employee to update (number): ")) - 1
    if 0 <= employee_choice < len(Current_Employees):
        loop_employee = 1
    else:
        print("\nThere is no data listed on the number you've chosen. Please choose another.")

#Locate the chosen employee from the dataFrame and save its Key. 
Employee_info = Current_Employees.iloc[employee_choice]
Employee_Key = Employee_info["Employee_Key"]

#Display the information of the employee and the list of changeable values in the dataFrame.
print("\nCurrent Employee Information:")
print(f"1. Name: {Employee_info['Name']}")
print(f"2. Position: {Employee_info['Position']}")
print(f"3. Company Location: {Employee_info['Company_Location']}")

#Loop for the input question of the specific field to be changed.
loop_field = 0
while loop_field == 0:
    field_choice = int(input("\nSelect the field to update (number): "))
    if 1 <= field_choice <= 3:
        loop_field = 1 
    else:
        print("\nThere is no data listed on the number you've chosen. Please choose another.")

#Save the output of the field      
field = "Name" if field_choice == 1 else ("Position" if field_choice == 2 else "Company_Location")

#Input the new data
new_value = input("Enter the new data: ").strip()

#Adding enddate for the previous record
Employee_DB["End_Date"] = pd.to_datetime(Employee_DB["End_Date"], errors="coerce")
Employee_DB.loc[Employee_DB["Employee_Key"] == Employee_Key, "End_Date"] = datetime.now().strftime("%m/%d/%Y")
Employee_DB.loc[Employee_DB["Employee_Key"] == Employee_Key, "Is_Current"] = 0

#Add the new record
new_data = Employee_info.copy() #copy the previous details 
new_data["Employee_Key"] = Employee_DB["Employee_Key"].max() + 1
new_data[field] = new_value
new_data["Start_Date"] = datetime.now().strftime("%m/%d/%Y") # used for format only
new_data["End_Date"] = None
new_data["Is_Current"] = 1 # 1 is equal to active employee data then 0 means historical data

#Convert the new data into DataFrame and change the format of the datetime to remove future error.
updated_data = pd.DataFrame([new_data], columns = Employee_DB.columns)
updated_data["End_Date"] = pd.to_datetime(updated_data["End_Date"], errors="coerce")

#Concatenate the new value into the Database
Employee_DB = pd.concat([Employee_DB,updated_data])

# Save the changes to the same csv to update the file context.
Employee_DB.to_csv("Employee_Database.csv", index=False)

#Display the table inside the csv file.
print("\nRecord updated successfully!")
print("\n--- Current Employee Records ---")
print(Employee_DB[["Employee_ID", "Position", "Name", "Company_Location", "Start_Date", "End_Date"]].to_markdown(index=False))


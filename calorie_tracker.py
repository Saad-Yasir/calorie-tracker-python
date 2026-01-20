# -*- coding: utf-8 -*-
"""
Created by:
  - Saad Bin Yasir 

Problem Description:

I always find it difficult tracking my daily calories, and
overall progress toward gaining weight. Most apps are locked behind a paywall
or have too few features, so I wanted to create a simple program that solves 
this problem in a straightforward way.

This program allows a user to sign up with their personal information such as 
username, weight, height, age, sex, and their goal (gain, lose or maintain). 
It then calculates their BMI, BMR, TDEE, and the user’s approximate daily 
calorie need based on their activity level.

After signing up, the user can record daily calorie intake and whether they
went to the gym. The program stores these records in a text file and later
analyzes the last seven days to estimate whether the user is gaining,
maintaining, or losing weight. It also calculates the overall change since
sign-up. 

The purpose of this project is to help myself and other users to easily monitor 
calorie intake and progress without needing any external tools or apps. It
handles the problem in a simple, beginner and user-friendly way.


This project includes:

1. calorie_tracker.py ---> the main program containing the full solution and problem description.
2. database.txt ---> contains one example user, "john" that can be used to log in.
3. john.txt ---> sample calorie and gym records for the user "john".

"""


import sys  # Needed for "sys.exit()" which was used below

# Functions:

def bmi(weight, height):
    if weight <= 0 or height <= 0:
        return 0
    return round(weight / ((height/100)**2), 1) # Returns BMI rounded to 1 d.p.

def recommend(bmi):
    if bmi < 18.5:
        return "gain"
    elif 18.5 <= bmi < 25:
        return "maintain"
    else:
        return "lose" 

def bmr(weight, height, age, sex):
    if weight <= 0 or height <= 0 or age <= 0:
        return 0  # Returns 0 if invalid weight/height/age  
    
    base = (10 * weight) + (6.25 * height) - (5 * age)
    if sex == "male":
        return base + 5
    elif sex == "female":
        return base - 161
    # If gender is not specified:
    else:
        return base
    
def tdee(bmr, activity_factor):
    return bmr * activity_factor
    # Activity factor will be determined based on whether user went to the gym

def af_from_days(days):
    if 1 <= days <= 2:
        return 1.375
    elif 3 <= days <= 5:
        return 1.55
    elif days > 5:
        return 1.725
    else:
        return 1.2  # Returns activity factor 1.2 if user does not go to the gym
    
def record_days(filename, mode):
    while True:
        try:
            days = int(input("How many days did you record calories?\n> ")) 
            if days <= 0:
                print("Please enter at least one day.")
                continue # Skips invalid data entry
            
            lines = []
            for i in range(days):
                print(f"Day {i+1}:")
                while True:  # Loop will keep running unless user types yes/no
                    gym = input("Did you go to the gym? (yes/no)\n> ").strip().lower()
                    if gym not in ("yes", "no"):
                        print("Please try again (yes/no).")
                    else:
                        break
                while True:
                    try:
                        calories = int(input("How many calories did you eat?\n> ").strip())
                        break
                    except ValueError:
                        print("Please enter calories in digits only!")
                lines.append(f"{gym}, {calories}\n")
            with open(filename, mode) as fileHandle:
                fileHandle.writelines(lines)
            return lines
        except ValueError:
            print("Please enter days in whole digits only!")



# Main Code:    

all_names = []
database = []    
try:
    with open("database.txt", "r") as fileHandle: # Reads pre-existing file names "database.txt"
        for line in fileHandle:
            line = line.strip() # Removes indentation, new lines, etc 
            if not line:
                continue   # This will skip empty lines
            all_names.append(line.split(",")[0].lower())
            database.append(line.split(",")) # This splits the line into a list seperated by commas
except FileNotFoundError:
    pass  # Ensures that if database.txt does not exist, code won't break. File will be created later with append.
    


# Loop for Main Menu
while True:    
    print()
    entered = input("Enter '0' to sign up, '1' to log in, or any key to close this program:\n> ").strip()
    # Strip will ignore accidental indentations

    #0 Sign Up:
    if entered == "0":
        while True:
            
            # Personal Info:
            name = (input("Enter Username:\n> ").strip().lower())[0:15] # Username should be no longer than 15 characters
            if name in all_names:
                print("Username taken, please log in or choose another username!") 
                break  # Exists sign up if user already has account
            while True:
                try:
                    weight = float(input("Enter weight in kg:\n> "))
                    height = float(input("Enter height in cm:\n> "))
                    break
                except ValueError:
                    print("Please enter your weight and height in digits only.")
                    
            while True:
                try:
                    age = int(input("Enter age in years:\n> ").strip())
                    if age < 16:
                        print("Sign up failed. You need to be at least 16 to sign up!")
                        sys.exit()
                    # Ages less than 16 are not allowed to join the program. This will cause user to be safely booted from program without errors raised.
                    
                    elif age > 175:
                        print("Sign up failed: Please enter a valid age!")
                    # Unrealistic ages will not be accepted, user will type age again.
                    else:
                        break
                except ValueError:
                    print("Please enter your age in years only.")
                    
            sex = input("Enter your biological sex (male/female for accuracy) or\nEnter 'none' if other or prefer not to specify:\n> ").strip().lower()
            if sex not in ("male", "female"):
                sex = "none"
            
            # Verification:
            verify = input(f"\nPlease verify the information you have provided by entering 'yes' or 'no':\nUsername: {name} \nWeight: {weight} kg \nHeight: {height} cm \nAge: {age} years \nSex: {sex}\n> ").lower()
            if verify == "yes":
                bmi_value = bmi(weight, height)
        
                print(f"Your BMI is approximately, {bmi_value}.")
                print("It's recommended to", recommend(bmi_value), "weight.")
                while True:
                    goal = input("Enter your weight plan goal (gain/lose/maintain):\n> ").strip().lower()
                    if goal in ("gain", "lose", "maintain"):
                        break
                
                # Adding User Record to Database:
                with open('database.txt', 'a') as fileHandle:
                    fileHandle.write(f"\n{name},{weight},{height},{age},{sex},{goal}")  # User and their information is added into database.txt

                all_names.append(name) 
                database.append([name, str(weight), str(height), str(age), sex, goal])  # User and their information is added into database list
                
                # BMI and Recommendation:
                while True:
                    try:
                        days = int(input("Enter days per week you work out:\n> "))
                        activity_factor = af_from_days(days)
                        break
                    except ValueError:
                        print("Please enter days in whole digits only!")
                
                print("Congrats! You have successfully signed up.")
                
                bmr_value = bmr(weight, height, age, sex)
                calories_needed = tdee(bmr_value, activity_factor)
                if goal == "gain":
                    calories_needed += 500
                elif goal == "lose":
                    calories_needed -= 500
                print(f"You need to eat approximately {int(calories_needed)} calories a day. Keep recording calorie intake and workout days.")
                break
    
    
    #1 Log In:
    elif entered == "1":
        name = input("Enter your username:\n> ").strip().lower()
        if name not in all_names:
            print(f"{name} does not exist in our database, please enter 0 to sign up") # Exists login if user's account does not exist
        else:
            print(f"Welcome, {name}!") 
            
            
            # Loop for Login Menu:
            while True:
                print()
                navigate = input("Enter:\n'1' to see your progress\n'2' to see your bmi\n'3' to see your personal information\n'4' to log out\n> ")
                
                #1.1 Progress:
                if navigate == "1":
                    for l in database:
                        if l[0] == name:
                            user = l
                            break
                    weight = float(user[1])
                    height = float(user[2])
                    age = int(user[3])
                    sex = user[4]
                    goal = user[5]
                    filename = f"{name}.txt"  # "f" before the string allows Python to replace {} with assigned variables, e.g "john.txt"
                        
                    # Reading/Creating User Record:
                    try: # Will try to look for user's record file
                        print("Analyzing Progress...")
                        with open(filename, "r") as fileHandle: # Starts reading user's record file
                            lines = fileHandle.readlines()
                    except FileNotFoundError:
                        lines = record_days(filename, "w")  # Creates user's record file if doesn't exist
                        print("Record created successfully!\n")
                            
                    if len(lines) >= 7:
                        past_seven = lines[-7:] # Past seven days will be used to output the direction of user's progress
                    else:
                        past_seven = lines
                    bmr_value = bmr(weight, height, age, sex)
                    net_cals = 0
                    days = 0
                    
                    for line in past_seven: # Loop won't apply if lines empty
                        updated = line.strip().lower().split(",")
                        if len(updated) != 2:
                            continue
                        # This will ensure if line doesn't have 2 values, line will be skipped and code won't crash
                        gym, calories = updated
                        try:
                            calories = int(calories)
                        except ValueError:
                            continue
                        activity_factor = 1.55 if gym == "yes" else 1.2
                        
                        tdee_value = tdee(bmr_value, activity_factor)
                        net_cals += calories - tdee_value
                        days += 1
                    
                    
                    
                    # User's weekly progress will be outputted:

                    try:
                        avg = net_cals / days
                    except ZeroDivisionError:
                        print("Invalid data record... please add recorded days first.")
                        continue
                    
                    weekly_change = avg * days / 7700   # 7700 kcals approximately equals 1kg
                    print("\nWeekly Progress:")
                    if avg > 0:
                        print(f"Calorie Surplus: +{int(round(avg))} kcal/day --> Gained = {round(weekly_change, 2)} kg")
                    elif avg < 0:
                        print(f"Calorie Deficit: {int(round(avg))} kcal/day --> Lost = {round(abs(weekly_change), 2)} kg")
                    else:
                        print("\nWeight Maintained")

                    
                    # User's overall progress since sign up will also be outputted:
                    overall_cals = 0
                    for line in lines:
                        updated = line.strip().lower().split(",")
                        if len(updated) != 2:
                            continue
                        
                        gym, calories = updated
                        try:
                            calories = int(calories)
                        except ValueError:
                            continue
                        activity_factor = 1.55 if gym == "yes" else 1.2
                        
                        tdee_value = tdee(bmr_value, activity_factor)
                        overall_cals += calories - tdee_value
                    
                    overall_change = overall_cals / 7700  # 7700 calories approx. = 1 kg
                    overall_change_sign = "+" + str(round(overall_change, 2)) if overall_change > 0 else str(round(overall_change,2))
                    print(f"Overall change since sign up: {overall_change_sign} kg")
                
                        
                    
                        
                    print()
                    if days >= 7:
                        if goal == "gain":
                            if avg > 0:
                                print("You're on track to gaining weight. Good Job!")
                            else:
                                print("You're below target. Try increasing calorie intake.")
                        elif goal == "lose":
                            if avg < 0:
                                print("You're on track to losing weight. Good Job!")
                            else:
                                print("You're above target. Try decreasing calorie intake.")
                        else:
                            if abs(avg) < 100:  # This allows a leeway of + or - 100 kcals
                                print("You're on track to maintaining weight. Good Job!")
                            elif avg < 0:
                                print("You're below target. Try increasing calorie intake.")
                            else:
                                print("You're above target. Try decreasing calorie intake.")
                    else:
                        print("Keep recording more days for higher accuracy.")  # Fewer recorded days are not sufficient to determine direction 
                            
                    print()
                    
                    while True:
                        more = input("Would you like to add more days? (yes/no)\n> ").strip().lower()
                        if more in ("yes","no"):
                            break
                        print("Invalid entry. Please try again.")
                    
                    # if user wishes to add more days:
                    if more == "yes":
                        record_days(filename, "a")
                        print("New data successfully entered! Re-run to see updated results.\n")
                                
                        
                
                #1.2 BMI:
                elif navigate == "2":
                    for l in database:
                        if l[0] == name:
                            weight = float(l[1])
                            height = float(l[2])
                            bmi_value = bmi(weight, height)
                            goal = l[5]
                            print(f"Your current BMI is approximately {bmi_value}.")
                            print("It's recommended to", recommend(bmi_value), "weight.")
                            print(f"Your chosen goal was to {goal} your weight.")
                            break
                
                
                #1.3 Personal Info:
                elif navigate == "3":
                    for l in database:
                        if l[0] == name:
                            # This will display user's info entered upon sign up.
                            print(f"Username: {l[0]}\nWeight: {l[1]} kg (initial)\nHeight: {l[2]} cm\nAge: {l[3]} years\nGender: {l[4]}\nGoal: {l[5]}")
                
                
                #1.4 Log Out:
                elif navigate == "4":
                    print(f"Goodbye, {name}!")
                    break # Exits login.
    
    else:
        print("Program Ended")
        break # Exits run/debugging.
        
        
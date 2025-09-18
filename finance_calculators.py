# This program allows the user to:
# ~Calculate the amount of interest earned on an investment (simple or compound).
# or
# ~Calculate the monthly repayment amount on a bond (home loan).


import math  # Importing math module for power calculations

# Ask the user for their name and greet them
# Introduce the programme
name = input("Please enter your name: ")
print(f"Hi, {name}! Welcome to your finance calculator.")

# Display options for the user
print('''Investment - to calculate the amount of interest you'll earn on 
your investment.''')
print('''Bond       - to calculate the amount you'll have to pay on a home 
loan.''')

# Define possible choices
input_1 = "investment"
input_2 = "bond"

# Loop until valid input is entered
# Print error message for invalid input
while True:
   # Prompt user to choose between investment or bond
   choice = input(f'''Enter either "{input_1}" or "{input_2}" from the menu above to proceed: ''').strip().lower()

   # Check if the user's input is valid
   if choice == input_1 or choice == input_2:
        print(f"Great! You have chosen {choice}. ")
        break #Exit loop
   else:
        print(f'''Invalid response. Please enter either "{input_1}" or "{input_2}" from the menu above to proceed: ''')

# If user selects investment
if choice == input_1:

    # Get investment details from the user
    # Print error message for invalid input
    # Loop until user enters valid input
    while True:   
        try:
             principal = float(input("How much are you depositing?:£ "))
             break
        except ValueError:
            print ("This is not a number. Please try again.")
    while True: 
        try:
             interest_rate = float(input("Which interest rate would you like to use?( e.g 2 for 2%): "))
             interest_rate = interest_rate / 100
             break
        except ValueError:
            print ("This is not a number. Please try again.")
    while True: 
        try:   
             time1 = int(input("How many years do you plan on investing?: "))
             break
        except ValueError:
            print ("This is not a number. Please try again.")

    # Define possible interest types
    ans1 = "simple"
    ans2 = "compound"
    
    # Ask which type of interest the user wants to use
    # Print error message for invalid input
    while True: 
        interest_type = input(f"Would you like to use {ans1} or {ans2} interest?: " ).strip().lower()
        if interest_type== ans1 or interest_type == ans2:  
           break
        else:
           print("Invalid input. Please type 'simple' or 'compound'.")

    # Display result based on user's interest type choice
    if interest_type == ans1: 
        # Calculate simple interest
        # Simple Interest Formula:
        # A = P * (1 + r * t)
        # where:
        # A = total amount after interest is added
        # P = amount initially deposited
        # r = annual interest rate 
        # t = time in years 
        simple = principal*(1+ interest_rate*time1)
        simple = round(simple, 2)  # Round up to 2 decimal places
        print(f"The amount of interest gained in {time1} years using {ans1} interest is £{simple}.")
    else:
        # Calculate compound interest
        # Compound Interest Formula:
        # A = P * (1 + r)^t
        # where:
        # A = total amount after interest is added
        # P = amount initially deposited
        # r = annual interest rate 
        # t = time in years
        compound = principal*math.pow((1+interest_rate), time1)
        compound = round(compound, 2)  # Round up to 2 decimal places
        print(f"The amount of interest gained in {time1} years using {ans2} interest is £{compound}.")

# If user selects bond
elif choice == input_2:
     # Get bond details from the user
     # Print error message for invalid input
     # Loop until user enters valid input
    while True:
     try: 
       current_value = float(input("What is the current value of the property:£ "))
       break
     except ValueError:
       print ("This is not a number. Please try again.")
    while True:
     try:
       interest_rate2 = float(input ("Which interest rate would you like to use?( e.g 2 for 2%): "))
       interest_rate2 = interest_rate2 / 100 / 12
       break
     except ValueError:
       print ("This is not a number. Please try again.")
    while True:
     try:
       time2 = int(input("How many months do you plan to take to repay the bond?: "))
       break
     except ValueError:
       print ("This is not a number. Please try again.")
      
    # Calculate monthly repayment
    # Bond Repayment Formula:
    # Repayment = (i * P) / (1 - (1 + i)^(-n))
    # where:
    # P = present value of the house
    # i = monthly interest rate (annual rate / 12)
    # n = number of months
    amount = (interest_rate2 * current_value) / (1 - (1 + interest_rate2) ** (-time2))   
    amount = round(amount, 2)  # Round to 2 decimal places

    # Display the monthly repayment amount
    print(f"You are required to repay £{amount} every month for {time2} months.")



name =input("Please enter your name: ")

print(f"Hi {name}, welcome to the age quiz.")

age =int(input("Please enter your age: "))

print(f"You are {age} years old.")

if age < 13:

    print ("You qualify for the kiddie discount")

elif age == 21:

    print("Congrats on your 21st!")

elif age > 100:

   print ("Sorry, you're dead")

elif age >= 65:

    print ("Enjoy your retirement!")
elif age >= 40:

   print ("You're over the hill.")

else :

     print("Age is but a number")
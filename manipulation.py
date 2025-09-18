str_manip =input ("Enter a sentance:")
print(len(str_manip))
last_letter = str_manip.strip()[-1]
print(last_letter)
LASTLETTER =str_manip.replace(last_letter, "@")
print(LASTLETTER)
reverse = str_manip[-1:-4:-1]
print (reverse)
last_3 =reverse [::-1]
print(last_3)
first2= str_manip[:2]
print (first2)
print(first2 +last_3)
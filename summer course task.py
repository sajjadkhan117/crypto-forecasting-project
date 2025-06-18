#task 1
from scipy.stats import alpha

num = float(input("enter a number"))
if num > 10:
    print("the number is positive ")
elif num < 10:
    print("the number is negative")
else:
    print("error")

    # TASK = 2
num = int(input("Enter a number: "))
if num % 2 == 0:
    print("Even number")
else:
    print("Odd number")
    # task 3
a = 30
b = 25
c = 15
if a >= b and a >= c:
    print("the largest number is ", a)
elif b >= a and b >= c:
    print("the largest number is ",b)
else:
    print("largest number is ",c)
    # TASK = 4
marks1 = float(input("Enter marks of subject 1: "))
marks2 = float(input("Enter marks of subject 2: "))
marks3 = float(input("Enter marks of subject 3: "))

avg = (marks1 + marks2 + marks3) / 3
if avg >= 90:
    grade = 'A'
elif avg >= 75:
    grade = 'B'
elif avg >= 60:
    grade = 'C'
elif avg >= 50:
    grade = 'D'
else:
    grade = 'F'
print("Average:", avg, "Grade:", grade)
# TASK = 5
year = int(input("Enter a year: "))
if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    print("Leap Year")
else:
    print("Not a Leap Year")
# TASK =6
ch = input("Enter a character: ").lower()
if ch in 'aeiou':
    print("vowel")
elif ch.isalpha():
    print("consonant")
else:
    print("not a alphabet character")
    #TASK =7
num = int(input("enter a number: "))
if num % 3 == 0 and num % 5 == 0:
    print("Multiple of both 3 and 5 ")
else:
    print("not a multiple of both 3 and 5")

# TASK 8
str1 = input("Enter first 3-letter string: ")
str2 = input("Enter second 3-letter string: ")
if len(str1) == 3 and len(str2) == 3:
    if str1 == str2:
        print("Strings are the same")
    else:
        print("Strings are different")
else:
    print("Please enter exactly 3-letter strings")
    # task = 9
    start = int(input("Enter start value: "))
    end = int(input("Enter end value: "))

    print("Prime numbers between", start, "and", end, "are:")
    for num in range(start, end + 1):
        if num > 1:
            for i in range(2, num):
                if num % i == 0:
                    break
            else:
                print(num)
# TASK = 10
day = input("Enter a day: ").lower()

if day in ["saturday", "sunday"]:
    print("Weekend")
elif day in ["monday", "tuesday", "wednesday", "thursday", "friday"]:
    print("Weekday")
else:
    print("Invalid day")




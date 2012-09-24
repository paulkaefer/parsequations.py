#
# parsequations.py
#
# By Paul Kaefer
# with some ideas contributed by Kevin Germino
#
# v1.0 - Developed between the hours of 9:00 PM and 12:00 PM CST, 2/5/2012.
#
# References
# ==========
# The book I taught myself python with: "Learn Python the Hard Way" 
#     See http://learnpythonthehardway.org/ for more details, including a free version of the book (HTML)
# File I/O: http://www.penzilla.net/tutorials/python/fileio/
# Miscellaneous python information, including documentation on
#     the various functions implemented: http://docs.python.org/
# The ord() function: http://mail.python.org/pipermail/python-win32/2005-April/003100.html
#

#from sys import argv

#script, filename = argv

print ""
print "Welcome to Paul's equation parser."
print ""
print "Hit CTRL+C to exit at any time."
print ""
raw_file = open(raw_input("Enter the file that has the equations: "), 'r')# Opens the file for READING ('w' for writing also deletes what's in it!)
wincupl_file = open(raw_input("\nEnter the file to write the WinCUPL equations to: "), 'w')

temp_file_string = ""

#target.truncate()# Deletes the file

string = raw_file.read()
length = len(string)

big_buff = " "# Kevin Germino wanted me to call it this. So I did. I guess. Yeah...
buffer_position = 0

# if there was an equation on a line, the program will add a semicolon (;)
was_there_stuff_on_this_line = 0

# "There's such a thing as overdocumenting your code... you're pushing it."
#  - Kevin Germino
#
# If you are before the equals sign, it's cool to have a + or * in your variable names.
# (I gotchu, bro!)
have_we_seen_an_equals_sign_yet = 0

# spaces between variables count as * (boolean AND)
variable = 0

# keep track of the last character written, so as not to write two spaces
last_character = "x"

for i in range(0, length):
    if (string[i]=="\n"):
        # new line in file

        # Debugging statement:
        #wincupl_file.write("newline")

        have_we_seen_an_equals_sign_yet = 0

        # clear the buffer
        for j in range(1, buffer_position+1):
            temp_file_string += big_buff[j]
            last_character = big_buff[j]
        big_buff = " "
        buffer_position = 0
        variable = 0

        # if there was text on this line, it will require a semicolon (;)
        if (was_there_stuff_on_this_line==0):
            # do nothing
            a = 0
        else:
            was_there_stuff_on_this_line = 0;
            temp_file_string += ";"
            last_character = ";"

        temp_file_string += string[i]
        last_character=string[i]
    elif (string[i]==" "):
        # clear the buffer
        for j in range(1, buffer_position+1):
            temp_file_string += big_buff[j]
            last_character = big_buff[j]
        big_buff = " "
        buffer_position = 0
        #variable = 0

        # write the original space character to the file
        temp_file_string += string[i]
        last_character=string[i]

        if ((have_we_seen_an_equals_sign_yet==1) and (variable==1)):
            if ((string[i+1]!="+") and (string[i+1]!="*") and (string[i+2]!="+") and (string[i+2]!="*") and (string[i+1]!="\n") and (string[i+2]!="\n")):
                # there is a space instead of a * character
                temp_file_string += "& "# removed one space after it
                last_character = " "
            else:
                # do nothing
                a = 0

        variable = 0

    elif ((string[i]=="'") or (string[i]=="`")):
        # apostrophe (boolean NOT)

        was_there_stuff_on_this_line = 1
    
        # write the NOT character
        temp_file_string += "!"
        last_character = "!"

        # write the variable name (stored in the buffer)
        for j in range(1, buffer_position+1):
            temp_file_string += big_buff[j]
            last_character = big_buff[j]
        big_buff = " "
        buffer_position = 0
        variable = 0

        if (len(string)>(i+2)):
            if ((string[i+1]!="+") and (string[i+1]!="*") and (string[i+2]!="+") and (string[i+2]!="*")):
                # there is a space instead of a * character
                temp_file_string += " & "# removed space before and after
                last_character = " "
        else:
            if (len(string)>(i+1)):# an attempt to eliminate "string index out of range" errors
                if ((string[i+1]!="+") and (string[i+1]!="*")):
                    # there is a space instead of a * character
                    if ((string[i+1]=="\n") or (string[i+2]=="\n")):
                        # do nothing, essentially
                        a = 0
                    else:
                        temp_file_string += " & "# this prints at the end of the line, before the ;
                        # removed space before and after & character
                        last_character = " "

    elif ((string[i]=="*") and (have_we_seen_an_equals_sign_yet==1)):
        # AND

        was_there_stuff_on_this_line = 1

        # clear the buffer
        for j in range(1, buffer_position+1):
            temp_file_string += big_buff[j]
            last_character = big_buff[j]
        big_buff = " "
        buffer_position = 0
        variable = 0

        if (last_character==" "):
            temp_file_string += "&"
            last_character = " "
        else:
            temp_file_string += " & "# removed space before and after
            last_character = "&"
    elif ((string[i]=="+") and (have_we_seen_an_equals_sign_yet==1)):
        # OR

        was_there_stuff_on_this_line = 1

        # clear the buffer
        for j in range(1, buffer_position+1):
            temp_file_string += big_buff[j]
            last_character=big_buff[j]
        big_buff = " "
        buffer_position = 0
        variale = 0

        if (last_character==" "):
            temp_file_string += "#"
        else:
            temp_file_string += " # "
        last_character=" "
    else:
        # other text (variable names, equals signs, comments YOU NAME IT!)
        if (string[i] == "="):
            have_we_seen_an_equals_sign_yet = 1
        big_buff += string[i]
        buffer_position += 1

        # ord() reference: http://mail.python.org/pipermail/python-win32/2005-April/003100.html
        intvalue = ord(string[i])
        if ((intvalue>64) and (intvalue<91)):
            # upper case letter
            variable = 1
        elif ((intvalue>96) and (intvalue<123)):
            # lower case letter
            variable = 1
        #wincupl_file.write(string[i]);

if (buffer_position!=0):
    # clear the buffer
    for j in range(1, buffer_position+1):
        temp_file_string += big_buff[j]
    big_buff = " "
    buffer_position = 0
    # if there was still stuff in the buffer, a semicolon (;) is most likely needed at the end of the file
    temp_file_string += ";\n\n"
    last_character=";"

if ((last_character!=";") and (last_character!="\n")):
    temp_file_string += ";\n\n"

'''
line = first_file.read()
second_file.write(line)
target.write(line2+"\n")
'''

raw_file.close()# Closes the file

# run a pass through the temp file to eliminate & characters that are at the end of the line

length = len(temp_file_string)

for i in range(0, length):
    if ((temp_file_string[i]=="&") and (temp_file_string[i+3]==";")):
        a = 0
    else:
        wincupl_file.write(temp_file_string[i])

wincupl_file.close()

# End of file.


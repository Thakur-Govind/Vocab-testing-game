import numpy as np
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from random import randint

def auth():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope) 
    #make the client_secret.json file yourself by following the link: https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/
    client = gspread.authorize(creds)
    return client
def get_sheet(client):
    sheet = client.open("GRE Words we dont know").sheet1
    #make a sheet like this yourself, snapshot example to be attached later
    return sheet
def add_new_word(sheet):
    word = input("Enter word: ")
    meaning = input("Enter meaning: ")
    list_of_hashes = sheet.get_all_records()
    try:
        sheet.insert_rows([[" "," ",len(list_of_hashes)+1,word,meaning,""]],row=len(list_of_hashes)+2,value_input_option = "USER_ENTERED")
        return "Word added successfully!"
    except:
        return "There seems to have been a problem. Please try again"
def quiz_mode(sheet):
    name = ""
    list_of_hashes = sheet.get_all_records()
    print("Welcome to quiz mode!\n Im gonna keep asking you vocab questions till youre done.\n To stop me, enter the words\"stop it dude\"")
    print("Ready??")
    ans = "yes"
    while ans!= "stop it dude":
        cell=list_of_hashes[randint(1,len(list_of_hashes))]
        word = cell["Word"]
        meaning = cell["Meaning"]
        print("-"*40)
        ans = input("What is the meaning of {}?(remember,\"stop it dude\" to exit): ".format(word))
        if ans in meaning:
            print("Correct! \nMeaning was: ",meaning,"\nGoing to the next one.....\n")
        elif ans == "stop it dude":
            print("Okay, thats it! Ending the quiz....")
        else:
            print("Wrong! \nMeaning was: ",meaning,"\nGoing to the next one.......\n")
        print("_"*40)
    return "Successfully Completed Quiz"
def view_10_words(sheet):
    list_of_hashes = sheet.get_all_records()
    print("Word -- Meaning")
    for i in range(10):
        cell = list_of_hashes[randint(1,len(list_of_hashes))]
        print("{} -- {}".format(cell["Word"],cell["Meaning"]))
client = auth()
ch = ""
print("Welcome to the Vocab app!\n ")
while ch!=0:
    print("-"*40)
    print("\nPlease choose one of the following to continue: \n1.Add a word\n2.View 10 words\n3.Quiz\n0.Exit")
    ch = int(input("Enter your choice [0 to 3]: "))
    if ch==0:
        print("\nThank you")
        break
    elif ch==1:
        print()
        sheet = get_sheet(client)
        print(add_new_word(sheet))
    elif ch==2:
        print()
        sheet = get_sheet(client)
        view_10_words(sheet)
    elif ch==3:
        print()
        sheet = get_sheet(client)
        quiz_mode(sheet)
    
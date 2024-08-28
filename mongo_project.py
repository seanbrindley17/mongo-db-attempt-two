import os
import pymongo
if os.path.exists("env.py"):
    import env
    
MONGO_URI = os.environ.get("MONGO_URI")
DATABASE = "myFirstDB"
COLLECTION = "celebrities"


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e  #Prints could not connect message with placeholder that includes the error message
        
        
def show_menu():  #Menu has full CRUD functionalityl; Create, Read, Edit, Delete.
    print("")
    print("1. Add a record")
    print("2. Find a record by name")
    print("3. Edit a record")
    print("4. Delete a record")
    print("5. Exit")
    
    option = input("Enter option: ")  #Call an input prompt for the user to enter one of the above options
    return option


def get_record():  #Helper function that asks user to find someone by name
    print("")
    first = input("Enter first name > ")
    last = input("Enter last name > ")
    
    try:  #Uses try/except block for searching. If we find someone in the database, store in Mongo Cursor object called doc
        doc = coll.find_one({"first": first.lower(), "last": last.lower()}) #Use find_one() method on the first and last variable which are converted to lower case
    except:
        print("Error accessing database")
    
    if not doc: #If the record we're looking for isn't found
        print("")
        print("Error! No results found")
    
    return doc


def find_record():
    doc = get_record() #Calls get_record() function and stores the results of that in "doc"
    if doc: #If we do get results
        print("") #Print a blank line for neatness
        for k,v in doc.items(): #For loop to iterate through the keys (k) & values (v) within the doc.items() method
            if k != "_id": #Need to check that the key doesn't equal the Mongo ID (_id) as we don't want to display this
                print(k.capitalize() + ": " + v.capitalize()) #If the key isn't the mongo ID, prints both the key and value with first letter capitalised
                

def edit_record():
    doc = get_record()
    if doc:
        update_doc = {} #Creates empty dictionary called update_doc which will be added to while iterating through key/value pairs
        print("")
        for k,v in doc.items():
            if k != "_id": #Filters the ID since we don't want to edit that
                update_doc[k] = input(k.capitalize() + " [" + v + "] > ")  
            #update_doc[k] iterates through the keys, displaying the name of the key capitalised and the original value in square brackets before the input field                                        
                if update_doc[k] == "": #If the new value is left blank i.e. it doesnt need to be changed
                    update_doc[k] = v #Sets the value to be the original value, the field isnt updated
        
        try:
            coll.update_one(doc, {"$set": update_doc})
            print("")
            print("Document updated")
        except:
            print("Error accessing database")
            

def delete_record():
    doc = get_record() #Use get_record() function to search first and last name
    if doc:
        print("")
        for k,v in doc.items():
            if k != "_id": #If not ID
                print(k.capitalize() + ": " + v.capitalize()) #Prints the key and value pair 
        print("")
        confirmation = input("Is this the document you want to delete?\nY or N > ") #Confirmation input for defensive programming
        print("")
        
        if confirmation.lower() == "y": #Uses .lower() so that it doesn't matter if y or Y are inputted 
            try:
                coll.delete_one(doc) #Deletes the selected record
                print("Document deleted")
            except:
                print("Error accessing database")
        else:
            print("Document not deleted") #If anything other than "y" is typed, print this and return to main menu


def add_record(): #Function that will prompt user to input this information and then stores it in these variables
    print("")
    first = input("Enter first name > ")
    last = input("Enter last name > ")
    dob = input("Enter date of birth > ")
    gender = input("Enter gender > ")
    hair_colour = input("Enter hair colour > ")
    occupation = input("Enter occupation > ")
    nationality = input("Enter nationality > ")
    
    new_doc = {  #Builds a dictionary to insert into the database
        "first": first.lower(), #First and Last name use the .lower() method to store names in lower case
        "last": last.lower(),
        "dob": dob,
        "gender": gender,
        "hair_colour": hair_colour,
        "occupation": occupation,
        "nationality": nationality
    }
    
    try: #Try block; try to insert the new_doc dictionary into the globally defined variable for the collection: coll
        coll.insert_one(new_doc)
        print("")
        print("Document inserted") #If successful, print this
    except:
        print("Error accessing the database") #If there's an error, print this
   

def main_loop():
    while True:  #While True means that essentially this function runs forever until stopped
        option = show_menu()  #Calls the show_menu() function every time and stores it in a variable named "option", which is consistent with option in above function
        if option == "1":
            add_record()
        elif option == "2":  #elif meaning else, if
            find_record()
        elif option == "3":
            edit_record()
        elif option == "4":
            print("You have selected option 4")
        elif option == "5":
            print("You have selected option 5")
            conn.close()  #If the user selects 5 which corresponds to the Exit option in the menu, close connection and break loop
            break
        else:
            print("Invalid option")  #If the user enters an invalid option, this is caught and printed to the terminal
        print("") #After menu is displayed, this prints a blank line under it
            
            
conn = mongo_connect(MONGO_URI) #Calls the Mongo connection
coll = conn[DATABASE][COLLECTION] #Create Mongo collection
main_loop() #Calls main_loop function

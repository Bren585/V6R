from database import Database, Character

db = Database()

def printAll(characters):
    print()
    print("| Name       | Gender     |Mood|Love|")
    print("}------------+------------+----+----{")
    for character in characters:
        print(character)
    print()

choice = None
while choice != 0:
    print()
    print("1 - Create a character")
    print("2 - Delete a character")
    print("3 - Edit a character")
    print("4 - Display a character")
    print("5 - Display all characters")
    print("0 - Exit")
    print()

    try:
        choice = int(input(" > "))
    except ValueError:
        choice = None
        continue

    if choice == 1:
        name = input("Name: ")
        if db.characterExists(name):
            print("Character already exists.")
            continue
        db.create(name)
    elif choice == 2:
        name = input("Name: ")
        db.delete(name)
    elif choice == 3:
        name = input("Name: ")
        if not db.characterExists(name):
            print("No such character.")
            continue

        character = Character(db, name)

        while choice != 0:
            print()
            print("1 - Change mood")
            print("2 - Increment mood")
            print("3 - Change love")
            print("4 - Increment mood")
            print("5 - Update gender")
            print("6 - Print %s" % name)
            print("7 - Test pronouns")
            print("0 - Submit changes")
            print()

            try:
                choice = int(input(" > "))
            except ValueError:
                choice = None
                print("Invalid Choice.")
                continue

            if choice == 1:
                try:
                    character.mood = int(input("New mood: "))
                    print("Changed mood to %i." % character.mood)
                except ValueError:
                    print("Invalid value.")

            elif choice == 2:
                try:
                    character.mood += int(input("Increment amount: "))
                    print("Changed mood to %i." % character.mood)
                except ValueError:
                    print("Invalid value.")
    
            elif choice == 3:
                try:
                    character.love = int(input("New love: "))
                    print("Changed love to %i." % character.love)
                except ValueError:
                    print("Invalid value.")
            
            elif choice == 4:
                try:
                    character.love += int(input("Increment amount: "))
                    print("Changed love to %i." % character.love)
                except ValueError:
                    print("Invalid value.")
                
            elif choice == 5:
                value = input("New gender: ")
                if value != 'male' and value != 'female' and value != 'none':
                    print("Invalid gender. (male, female, none)")
                else:
                    character.gender = value
                    character.refreshPronouns()
                    print("Gender and Pronouns updated.")

            elif choice == 6:
                print()
                print("| Name       | Gender     |Mood|Love|")
                print("}------------+------------+----+----{")
                print(character)
                print()

            elif choice == 7:
                print("""
                Oh, sorry, you can't sit here. This is %s's seat. 
                You can ask %s if you want, %s talking to %s friend over there.
                Yeah, sorry. The seat's %s.
                """ % (character.name,       character.pronouns[1], character.pronouns[5],
                      character.pronouns[2], character.pronouns[3]))

            elif choice != 0:
                print("Invalid Choice.")

        character.save()
        choice = None

    elif choice == 4:
        name = input("Name: ")
        if not db.characterExists(name):
            print("No such character.")
            continue
        print()
        print("| Name       | Gender     |Mood|Love|")
        print("}------------+------------+----+----{")
        print(Character(db, name))
        print()
    elif choice == 5:
        printAll(db.loadCharacters())
    elif choice != 0:
        print("Invalid Choice.")
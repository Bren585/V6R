import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('character_data.db')
        self.cursor = self.connection.cursor()
        # Create the Tables
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS 'genders' (
            'id' INTEGER PRIMARY KEY,
            'gender' VARCHAR(7) NOT NULL,
            'personal' VARCHAR(7) NOT NULL,
            'indirect' VARCHAR(7) NOT NULL,
            'dirPossesive' VARCHAR(7) NULL,
            'indPossesive' VARCHAR(7) NULL,
            'article' VARCHAR(7) NULL,
            'contraction' VARCHAR(7) NULL)
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS 'characters' (
            'id' INTEGER PRIMARY KEY,
            'name' VARCHAR(45) NOT NULL,
            'gender' INT NULL,
            'mood' INT NOT NULL,
            'love' INT NOT NULL)
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS 'savedata' (
            'id' INTEGER PRIMARY KEY,
            'filename' VARCHAR(45),
            'username' VARCHAR(45))
        """)
        
        self.cursor.execute("SELECT * FROM genders")
        if (len(self.cursor.fetchall()) != 3):
            self.cursor.execute("DELETE FROM genders WHERE 1 = 1")
            self.cursor.execute("""
                INSERT INTO genders 
                    (gender, personal, indirect, dirPossesive, indPossesive, article, contraction)
                VALUES 
                    ('none',   'they', 'them', 'their', 'theirs', 'are', \"they're\"),
                    ('male',   'he',   'him',  'his',   'his', 'is', \"he's\"),
                    ('female', 'she',  'her',  'her',   'hers', 'is', \"she's\")
            """)
        
        self.cursor.execute("SELECT * FROM savedata")
        if (len(self.cursor.fetchall()) != 1):
            self.cursor.execute("DELETE FROM savedata WHERE 1 = 1")
            self.cursor.execute("INSERT INTO savedata (filename) VALUES ('010.txt')")

    def __del__(self):
        self.connection.commit()
        self.connection.close()

    def execute(self, command):
        self.cursor.execute(command)

    def create(self, name):
        self.cursor.execute("INSERT INTO characters (name, mood, love, gender) VALUES ('%s', 0, 0, 1)" % name)

    def delete(self, name):
        self.cursor.execute("DELETE FROM characters WHERE name = '%s'" % name)

    def getCharacterData(self, name):
        self.cursor.execute("""
        SELECT * FROM characters AS c
        JOIN genders AS g
        ON c.gender = g.id
        WHERE c.name = '%s'
        """ % name)
        try:
            r = self.cursor.fetchall()[0]
            return r[1:2] + r[3:5] + r[6:]
        except IndexError:
            return []
    
    def characterExists(self, name):
        self.cursor.execute("SELECT 1 FROM characters WHERE name = '%s'" % name)
        return len(self.cursor.fetchall()) != 0
    
    def getGenderData(self, gender):
        self.cursor.execute("SELECT * FROM genders WHERE gender = '%s'" % gender)
        try:
            return self.cursor.fetchall()[0]
        except IndexError:
            return []
    
    def loadCharacters(self):
        self.cursor.execute("""
        SELECT name FROM characters AS c
        JOIN genders AS g
        ON c.gender = g.id
        """)
        characters = []
        for name in self.cursor.fetchall():
            characters.append(Character(self, name[0]))
        return characters

class Character:
    def __init__(self, db, name):
        self.db   = db
        self.name = name
        if self.db.characterExists(name):
            request = db.getCharacterData(name)
            self.mood     = request[1]
            self.love     = request[2]
            self.gender   = request[3]
            # Pronouns
            self.p = request[4]
            self.i = request[5]
            self.dp = request[6]
            self.ip = request[7]
            self.a = request[8]
            self.c = request[9]
            self.pronouns = request[4:]
        else:
            db.create(name)
            self.mood = 0
            self.love = 0
            request = self.db.getGenderData('none')
            self.gender   = 'none'
            # Pronouns
            self.p = request[2]
            self.i = request[3]
            self.dp = request[4]
            self.ip = request[5]
            self.a = request[6]
            self.c = request[7]
            self.pronouns = request[2:]
    
    def __del__(self):
        try:    self.save()
        except: pass

    def __repr__(self):
        return "| {:<10} | {:<10} | {:<2} | {:<2} |".format(str(self.name), self.gender, self.mood, self.love)
    
    def save(self):
        if   self.gender == 'male':
            gender = 2
        elif self.gender == 'female':
            gender = 3
        else:
            gender = 1

        self.db.execute(""" 
        UPDATE characters
        SET mood   = %i,
            love   = %i,
            gender = %i
        WHERE name = '%s'
        """ % (int(self.mood), int(self.love), gender, self.name))

    def refreshPronouns(self):
        request = self.db.getGenderData(self.gender)
        self.p = request[2]
        self.i = request[3]
        self.dp = request[4]
        self.ip = request[5]
        self.a = request[6]
        self.c = request[7]
        self.pronouns = request[2:]
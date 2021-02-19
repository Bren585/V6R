# Overview

V6R (short for vvvvvvar) is a programming language I built for no good reason. It is limited in use and application.
V6R contains one "Interpreter" class (and various supporting logics) to be used for reading in .txt files and interpreting them as some new code, executable in python3, effectively a V6R compiler.

[Software Demo Video](https://youtu.be/Ik8WHY8vNHE)

# Syntax

; Line End :

Put a semi colon at the end of every line or I will personally crash your program.
This allows for multi-line code, so the following code snippets are interpreted the same.
```
$if(
%num >= 10
) {
  $print("That's a big number");
  $print("Wow");
};

$if(%num>=10){$print("That's a big number");$print("Wow");};
```

\# Comments : 
```
# I am a comment! The compiler will ignore me.
%foo = %bar; #It'll read that <--- code just fine, but I'm invisible!
```
As soon as the compiler sees a '#' symbol, it will discard everything to the right of the symbol and move on to the next line.

% Variables : (Single-value only)
```
%foo = 0;
%bar = 1;
%foo = %bar + 2;
%foo += 3;
$print(%foo); # Will print 6
```
The compiler will treat the symbols follwing a '%' symbol as a variable. Variables can be manipulated with many of the common operators (+, -, *, /, >=, ==, <, etc.). The compiler can also handle member variables, as in the following.
```
%user = $load(%username);
%user.mood += 5;
$print(%user.mood);
```
The two datatypes the compilier can implicitly handle are String and Int. To print strings and ints together, the following syntax can be used while using the "announce" function.
```
%name = "bren";
%age = 53;
$announce("Happy birthday, ^ %name +! You're turning %age this year!");
# out > Happy birthday, Bren! You're turning 53 this year!
```
The '^' symbol will capitalize the first letter of the following word. The '+' symbol will combine the following characters with the previous word. 
```
$announce("^ hello"); # Hello
$announce("he +llo"); # hello
```
These symbols are used only for formatting variables into strings in the announce and speak functions.

$ Functions : ()
```
$print("Hello World!");
```
A function call requires a '$' symbol, denoting where the function is, and should be followed by a parenthetical containing the arguments of the function. 

# Functions

|Name|Argc|Description|
|-|-|-|
|print|1|Just the Python Print() function
|input|0|Just the Python Input() function
|clear|0|Prints 50 '\n' symbols to clear the console
|if|1|Honestly not much. It just evaluates lines in a following {} section if the argument is true
|loadFile|0|Loads a filename saved in a database.
|loadUser|0|Loads a username saved in a database.
|saveFile|1|Saves a given filename into a database.
|saveUser|1|Saves a given username into a database.
|create|1|Creates a character in the character database with a given name.
|load|1|Returns a character object loaded from the database with a given name.
|save|0|Saves a character object into the database.
|speak|2|A special print command, that prints a given speaker "saying" given speech.
|announce|1|A special print command. See variables section.
|pause|0|Wait for user to press enter before continuing.
|jump|1|Stop executing code in the current file, and switch to a new file.
|stop|0|Stop executing code. Exit program.

# Development Environment

Python 3 with my [Character Database Software](https://github.com/Bren585/Character-Database).

# Useful Websites

* [W3Schools](https://www.w3schools.com/)

# Future Work

* Fix Substitution methods to replace vairables, functions, and operators all at once.
* Fix compliler to handle line-start symbols the same as all other symbols.
* Add capability to create and store functions and arrays. 

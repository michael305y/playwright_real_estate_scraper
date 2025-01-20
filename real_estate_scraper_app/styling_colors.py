"""
======  MODULE FOR USING ANSI COLORS TO STYLE PRINT STATEMENTS =============

1. RESET_COLOR  will reset the color previously chosen   
2. BLUE_COLOR   Changes the text color to blue.
3. CYAN_COLOR   Changes the text color to cyan.
4. RED_COLOR    Changes the text color to red
5. MAGENTA_COLOR  Changes the text color to magenta

Example: print(f"{GREEN_COLOR}This is green text{RESET_COLOR}")

"""

GREEN_COLOR = "\033[32m"  # ANSI escape sequence for green color 
RESET_COLOR = "\033[0m"   
BLUE_COLOR = "\033[34m"
CYAN_COLOR = "\033[36m" 
RED_COLOR = "\033[31m"
MAGENTA_COLOR =  "\033[35m"



if __name__ == '__main__':
    print(f"{GREEN_COLOR}This is green text{RESET_COLOR}")
    print(f"{BLUE_COLOR}This is blue text{RESET_COLOR}")
    print(f"{CYAN_COLOR}This is cyan text{RESET_COLOR}")
    print(f"{RED_COLOR}This is red text{RESET_COLOR}")
    print(f"{MAGENTA_COLOR}This is magenta text{RESET_COLOR}")

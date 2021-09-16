import math
from sympy import pi, E, N
def expand(digits = 10, mathex = "pi", multiplier = 1):
    """
    INPUT: digits - The number of digits past the decimal the user is interested in 
           mathex - The mathematical expression the user is intersted in 
           multliplier - Multipliers to the mathematical expression
    BEHAVIOR: intakes desired math expression and outputs a string 
                representation for later processing
    OUTPUT: A string representation of digits past the decimal
    """
    if mathex == "pi":
        myval = str(N(multiplier * pi, digits))
        return myval
    if mathex == "e":
        myval = str(N(multiplier * E, digits))
        return myval
    
def is_prime(user_num = 1):
    """
    INPUT: Integer number to check if prime
    BEHAVIOR:check if the user input is a prime number
        by iteratively checking the ceiling of square roots
    OUTPUT: string that shows "prime" or "not prime"
    """
    if user_num > 1 and isinstance(user_num, int) == True:  
        #if the number is greater than 1 AND it is a whole integer
        #then we iterate
        #from the input number to the cieling of the square root
        for num in range(2, int(math.sqrt(user_num)+1)):
            #if we find a whole number divisor, then the user input
            #is not a FALSE
            if (user_num % num) == 0:
                return False
        return True
    #if the number input is less than one, 
    #then we have a NON prime immediately
    return False

def sliding(my_string = "8309735", window=3):
    """
    INPUT: string representation of a long integer. 
        sliding window length

    BEHAVIOR:user inputs an integer and the function 
    will generate sliding windows of that input 
    length from a string representation of a number (iterable)
    
    OUTPUT: list of integers. 
    each integer is of specified sliding window length
    """
    #intialize main empty list that will hold all sub-lists
    all_list = []
    my_string = str(my_string.split('.')[-1])
    #store the length of the string
    total_len = len(my_string)
    #create for loop to iterate through 
    #all possible sliding windows of the string
    for i in range(0,(total_len - window+1)):
        #create a substring that stores a window
        substr = my_string[i:i+window]
        #If the substring starts with 0, then we go to the next iteration of the loop
        #we want integers with entire length. starting with 0 will break this
        if substr[0] == '0':
            continue
        #append the string to the main list
        all_list.append(int(substr))
    #return the main list that now contains all sublist
    return all_list

def digit_prime(pdigits = 10, pmathex = "pi", pmultiplier = 1, pwindow=3):
    """
    INPUT: 
        pdigits - The number of digits past the decimal the user is interested in
        pmathex - The mathematical expression the user is intersted in 
        pmultliplier - Multipliers to the mathematical expression
    
    BEHAVIOR: 
        uses the helper functions 'expand', 'sliding' and 'is_prime' to 
        determine the first prime in the decimal expansion of user input's window length 
        from the user input's mathematical expression
    
    OUTPUT: 
        First prime digit of user specified length from 
        decimal expansion of user input mathematical expression
    """
    #create string with 'expand' function
    my_expression = expand(digits = pdigits, mathex = pmathex, multiplier = pmultiplier)
    #create list of integers with length of user specified window
    slide_list = sliding(my_string = my_expression, window = pwindow)
    #iterate through the list and check if the value is prime
    for i in slide_list:
        if is_prime(i) == True:
            #if prime, we end the loop by returning the integer
            return(i)

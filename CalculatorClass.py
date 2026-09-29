#program to write calculator using class
import re

def checknum(n):
	"""
	Returns either negative, positive
	or float number

	raises:
		Error for other strings
	"""
	try:
		res= float(n)
		if res.is_integer():
			return int(res)
		else:
			return float(n)
	except (ValueError, TypeError):
		raise TypeError(f"Error: Expected int got {n}")	

	
def checkint(n):
	"""
	returns only integer

	raise:
		Error for float and strings
	"""
	try:
		return int(n)
	except (ValueError, TypeError):
		raise TypeError(f"Error: Expected int got {n}")

#converting the infix to postfix with only numerical expression
#which retrieved from the root window

def infix_to_postfix(expression: str):
    # Define operator precedence (higher number = higher precedence)
    # tokens = re.findall(r'\d+(?:\.\d+)?|[\+\-\*\%\/\(\)\^]', expression)
 	
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2,'%':2, '^': 3, 'u-' :4,"√" :5,"2√":6,}
    
    # Track right-associative operators (like exponentiation '^')
    associativity = {'2√':'Right','√':'Right','u-' : 'Right','^': 'Right', '+': 'Left', '-': 'Left', '*': 'Left', '/': 'Left','%':'Left'}
    
    stack = []      # Stack to store operators and parentheses
    output = []     # List to build the final postfix expression
    # Process the expression character by character
    for char in expression:
        # 1. If the character is alphanumeric, it's an operand; add it directly to output
        # if char.replace(".","",1).isdigit():
        if isinstance(char,(int,float)):
        	output.append(char)
            
        # 2. If it's an opening parenthesis, push it onto the stack
        elif char == '(':
            stack.append(char)
            
        # 3. If it's a closing parenthesis, pop from stack to output until '(' is found
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack:
                stack.pop() # Discard the opening parenthesis '('
                
        # 4. If the character is an operator
        elif char in precedence:
            while stack and stack[-1] != '(' and (
                (associativity[char] == 'Left' and precedence[char] <= precedence[stack[-1]]) or
                (associativity[char] == 'Right' and precedence[char] < precedence[stack[-1]])
            ):
                output.append(stack.pop())
            stack.append(char)
            
    # 5. Pop any remaining operators left in the stack to the output
    while stack:
        output.append(stack.pop())
    # messagebox.showinfo("postfixexpression",output)

    return output


#converting a infix to postfix which has trigonometric functions
#which retrieved from the trigonometric window

def infix_trig_postfix(expression: str):
    # Define operator precedence (higher number = higher precedence)
    # tokens = re.findall(r'\d+(?:\.\d+)?|[\+\-\*\%\/\(\)\^]', expression)
    trig_pat = r"[a-zA-Z]+\(\d+(?:\.\d+)?\)"
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2,'%':2, '^': 3, 'u-' :4,"√" :5,"2√":6}
    
    # Track right-associative operators (like exponentiation '^')
    associativity = {'2√':'Right','√':'Right','u-' : 'Right','^': 'Right', '+': 'Left', '-': 'Left', '*': 'Left', '/': 'Left','%':'Left'}
    
    stack = []      # Stack to store operators and parentheses
    output = []     # List to build the final postfix expression
    # Process the expression character by character

    for char in expression:
        # 1. If the character is alphanumeric, it's an operand; add it directly to output
        # if char.replace(".","",1).isdigit():
        if isinstance(char,(int,float)) or re.fullmatch(trig_pat,char):
        	output.append(char)
            
        # 2. If it's an opening parenthesis, push it onto the stack
        elif char == '(':
            stack.append(char)
            
        # 3. If it's a closing parenthesis, pop from stack to output until '(' is found
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack:
                stack.pop() # Discard the opening parenthesis '('
                
        # 4. If the character is an operator
        elif char in precedence:
            while stack and stack[-1] != '(' and (
                (associativity[char] == 'Left' and precedence[char] <= precedence[stack[-1]]) or
                (associativity[char] == 'Right' and precedence[char] < precedence[stack[-1]])
            ):
                output.append(stack.pop())
            stack.append(char)
            
    # 5. Pop any remaining operators left in the stack to the output
    while stack:
        output.append(stack.pop())
    # messagebox.showinfo("postfixexpression",output)

    return output

#trig tokens is to have the expression in the form of a list
#which retrieved from trigonometry window
def trig_tokens(expression):
    """Splits expression into tokens and flags unary minus as 'u-'."""

    pattern = r"\)(?=[a-zA-Z])"
    trig_pat = r"[a-zA-Z]+\(\d+(?:\.\d+)?\)"

    if re.search(pattern, expression):
        expression1 = re.sub(r"\)(?=[a-zA-Z])", r")*", expression)
    else:
        expression1 = expression

    raw_tokens = re.findall(
        r'[a-zA-Z]+\(\d+(?:\.\d+)?\)|\d+(?:\.\d+)?|[()+\-/*%^√]',
        expression1
    )

    tokens = []

    for i, token in enumerate(raw_tokens):

        if token == '-':
            # Unary minus
            if i == 0 or raw_tokens[i - 1] in {
                '+', '-', '*', '/', '(', '%', '^', '√'
            }:
                tokens.append('u-')
            else:
                tokens.append('-')

        elif token == "√":
            # Square root
            if i == 0 or raw_tokens[i - 1] in {
                '+', '-', '*', '/', '(', '%', '^'
            }:
                tokens.append('2√')
            else:
                tokens.append('√')

        #check when the token is trig func

        elif re.fullmatch(trig_pat, token):
            tokens.append(token)

        #checks when the token is integer
        elif token.isdigit():
            tokens.append(int(token))

        #check when the token is float
        elif re.fullmatch(r'\d+\.\d+', token):
            tokens.append(float(token))

        else:
            #when the token is an operator
            tokens.append(token)
#returns the all tokens in the form a list including trig funcs
    return tokens 



#unary is to convert the numerical expression in to the list of items

def check_unary(expression):
    """Splits expression into tokens and flags unary minus as 'u-'."""
    # Match numbers, multi-character tokens, or single operators
    pattern=r"\)\d+"
    if re.search(pattern,expression): #replaces ex:(3+5)4 to (3+5)*4
    	expression1=re.sub(r"\)(\d+)", r")*\1", expression)
    else:
    	expression1=expression
    raw_tokens = re.findall(r'\d+\.\d+|\d+|[+\-*/%()^√]', expression1.replace(" ", ""))
    
    tokens = []
    for i, token in enumerate(raw_tokens):
        if token == '-':
            # Unary if it's the first token or follows another operator/'('
            if i == 0 or raw_tokens[i-1] in {'+', '-', '*', '/', '(','%','^','√'}:
                tokens.append('u-')
            else:
                tokens.append('-')
        elif token =="√":
        	if i == 0 or raw_tokens[i-1] in {'+', '-', '*', '/', '(','%','^'}:
        		tokens.append('2√')
        	else:
        		tokens.append('√')
        else:
            # Convert numeric strings to actual integers or floats
            if token.isdigit():
                tokens.append(int(token))
            elif re.match(r'^\d+\.\d+$', token):
                tokens.append(float(token))
            else:
                tokens.append(token)
        #retuns the numerical expression in the form of list
    return tokens


#to calculate the factorial of a number which only a integer

def factorial_number(num: int)->int:
	n=num
	if n<0:
		raise ValueError("Error: Expected +ve value")
	fact_number=1
	if n ==0:
		return 1
	while n > 0:
		fact_number=fact_number*n
		n-=1
	return fact_number

	#to know whether the integer number is even or odd
    #only +ve integer 

def is_odd_or_even(num: int)->str:
	n=num
	if not isinstance(n,int):
		raise TypeError(f"Error: Expected integer got {type(n)}")
	if n < 1:
		raise ValueError(f"Error: Negative integer not allowed")
	if n%2 == 0:
		return "Even"
	elif n%2!=0:
		return "Odd"

#to calculate the greatest common divisor of two +ve numbers

def gcd_two_number(num1: int,num2: int)->int:
	n1=checkint(num1)
	n2=checkint(num2)
	if n1<0 or n2<0:
		raise ValueError("Error: Expected +ve value")
	gcd=1
	for i in range(1,min(n1,n2)+1):
		if n1 % i == 0 and n2 % i == 0:
			gcd=i
	return gcd


#to calculate the Least common multiple of two +ve integers

def lcm_two_number(num1: int,num2: int)->int:
	n1=checkint(num1)
	n2=checkint(num2)
	return abs(n1*n2)//gcd_two_number(n1,n2)

#calculator class to calculate two operands with operator [+|/|-|*|%]

class Calculator:

    #returns the addition of two operands

	def add(self,a,b):
		return a+b

    #returns the product of two operands
	def multiply(self,a,b):
		return a*b

    #returns the difference of two operands
	def subtract(self,a,b):
		return a-b

    #returns the division of two operands
	def division(self,a,b):
		if b!=0:
			return a/b
		elif b == 0:
			raise ZeroDivisionError("Error: division by zero not allowed")

    #returns modulus of two operands
	def modulo(self,a,b):
		if b!=0:
			return a%b
		elif b == 0:
			raise ZeroDivisionError("Error: division by zero not allowed")


# #main()

# trig_string="cos(45)+65-atan(56)/sin(44)"
# res=trig_tokens(trig_string)
# print(res)
# evaluate=infix_trig_postfix(res)
# print(evaluate)
import tkinter as tk
from tkinter import messagebox
from trigonometry_cal import open_trig_window
import re
import math
import CalculatorClass

#validate the values entered in textbox on calculator window

def validate_input(input_val):
	allowed ="0123456789+-!^%/*()√e."

	return all(char in allowed for char in input_val)

#validate the input in gcd/lcm window and trigonometry window
def only_digits(input_digit):
	allowed ="0123456789"

	return all(char in allowed for char in input_digit)


#check whether the number on root window textbox is single number or not

def is_single_number(val):
	pattern = r"\(-?\d+(?:\.\d+)?\)|-?\d+(?:\.\d+)?"
	return bool(re.fullmatch(pattern,val))

#get the number from the root window textbox

def get_single_number():
	val=get_input()
	if not is_single_number(val):  #checks single number or not
		get_result("ERROR!")
		return 
	if val.startswith("(") and val.endswith(")"):
		val = val[1:-1]
	return CalculatorClass.checknum(val) #returns string num to int or float


# calculates power operations with square and cube
def power_operations(value):
	try:
		a=get_single_number()
		if isinstance(a,(int,float)):
			if value == "x^2":
				result=a**2
			elif value == "x^3":
				result=a**3
			get_result(result)
		else:
			pass
	except ValueError as e:
		get_result(e)


#calculate the square root and cube root operations

def root_operations(value):
	try:
		a=get_single_number()
		if isinstance(a, (int,float)):
			if value == "2√x":
				result= a**0.5
			elif value == "3√x":
				result=a**(1/3)
			get_result(result)
		else:
			pass
	except ValueError as e:
		get_result(e)


#calculates the eulers numbers 
def eulers_number():
	try:
		a=get_single_number()
		if isinstance(a,(int,float)):
			result=a*2.718281828
			get_result(result)
		else:
			pass
	except ValueError as e:
		get_result(e)


#retrieves the last digit from the expression or the single digit 
#given in root window textbox and performs
# the operations like odd/even, 1/x, log10, e^x,! and |x|

def last_digit_method(value):
	val=get_input()
	last_digit=re.search(r"\d+(\.?\d+)?$",val)
	# messagebox.showinfo("last_digit",last_digit.group())
	if last_digit:
		start=last_digit.start()
		number=last_digit.group()
		number=CalculatorClass.checknum(number)
		if value=="!":
			if number >= 0 and number <= 100:
				if isinstance(number,float) and not number.is_integer():
					get_result("requires integer")
				else:
					res=CalculatorClass.factorial_number(number)
					if len(str(res))>10:
						res=f"{res:.2e}"
					text_bar.delete(start,tk.END)
					text_bar.insert(tk.END,res)
					get_result(f"{number}!={res}")
		elif value == "1/x":
			if number == 0:
				get_result("cannot divide by zero")
			else:
				res=1/number
				res=f"{res:.2f}"
				text_bar.delete(start,tk.END)
				text_bar.insert(tk.END,res)
				get_result(f"1/{number}={res}")
		elif value == "log₁₀":
			if number<0:
				get_result("Undefined")
			elif number>=0:
				res=math.log10(number)
				res=f"{res:.2f}"
				text_bar.delete(start,tk.END)
				text_bar.insert(tk.END,res)
				get_result(f"log₁₀({number})={res}")
		elif value == "10ˣ":
			res=pow(10,number)
			res=f"{res:.2f}"
			text_bar.delete(start,tk.END)
			text_bar.insert(tk.END,res)
			get_result(f"10^{number}={res}")
		elif value == "|x|":
			res = abs(number)
			text_bar.delete(start,tk.END)
			text_bar.insert(tk.END,res)
			get_result(f"|{number}|={res}")
		elif value == "O/E":
			res=CalculatorClass.is_odd_or_even(number)
			if number <= 0:
				get_result("Negative value!")			
			else:
				text_bar2.config(state="normal")
				if text_bar2.get():
					text_bar2.delete(0,tk.END)
					text_bar2.insert(tk.END,f"{number}:{res}")
				else:
					text_bar2.insert(tk.END,f"{number}:{res}")
				text_bar2.config(state="readonly")
		elif value == "eˣ":
				# messagebox.showinfo("eulers expo",val)
				res=math.e**number
				res=f"{res:.2f}"
				get_result(f"{res}")

	#if the expression is in the form of (-x)

	if re.match(r"\(-\d+(?:\.\d+)?\)$", val):  
		last=re.search(r"\(-\d+(?:\.\d+)?\)$", val)			
		if last:
			val = val.replace("(", "").replace(")", "")
			val=CalculatorClass.checknum(val)
			if value == "10ˣ":							
				res=pow(10,val)
				# messagebox.showinfo("res",res)
				get_result(f"10^{val}={res}")
			if value == "log₁₀":
				if val<0:
					get_result("Undefined")
			if value == "!":
				if val <0:
					get_result("Undefined")
			if value == "O/E":
				if val<=0:
					get_result("Negative Undefined")
			if value == "|x|":
				res=abs(val)
				get_result(f"|{val}|={res}")
			if value ==  "%":
				res=val*(1/100)
				get_result(f"{val}%={res}")
			if value == "eˣ":
				# messagebox.showinfo("eulers expo",val)
				res=math.e**val
				get_result(f"{res}")

#to make the value in the form of unary i.e, +/-X
#if the value is in the form of x then it converts to -x
#if the values is in the form of -x then it converts to x
#while clicking on -/+ button

def text_unary():
	textval =text_bar.get()
	if not textval:
		return
	elif textval:
		last_digit=re.search(r"\d+(\.?\d+)?$",textval)
		if last_digit:
			start=last_digit.start()
			number=last_digit.group()
			text_bar.delete(start,tk.END)
			text_bar.insert(tk.END,f"(-{number})")
		match=re.search(r"\(-\d+(?:\.\d+)?\)$", textval)
		if match:
			start=match.start()
			number=match.group()
			text_bar.delete(start,tk.END)
			text_bar.insert(tk.END,number[2:-1])
		else:
			pass

#to enter the result for the expression on second textbox 
#of root window after calculating
def text_clear():
	if text_bar.get() or text_bar2.get():
		text_bar.delete(0,tk.END)
		text_bar.insert(tk.END,"")
		text_bar2.config(state="normal")
		text_bar2.delete(0,tk.END)
		text_bar2.insert(tk.END,"")
		text_bar2.config(state="readonly")

#to delete the values one by one while clicking backspace or 
#pressing the backspace from keyboard
def text_bksp():
	if text_bar.get():
		text_bar.delete(len(text_bar.get())-1,tk.END)

#evaluate the expression which was converted from infix to postfix
def evaluate_postfix(expression):
	stack=[]
	for ch in expression:
		# if isinstance(ch,(int,float)):
		n1=None
		n2=None
		if re.fullmatch(r"\d+(?:\.\d+)?", str(ch)):
			val=float(ch)
			stack.append(clean_number(val))
			continue
		if ch =='u-':
			if len(stack) < 1:
				return "Invalid expression"
			operand=stack.pop()
			stack.append(clean_number(-operand))
			continue
		if ch == "2√":
			if len(stack) < 1:
				return "Invalid expression"
			n2=stack.pop()
			# messagebox.showinfo("value 2 root",ch)
			if n2<0:
				return "Undefined"
			result = pow(n2,(1/2))
			stack.append(clean_number(result))
			continue

		if ch == "√":
			if len(stack) < 2:
				return "Invalid expression"
			n2=stack.pop() #value
			n1=stack.pop() #root
			# messagebox.showinfo("root n1 and value n2",f"{n1} {n2}")
			if n1==0:
				return "Undefined"
			if n2<0:
				if n1 %2 ==0:
					return "Undefined"
				else:
					result=-pow(abs(n2),(1/n1))
			else:
				result=pow(n2,(1/n1))
			# messagebox.showinfo("result",result)
			stack.append(clean_number(result))
			continue

		if ch == "%" and len(stack)==1:
			n2=stack.pop()
			stack.append(clean_number(n2/100))
			continue
		if len(stack)<2:
			return "Invalid expression"

		b=stack.pop()
		a=stack.pop()
		# messagebox.showinfo("two parameters:",f"a={a},b={b} & ch={ch}")					
		if ch=="+":
			result=cal.add(a,b)
		elif ch=="-":
			result=cal.subtract(a,b)
		elif ch=="/":
			if b != 0:
				result=cal.division(a,b)
			elif b==0:
				return "Undefined"	
		elif ch=="*":
			result=cal.multiply(a,b)
		elif ch=="%":
			if b==0:
				return "Undefined"				
			result=cal.modulo(a,b)
			# print(result)
		elif ch=="^":
			result=pow(a,b)
		else:
			return "Invalid expression"
		stack.append(clean_number(result))
		
	if len(stack)==1:
		# print("finalstack: ",stack)
		return(stack[-1])
	return "Invalid expression"


def handle_operator(operator,a,b):
	pass

def clean_number(value):
    # return int(value) if isinstance(value, float) and value.is_integer() else value
    if isinstance(value,float) and value.is_integer():
    	return int(value)
    return value

def calculate():
	textval=get_input()
	if textval:
		if re.findall(r"[\+\-\*\%\^\√/]",textval):
			unary_values=CalculatorClass.check_unary(textval)
			# messagebox.showinfo("unary_values",f"{unary_values}, {type(unary_values)}")
			postfixexpression=CalculatorClass.infix_to_postfix(unary_values)
			# messagebox.showinfo("postfixexpression",f"{postfixexpression}, {type(postfixexpression)}")
			result= evaluate_postfix(postfixexpression)
			if result is not None:
				get_result(result)
			else:
				pass
	else:
		pass


def get_result(result):
	text_bar2.config(state="normal")
	text_bar2.delete(0,tk.END)
	text_bar2.insert(tk.END,result)
	text_bar2.config(state="readonly")

def get_input():
	return text_bar.get()

#main()#        
root = tk.Tk()
root.title("CALCULATOR")
root.geometry("300x400")
root.resizable(False,False)
root.configure(bg="lightblue")
cal=CalculatorClass.Calculator()

vcmd=(root.register(validate_input),"%S")

textval=""
result=0

text_bar=tk.Entry(root,width=20,font=("Arial",16,"bold"),justify="right",validate="key",validatecommand=vcmd)
text_bar.insert(tk.END,"")
text_bar.grid(row=0,column=0,sticky="nsew",columnspan=4,padx=0,pady=0,ipady=10)

text_bar2=tk.Entry(root,width=20,font=("Arial",16,"bold"),justify="right",state="readonly")
text_bar2.insert(tk.END,"")
text_bar2.grid(row=1,column=0,sticky="nsew",columnspan=4,padx=0,pady=0,ipady=10)

for i in range(4):
	root.columnconfigure(i,weight=1)
root.rowconfigure(0, weight=0)
root.rowconfigure(1, weight=0)
for i in range(2,11):
    root.rowconfigure(i, weight=1)


def button_click(value):
	if text_bar2.get():	
		text_bar.delete(0,tk.END)
		get_result("")
	
	if value == "=":
		val=get_input()
		if val:
			if re.search(r"[\d+]",val):
				calculate()
		else:
			pass
	
	elif value=="x^y":
		val=get_input()
		if not val:
			pass
		else:
			text_bar.insert(tk.END,"^")		
	
	elif value=="x^2":
		power_operations(value)
	
	elif value=="x^3":
		power_operations(value)
	
	elif value=="2√x":
		root_operations(value)
	
	elif value=="3√x":
		root_operations(value)
	
	elif value=="O/E" or value=="eˣ":
		last_digit_method(value)	

	elif value == "1/x":
		last_digit_method(value)

	elif value=="+" or value == "-" or value == "/" or value == "*" or value == "%" or value == "^":
		val = get_input()
		if not val:
			pass
		if val and val[-1] in "+-/*%^":
			pass
		else:
			if re.search(r"[\d+]",val):
				text_bar.insert(tk.END,value)
			else:
				pass

	elif value == "10ˣ":
		last_digit_method(value)

	elif value == '!':
		last_digit_method(value)

	elif value == '|x|':
		last_digit_method(value)

	elif value == 'log₁₀':
		last_digit_method(value)
		
	elif value == "e":
		eulers_number()

	elif value == "x√y":
		val=get_input()
		last_digit=re.search(r"\d+(\.?\d+)?$",val)
		if last_digit:
			start=last_digit.start()
			number=last_digit.group()
			text_bar.delete(start,tk.END)
			text_bar.insert(tk.END,f"√({number})")					
		last=re.search(r"\(-\d+(?:\.\d+)?\)$", val)			
		if last:
			start=last.start()
			number=last.group()
			text_bar.delete(start,tk.END)
			text_bar.insert(tk.END,f"√{number}")
	else:
		val = get_input()
		match = re.search(r"√\((\d+(?:\.\d+)?)\)?$", val)
		neg_match=re.search(r"√\(-(\d+(?:\.\d+)?)\)?$", val)
		if match :
			start = match.start()
			number = match.group()
			# messagebox.showinfo("number",number)
			text_bar.delete(start, tk.END)
			text_bar.insert(tk.END, f"{value}{number}")
		elif neg_match:
			start = neg_match.start()
			number = neg_match.group()
			# messagebox.showinfo("number",number)
			text_bar.delete(start, tk.END)
			text_bar.insert(tk.END, f"{value}{number}")
		else:
			text_bar.insert(tk.END, value)

def match_regex(string):
	pass



buttons_text=["x^y","x^3","x^2","3√x",
				"2√x","x√y","(",")",
				"1","2","3","+",
				"4","5","6","-",
				"7","8","9","/",
				"0",".","*","%",
				"eˣ","1/x","!","=",
				"10ˣ","log₁₀","|x|","O/E",
				"e"
				]
buttons={}
for i,text in enumerate(buttons_text):
    button = tk.Button(
        root,
        text=text,
        width=3,
        height=2,
        bg="#c9ecdf",
        fg="black",
        activebackground="skyblue",
        activeforeground="white",
        font=("Arial",12,"bold"),
        command=lambda value=text: button_click(value)
    )
    buttons[text]=button

    row = (i // 4) + 2
    column = i % 4

    button.grid(row=row, column=column,padx=0,pady=0,sticky="nsew")


button_unary=tk.Button(root,text="±",width=3,height=2,bg="#c9ecdf",
	fg="black",
	activebackground="skyblue",
	activeforeground="white",
	font=("Arial",12,"bold"),command=text_unary)  
button_unary.grid(row=10,column=1,padx=0,pady=0,sticky="nsew")

button_backspace=tk.Button(root,text="←",width=3,height=2,bg="#c9ecdf",
	fg="black",
	activebackground="skyblue",
	activeforeground="white",
	font=("Arial",12,"bold"),command=text_bksp)  #⌫
button_backspace.grid(row=10,column=2,padx=0,pady=0,sticky="nsew")

button_clear=tk.Button(root,text="C",width=3,height=2,
	bg="#c9ecdf",fg="black",
	activebackground="skyblue",
	activeforeground="white",
	font=("Arial",12,"bold"),command=text_clear)
button_clear.grid(row=10,column=3,padx=0,pady=0,sticky="nsew")

def open_gcd_lcm():

	def gcd_click():
		val1=text_number1.get()
		val2=text_number2.get()
		if val1 and val2:
			res=CalculatorClass.gcd_two_number(val1,val2)
			get_gcd_lcm(res)
		else:
			pass

	def lcm_click():
		val1=text_number1.get()
		val2=text_number2.get()
		if val1 and val2:
			res=CalculatorClass.lcm_two_number(val1,val2)
			get_gcd_lcm(res)
		else:
			pass

	def get_gcd_lcm(result):
		text_result.config(state="normal")
		text_result.delete(0,tk.END)
		text_result.insert(tk.END,result)
		text_result.config(state="readonly")


	gcd_lcm=tk.Toplevel(root)
	gcd_lcm.title("GCD LCM Calculator")
	gcd_lcm.geometry("350x350")
	gcd_lcm.resizable(False,False)
	gcd_lcm.configure(bg="skyblue")
	vcmd_digits=(gcd_lcm.register(only_digits),"%S")
	for i in range(4):
		gcd_lcm.columnconfigure(i, weight=1)
	for i in range(7):
		gcd_lcm.rowconfigure(i, weight=1)
	
	label=tk.Label(gcd_lcm,
        text="GCD and LCM Calculator",
        width=3,
        height=2,
        bg="#c9ecdf",
        fg="black",
        font=("Arial",12,"bold"),)
	label.grid(row=0,column=0,sticky="nsew",columnspan=4,padx=5,pady=15,ipady=5)
	label_number1=tk.Label(gcd_lcm,
        text="Number 1:",
        width=3,
        height=2,
        bg="#c9ecdf",
        fg="black",
        font=("Arial",10,"bold"),)
	label_number1.grid(row=1,column=0,sticky="nsew",columnspan=1,padx=5,pady=5,ipady=5)

	text_number1=tk.Entry(gcd_lcm,width=20,font=("Arial",16,"bold"),justify="right",validate="key",validatecommand=vcmd_digits)
	text_number1.insert(tk.END,"")
	text_number1.grid(row=2,column=0,sticky="nsew",columnspan=4,padx=0,pady=0,ipady=10)

	label_number2=tk.Label(gcd_lcm,
        text="Number 2:",
        height=2,
        bg="#c9ecdf",
        fg="black",
        font=("Arial",10,"bold"))
	label_number2.grid(row=3,column=0,sticky="nsew",columnspan=1,padx=5,pady=5,ipady=5)
	
	text_number2=tk.Entry(gcd_lcm,width=20,font=("Arial",16,"bold"),justify="right",validate="key",validatecommand=vcmd_digits)
	text_number2.insert(tk.END,"")
	text_number2.grid(row=4,column=0,sticky="nsew",columnspan=4,padx=0,pady=0,ipady=10)

	label_result=tk.Label(gcd_lcm,
        text="Result :",
        height=2,
        bg="#c9ecdf",
        fg="black",
        font=("Arial",10,"bold"))
	label_result.grid(row=5,column=0,sticky="nsew",columnspan=1,padx=5,pady=5,ipady=5)

	text_result=tk.Entry(gcd_lcm,width=20,font=("Arial",16,"bold"),justify="right",state="readonly")
	text_result.insert(tk.END,"")
	text_result.grid(row=6,column=0,sticky="nsew",columnspan=4,padx=0,pady=0,ipady=10)

	gcd_button=tk.Button(gcd_lcm,text="GCD",height=2,bg="#c9ecdf",
		fg="black",font=("Arial",10,"bold"),command=gcd_click)	
	gcd_button.grid(row=7,column=0,sticky="nsew",columnspan=1,padx=5,pady=20,ipady=5)
	lcm_button=tk.Button(gcd_lcm,text="LCM",height=2,bg="#c9ecdf",
		fg="black",font=("Arial",10,"bold"),command=lcm_click)	
	lcm_button.grid(row=7,column=1,sticky="nsew",columnspan=2,padx=5,pady=20,ipady=5)

lcm_gcd_button=tk.Button(root,text="lcm/gcd",width=3,height=2,bg="#c9ecdf",
	fg="black",font=("Arial",12,"bold"),command=open_gcd_lcm)
lcm_gcd_button.grid(row=11,column=0,columnspan=2,padx=0,pady=0,sticky="nsew")

trigonometry_button=tk.Button(root,text="Trigonometry",width=3,height=2,bg="#c9ecdf",
	fg="black",font=("Arial",12,"bold"),command=lambda: open_trig_window(root))
trigonometry_button.grid(row=11,column=2,columnspan=3,padx=0,pady=0,sticky="nsew")

root.mainloop()
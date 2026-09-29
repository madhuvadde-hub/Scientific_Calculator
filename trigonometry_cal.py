# trigonometry calculator
# | Function | Normal     | Inverse     |
# | -------- | ---------- | ----------- |
# | `sin`    | `sin(x)`   | `asin(x)`   |
# | `cos`    | `cos(x)`   | `acos(x)`   |
# | `tan`    | `tan(x)`   | `atan(x)`   |
# | `cot`    | `1/tan(x)` | `atan(1/x)` |
# | `sec`    | `1/cos(x)` | `acos(1/x)` |
# | `csc`    | `1/sin(x)` | `asin(1/x)` |

import tkinter as tk
from tkinter import messagebox
import math
import CalculatorClass
import re

inv_mode=False #declaring initially a inv mode as false

#to store trig funcs in buttons_trig dictionary

buttons_trig={}

#to store the numerics and operators with Inv in buttons dictionary

buttons={}

#to store the paranthesis with degree/radians in buttons_para dictionary

buttons_para={}

#declaring the expression textbox value as global

text_value=None

#declaring a result textbox as a global
text_res=None

#calling a calculator class from calculatorClass.py file
cal=CalculatorClass.Calculator()

#dictionary of inverse_trig created
#to display the inverse trig funcs on buttons while
# Inv button is True

inverse_trig = {
    "sin": "asin",
    "cos": "acos",
    "tan": "atan",
    "sinh": "asinh",
    "cosh": "acosh",
    "tanh": "atanh",
    "sec": "asec",
    "csc": "acsc",
    "cot": "acot",
    "sech": "asech",
    "csch": "acsch",
    "coth": "acoth"}

#dictionary of norma_trig created to display the normal trig func while 
#the Inv mode is False
	
normal_trig={
	"sin": "sin",
    "cos": "cos",
    "tan": "tan",
    "sinh": "sinh",
    "cosh": "cosh",
    "tanh": "tanh",
    "sec": "sec",
    "csc": "csc",
    "cot": "cot",
    "sech": "sech",
    "csch": "csch",
    "coth": "coth"}		

def validate_input(input_val):
	allowed ="0123456789.+-!^%/*()√e"

	return all(char in allowed for char in input_val)

def only_digits(input_digit):
	allowed ="0123456789"

	return all(char in allowed for char in input_digit)

trig_functions = r'(?:sin|cos|tan|cot|sec|csc|sinh|cosh|tanh|coth|sech|csch|asin|acos|atan|acot|asec|acsc|asinh|acosh|atanh|acoth|asech|acsch)'
trig_pattern = rf'^(?:(?:{trig_functions}\(-?\d+(?:\.\d+)?\)|-?\d+(?:\.\d+)?)(?:[+\-*/%^])?)+$'

token_trig=rf'^(?:{trig_functions}\(-?\d+(?:\.\d+)?\))'

def trig_evaluate(expression):

	# token_trig=rf'^(?:{trig_functions}\(-?\d+(?:\.\d+)?\))'

	for i,token in enumerate(expression):
		if re.match(token_trig,str(token)) :

			# to check whether the expression has trig funcs or not
			# if so, retrieve the trig func and separate trig func and its numberic value
			# into func and num

			func,num=re.match(r'([a-z]+)\((-?\d+(?:\.\d+)?)\)', token).groups()

			# convert the string number into float or integer

			num=CalculatorClass.checknum(num)
			# print(type(num),num)

			res=trig_cal(func,num)
			# messagebox.showinfo("res",res)
			if res is not None:
				# if the trig func is invalid returns "Undefined"
				if res=="Undefined":
					return "Undefined"
				else:
					# replace the result of trig func into its original
					#position as a trig func

					expression[i]=res		
	return expression

def calculate_expression(expression):  
# calculates the converted trig funcs into numerical expression
	stack=[]
	for ch in expression:
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


def clean_number(value):
    # return int(value) if isinstance(value, float) and value.is_integer() else value
    if isinstance(value,int):
    	return int(value)
    else:
    	return float(value)

# function to calculate the trigonometry funcs which are coming from 
# trig_evaluate(expression) function

def trig_cal(value,number):
	if value == "asin":
		if -1 <= number <= 1:
			val=math.asin(number)
			val=math.degrees(val)
			return round(val,2)
		else:
			return "Undefined"
	elif value == "sin":
			val=math.radians(number)
			val=math.sin(val)
			return round(val,2)
	elif value == "acos":
		if -1 <= number <= 1:
			val=math.acos(number)
			val=math.degrees(val)
			return val
		return "Undefined"
	elif value == "cos":
		val=math.radians(number)
		val=math.cos(val)
		return round(val,2)
	elif value == "atan":
		val=math.atan(number)
		val=math.degrees(val)
		return round(val,2)
	elif value == "tan":
		if number % 180 == 90 or number % 180 == -90:
			return "Undefined"
		val=math.radians(number)
		val=math.tan(val)
		return round(val,2)
	elif value == "acot":
		if number == 0:
			return 90
		val=math.atan(1/number)
		val=math.degrees(val)
		if val < 0:
			val+=180
		return round(val,2)
	elif value == "cot":
		if number%180==0:
			return "Undefined"
		val=math.radians(number)
		val=1/math.tan(val)
		return round(val,2)
	elif value == "asec":
		if -1 <= number <= 1:
			return "Undefined"
		val=math.acos(1/number)
		val=math.degrees(val)
		return round(val,2)
	elif value == "sec":
		if number % 180 == 90 or number % 180 == -90:
			return "Undefined"
		val = math.radians(number)
		return round(1 / math.cos(val), 2)
	elif value == "acsc":
		if -1 < number < 1:
			return "Undefined"
		val=math.asin(1/number)
		val=math.degrees(val)
		return round(val,2)			
	elif value == "csc":
		if number%180 == 0:
			return "Undefined"
		val=math.radians(number)
		val=1/math.sin(val)
		return round(val,2)
	elif value == "asinh":
		return round(math.asinh(number),2)
	elif value == "sinh":
		return round(math.sinh(number),2)
	elif value == "acosh":
		if number <1 :
			return "Undefined"
		return round(math.acosh(number),2)
	elif value == "cosh":
		return round(math.cosh(number),2)
	elif value == "atanh":
		if -1 < number <1:
			return round(math.atanh(number),2)
		return "Undefined"			
	elif value == "tanh":
		return round(math.tanh(number),2)
	elif value == "acoth":
		if -1 <= number <= 1:
			return "Undefined"
		return round((math.acosh(number) / math.asinh(number)),2)
			# return 0.5* math.log((number+1)/(number-1))
	elif value == "coth":
		if number == 0:
			return "Undefined"
		return round((math.cosh(number) / math.sinh(number)),2)
	elif value == "asech":
		if 0 < number <= 1:
			return round(math.acosh(1 / number), 2)
		else:
			return "Undefined"
	elif value == "sech":
		return round((1/math.cosh(number)),2)
	elif value == "acsch":
		if number%180 == 0:
			return "Undefined"
		return round((1/math.asinh(number)),2)
	elif value == "csch":
		return round((1/math.sinh(number)),2)

#def toggle_inv to change the boolean value of 
#inv_mode when the Inv button is clicked

def toggle_inv():
	global inv_mode
	inv_mode=not inv_mode

#retrieves and returns the expression from the
#expression text value

def get_textvalue():
	return text_value.get()

#to display the result on result textbox

def get_text_result(result):

	#displays the result in below textbox of trigonometry window

	text_res.config(state="normal")
	text_res.delete(0,tk.END)
	text_res.insert(tk.END,result)
	text_res.config(state="readonly")

def text_clear():

#clears the both textboxes when the "C" button is clicked

	if text_value.get() or text_res.get():
		text_value.delete(0,tk.END)
		text_value.insert(tk.END,"")
		text_res.config(state="normal")
		text_res.delete(0,tk.END)
		text_res.insert(tk.END,"")
		text_res.config(state="readonly")

def text_bksp():
	#deletes the text from upper textbox one by one while clicking on
	#backspace or key board backspace

	if text_value.get():
		text_value.delete(len(text_value.get())-1,tk.END)

def open_trig_window(parent):

	#creating trigonometry window from the parent window

	trig_window=tk.Toplevel(parent)	
	trig_window.title("Trigonometry Calculator")
	trig_window.geometry("400x400")
	trig_window.resizable(False,False)
	trig_window.transient(parent)
	trig_window.grab_set()
	vcmd=(trig_window.register(validate_input),"%S")
	# parent.wait_window(trig_window)

	for i in range(6):
		trig_window.columnconfigure(i,weight=1)

	trig_window.rowconfigure(0, weight=0)
	trig_window.rowconfigure(1, weight=0)

	for i in range(2,6):
		trig_window.rowconfigure(i, weight=0)
	
	global text_value
	global text_res
	
	#textbox to enter the expression

	text_value=tk.Entry(trig_window,width=20,
		font=("Arial",12,"bold"),
		justify="right")#,validate="key",validatecommand=vcmd)
	text_value.insert(tk.END,"")
	text_value.grid(row=0,column=0,columnspan=6,sticky="nsew",padx=0,pady=0,ipady=10)

# textbox to display the result

	text_res=tk.Entry(trig_window,width=20,font=("Arial",12,"bold"),
		justify="right",state="readonly")
	text_res.insert(tk.END,"")
	text_res.grid(row=1,column=0,columnspan=6,sticky="nsew",padx=0,pady=0,ipady=10)

#Numerical buttons under the two textboxs with inverse button and 
#operators [+-/*^%]

	buttons_text=["1","2","3","4","5","+",
				"6","7","8","9","0","-",
				"Inv","=",".","/","*","%",]

	for i,text in enumerate(buttons_text):
		button = tk.Button(trig_window,text=text,width=3,height=2,
			bg="#c9ecdf",fg="black",activebackground="skyblue",
			activeforeground="white",font=("Arial",12,"bold"),
			command=lambda value=text: button_click(value))

		buttons[text]=button

		row = (i // 6) + 2
		column = i % 6

		button.grid(row=row, column=column,padx=0,pady=0,sticky="nsew")

#trigonometry buttons under the numerical buttons

	button_trig=["sin","cos","tan","sinh","cosh","tanh",
				"sec","csc","cot","sech","csch","coth"]
	
	for i,text in enumerate(button_trig):
		button = tk.Button(trig_window,text=text,width=3,height=2,
			bg="#c9ecdf",fg="black",activebackground="skyblue",
			activeforeground="white",
			font=("Arial",12,"bold"),
			command=lambda value=text: trig_button_click(value))

		buttons_trig[text]=button

		row = (i // 6) +5
		column = i % 6

		button.grid(row=row, column=column,padx=0,pady=0,sticky="nsew")

#paranthesis buttons with degree/radians , backspace and clear on same row

	button_paranthesis=["(",")","deg","rad"]
	for i, text in enumerate(button_paranthesis):
		button_p =  tk.Button(trig_window,text=text,width=3,height=2,
			bg="#c9ecdf",fg="black",activebackground="skyblue",
			activeforeground="white",
			font=("Arial",12,"bold"),
			command=lambda value=text: button_para_click(value))
		if text in ["deg","rad"]:
			button_p.config(state="disabled")		
		buttons_para[text]=button_p
		row=(i//6)+8
		column=i%6
		button_p.grid(row=row, column=column,padx=0,pady=0,sticky="nsew")
		

#backspace button

	button_bksp=tk.Button(trig_window,text="←",width=3,height=2,
			bg="#c9ecdf",fg="black",activebackground="skyblue",
			activeforeground="white",
			font=("Arial",12,"bold"),command=text_bksp )	
	button_bksp.grid(row=8, column=4,columnspan=1,padx=0,pady=0,sticky="nsew")

#clear button

	button_clear=tk.Button(trig_window,text="C",width=3,height=2,
			bg="#c9ecdf",fg="black",activebackground="skyblue",
			activeforeground="white",
			font=("Arial",12,"bold"),command=text_clear)	
	button_clear.grid(row=8, column=5,columnspan=1,padx=0,pady=0,sticky="nsew")

def button_para_click(value):

	# to display the paranthesis on first textbox while clicking on them
	if value in ["(",")"]:
		text_value.insert(tk.END,f"{value}")
	else:
		pass

def button_click(value):

#to display the Inv, numeric , operators on textbox while clicking on them

	if value == "Inv":
		toggle_inv()
		if inv_mode:
			# buttons["Deg"].config(text="Rad")
			for name , inverse in inverse_trig.items():
				buttons_trig[name].config(text=inverse)
		else:
			# buttons["Deg"].config(text="Deg")
			for name , normal in normal_trig.items():
				buttons_trig[name].config(text=normal)

	elif value in ["1","2","3","4","5","6","7","8","9","0"]:

		text_value.insert(tk.END,value)

	elif value in ["+","-","/","*","%",".","^"]:
		val = get_textvalue()
		if not val:
			pass
		if val and val[-1] in "+-/*%^.":
			pass
		else:
			if re.search(r"[\d+]",val):
				text_value.insert(tk.END,value)
			else:
				pass		
	elif value=="=":
	
		#when the = is clicking , trig expression is calculated

		val=get_textvalue()
		if val:
			if re.findall(r"[\+\-\*\%\^\√/]",val):

				# take the expression from textbox and list the items

				tokens=CalculatorClass.trig_tokens(val)

				# convert the list of items from infix to postfix

				postfix_exp=CalculatorClass.infix_trig_postfix(tokens)

				#evaluate the trigonometry funcs resulting into numeric values

				res_exp=trig_evaluate(postfix_exp)
				if res_exp is not None:

					#if the trig funcs has any undefined one results returns as "Undefined"

					if res_exp=="Undefined":
						get_text_result("Undefined")
					else:

						#calculates all numerical expressions 

						result=calculate_expression(res_exp)
						get_text_result(result)	
			else:
				if re.match(token_trig,str(val)) :
					# to check whether the expression has trig funcs or not
					# if so, retrieve the trig func and separate trig func and its numberic value
					# into func and num

					func,num=re.match(r'([a-z]+)\((-?\d+(?:\.\d+)?)\)', val).groups()

			# convert the string number into float or integer

					num=CalculatorClass.checknum(num)
			# print(type(num),num)

					res=trig_cal(func,num)
					get_text_result(res)

#regex of trig funcs with numerics

operators=["+","-","/","*","%","^"]
def trig_button_click(value):

	#When any of the trig func is clicked , checks whether func is normal mode or 
	#inverse mode and displays on the first textbox

	trig_val=text_value.get()
	if re.fullmatch(trig_pattern,trig_val):
		get_text_result("")
		if inv_mode:
			text_value.insert(tk.END,f"a{value}(")
		else:
			text_value.insert(tk.END,f"{value}(")
	elif not trig_val:
		get_text_result("")
		if inv_mode:
			text_value.insert(tk.END,f"a{value}(")
		else:
			text_value.insert(tk.END,f"{value}(")
SCIENTIFIC CALCULATOR:
======================

A Desktop calculator with GCD/LCM and trigonometry functions developed using Python and Tkinter

FEATURES:
=========

1. Basic Arithmatic Operations:
	
	- Addition
	- Subtraction
	- Multiplication
	- Division
	- Modulus

2. Mathematical Operations:
	
	- Power
	- Sqaure
	- Cube
	- Square root
	- Cube root
	- Nth root
	- Reciprocal
	- Factorial
	- Percentage
	- Absolute Value
	- Logarithm
	- Exponential

3. Trigonometric Functions:

	- sin
	- cos
	- tan
	- cot
	- sec
	- cosec(csc)
	

4. Hyperbolic Functions:

	- sinh
	- cosh
	- tanh
	- coth
	- sech
	- cosech(csch)

5. Trigonometric Modes:

	- Deg -> yet to develop
	- Rad -> yet to develop
	- Inverse Trigonometric functions

6. Other features

	- GCD
	- LCM
	- Parenthesis
	- Expression evaluation
	- Input validation
	- Error /  domain handling

This calculator does not use eval() funtion.

Expressions are retrived from the textbox and converted them from infix notation to postfix notation and
then evaluated using postfix evaluator.

example :

	5 + 3 * 2

above expression converted according to operator precedence before evaluation,
either the expression is numerical expression or trigonometric experssion with numerics.

To calculate the GCD/LCM and trigonometric functions a separate sub windows has developed.
In GCD/LCM window , calculated using two integers.

In Trigonometric window, bot normal and hyperbolic functions developed with inversion functions.

example:

	tan(45)+sec(90)-34/
asin(1)

above expression is conveted according to operator precedence before evaluation, which is retrieved from the textbox.

Yet degree and radian mode need to develop in this project


PROJECT STRUCTURE:
==================

CalculatorClass.py

	contains the calculator logic and mathematical operations

tkinter_calculator.py

	contains main calculator GUI with GCD/LCM sub window

trigonomtry_cal.py

	contains trigonometry calculator window and functionality
extentions.
	selenium IDE https://chrome.google.com/webstore/detail/selenium-ide/mooikfkahbdckldjjndioackbalphokd?hl=en
Conventions.
    A. Indentation
	    # Aligned with opening delimiter.
	    foo = long_function_name(var_one, var_two,
	                             var_three, var_four)

	B. Imports
		from subprocess import Popen, PIPE

	C. Whitespace in Expressions and Statements
		spam(ham[1], {eggs: 2})
		foo = (0,)
		ham[1:9], ham[1:9:3], ham[:9:3], ham[1::3], ham[1:9:]
		spam(1)
		dct['key'] = lst[index]
		x = 1
		x = x*2 - 1
		def munge(sep: AnyStr = None) -> PosInt:
		def complex(real, imag=0.0):
		if foo == 'blah':
		    do_blah_thing()
		
	D. Naming Conventions
		* 	Non-public method begin with a single underscore
		** 	with words separated by underscores

		Packages
			lowercase

		Module
			lower case

		Class 
			UpperCaseCamelCase
		
		Functions 
			lowercase

		Variable
			lowercase

		Bool Variable
			is_ + lowercase

		Arguments
			lowercase

		Global
			should be all lowercase

		Constant
			fully capitalized

pip3 freeze > requirements.txt

Usefull commands
	show enviroment variable path in ps: 			$ENV:path

	get Python version: 					python --version
	call python module:					python -m

	list installed packages: 				python -m pip list
	uninstall package:					python -m pip uninstall 'pckagename'
	create virtual enviroment:				python -m venv C:\Users\mpaarmann\MyProjects\md_365\.venv

Create repository
        python3 -m venv C:\OneDrive\Test_Automat\.venv
        Create pth file in C:\OneDrive\Test_Automat\.venv\Lib\site-packages\WAWi.pth contain(c:\OneDrive\Test_Automat)
        cd C:\OneDrive\Test_Automat\.venv\Scripts
		run activate.bat
		pip3 install --upgrade pip

install Package
	Appium-Python-Client==3.1.0
	comtypes==1.1.14
	dict2xml==1.7.3
	pyodbc==4.0.35
	PyQt5==5.15.9
	PyQt5-Qt5==5.15.2
	PyQt5-sip==12.11.1
	pywin32==306
	pywinauto==0.6.8
	PyYAML==6.0.1
	selenium==4.14.0
	six==1.16.0
	urllib3==1.26.15
	xmltodict
	pytest==7.4.2
	pytest-html==4.0.2
	pytest-xdist==3.3.1

pip3 install -r requirements.txt
pip list

My Usefull Shortkeys
	comment ctrl+k ctrl+c
	uncomment ctrl+k ctrl+u

	""" shift+alt+a

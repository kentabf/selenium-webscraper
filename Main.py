import sys
import os
import datetime
import importlib

def update_ui(name):
	last_time = datetime.datetime.now()

	ui_file = open('UI_text.txt', 'r')
	text = ''
	for line in ui_file:
		if line.startswith('META'):
			line = 'META: ' + name + ': ' + str(last_time) + '\n'
		text += line
	ui_file.close()
	ui_file = open('UI_text.txt', 'w')
	ui_file.write(text)
	ui_file.close()



ui_file = open('UI_text.txt', 'r')
print('')
for line in ui_file:
	if not (line.startswith('META')):
		print(line)
	else:
		parts = line.split(': ')
		print('** Most recently you performed ' + parts[1] + ' at ' + parts[2][:-1] + ' **')
		break
ui_file.close()


program_choice = input('Which component do you want to run?: ')

if program_choice == '01':
	curr_path = os.path.dirname(os.path.realpath(__file__))
	sys.path.append(curr_path+'/01_setup')
	import setup as component
	component.run_component()
	update_ui('01_setup')
elif program_choice == '02':
	curr_path = os.path.dirname(os.path.realpath(__file__))
	sys.path.append(curr_path+'/02_scrape')
	import srape as component
	component.run_component()
	update_ui('02_scrape')
elif program_choice == '03':
	curr_path = os.path.dirname(os.path.realpath(__file__))
	sys.path.append(curr_path+'/03_dividedata')
	import dividedata as component
	component.run_component()
	update_ui('03_dividedata')
elif program_choice == '04':
	curr_path = os.path.dirname(os.path.realpath(__file__))
	sys.path.append(curr_path+'/04_parsehtml')
	import parsehtml as component
	component.run_component()
	update_ui('04_parsehtml')
elif program_choice == '05':
	curr_path = os.path.dirname(os.path.realpath(__file__))
	sys.path.append(curr_path+'/05_google')
	import google as component
	component.run_component()
	update_ui('05_google')
elif program_choice == 'q':
	sys.exit('You quit the program.')
	
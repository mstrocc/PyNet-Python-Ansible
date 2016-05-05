#!/usr/bin/env/python

from ciscoconfparse import CiscoConfParse
# define your function
def main():
	'''
	Find all of the crypto map entries in the file (lines that begin with 'crypto map CRYPTO')and print out the children of each crypto map.
	'''
	# define the file you wish to parse and make it a callable object
	cisco_file = '/Users/mstrocchia/Python_Training/Python4Network/GIT/pynet/pyth_ans_ecourse/class1/cisco_ipsec.txt'
	# define an object that uses ciscoconfparse() then pass it the file object
	cisco_cfg = CiscoConfParse(cisco_file)
	# define an objct that appends the .find_objects function to your ciscoconfparse object and give it search criteria 
	crypto_maps = cisco_cfg.find_objects("^crypto map CRYPTO")
	
	for c_map in crypto_maps: # for each list element in your output print it in text
		print
		print c_map.text
		for child in c_map.children: # For each child associated wiht a parent found in cmap, append the .children fucntion to grab the child data
			print child.text # print the parent and child data in readable text

	print

if __name__ == "__main__": # executes the function 'main' you created above
	main()

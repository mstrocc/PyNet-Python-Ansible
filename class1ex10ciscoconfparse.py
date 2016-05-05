#!/usr/bin/python

'''
using ciscoconfparse find the ctypto maps that are not using AES (based-on the transform set name). Print these entries and thier corresponding transform set name.
'''

import re
from ciscoconfparse import CiscoConfParse

def main():
	'''
	Using ciscoconfparse find the crypto maps that are not using AES (based-on th transform set name). Print these entries and thier correspinding transfo	  rm set name.
	'''
	cisco_file = ('cisco_ipsec.txt')
	cisco_cfg = CiscoConfParse(cisco_file)
	crypto_maps = cisco_cfg.find_objects_wo_child(parentspec=r'crypto map CRYPTO', childspec=r'AES')

	print  "\nCrypto Maps not using AES:"
	for entry in crypto_maps:
		for child in entry.children:
			if 'transform' in child.text:
				match = re.search(r"set transform-set (.*)$", child.text)
				encryption = match.group(1)
		print "  {0} >>> {1}".format(entry.text.strip(), encryption)
	print

if __name__ == "__main__":
	main()



#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List,Dict
import json
from data_provider import get_mc_data_versions,get_mc_data,get_spigot_enum_json,legacy_minecraft_data_conversion

# It will try to convert from one version's items to the next one.
#
# The return will relate the new item name to the old one (even if it's the same).
# If the key isn't found then the conversion for that item wasn't possible (maybe it didn't exist?).
def forward(old: json, new: json, legacy_conversion: Dict[str,str]) -> Dict[str,str]:
	conversion = {}
	for item in old:
		new_equivalence = None
		for search in new:
			if search['displayName'] == item['displayName']:
				new_equivalence = search['name']
				break

		if new_equivalence is None:
			# try re-using the same ID
			for search in new:
				if search['name'] == item['name']:
					new_equivalence = search['name']
					break
				
		if new_equivalence is None:
			# try with legacy conversion
			try:
				new_id = legacy_conversion[item['name']]
				for search in new:
					if search['name'] == new_id:
						new_equivalence = search['name']
						break
			except KeyError:
				pass
		
		if new_equivalence is None:
			print(f"[e] Couldn't find item {item['name']}")
		else:
			conversion[new_equivalence] = item['name']

	return conversion

def main():
	versions = get_mc_data_versions()
	versions.sort(key=lambda s: list(map(int, s.split('.'))))

	versions.remove('1.7') # old version
	versions.remove('1.15') # no item file
	versions.remove('1.16') # no item file
	print(versions)

	legacy_conversion = legacy_minecraft_data_conversion()
	for i in range(len(versions)-1):
		print(f"[v] Getting {versions[i]}...")
		old = get_mc_data(versions[i])
		new = get_mc_data(versions[i+1])

		conversion = forward(old, new, legacy_conversion)
		#print(conversion)

	#print(get_spigot_enum_json())

if __name__ == '__main__':
	main()
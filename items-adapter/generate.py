#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List,Dict,Tuple,Any
import json
from data_provider import get_mc_data_versions,get_mc_data,get_spigot_enum_json,get_spigot_enum,legacy_minecraft_data_conversion

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

# @param convertors list of convertors and its version, ordered from high to low.
# 		The first version (last element) must contain a None conversion
def generate_json_entry(material: str, convertors: List[Tuple[str,Dict[str,str]]]) -> Dict[str,Any]:
	material = material.lower()

	element = material
	aliases = [{'name': element, 'max-version': convertors[0][0]}]
	for i in range(len(convertors)):
		(version,conversion) = convertors[i]
		prior_version = (None if i == 0 else convertors[i-1][0])
		if conversion is None:
			aliases[-1]['min-version'] = prior_version # last append
			break

		try:
			if element != conversion[element]:
				element = conversion[element] # save the other element
				aliases.append({'name': element, 'max-version': version})
		except KeyError as e:
			if i == 0: raise e # not found in the first version
			aliases[-1]['min-version'] = prior_version
			break

	return {
		'name': material,
		'aliases': aliases
	}

def main():
	versions = get_mc_data_versions()
	versions.remove('1.7') # old version
	versions.remove('1.15') ; versions.append('1.15.2') # no item file
	versions.remove('1.16') ; versions.append('1.16.2') # no item file
	versions.sort(key=lambda s: list(map(int, s.split('.'))))
	print(versions)

	conversion_queue = [None] # the first version won't have a conversion queue
	legacy_conversion = legacy_minecraft_data_conversion()
	for i in range(len(versions)-1):
		print(f"[v] Getting {versions[i+1]} to {versions[i]}...")
		old = get_mc_data(versions[i])
		new = get_mc_data(versions[i+1])

		conversion = forward(old, new, legacy_conversion)
		conversion_queue.append(conversion)

	#conversion_queue.append( forward(get_mc_data(versions[-1]), get_spigot_enum_json(), legacy_conversion={}) ) # spigot to Mineflayer 1.20
	#versions.append('Spigot')

	convertors = list(reversed(list(zip(versions,conversion_queue))))
	for mat in get_spigot_enum():
		print(generate_json_entry(mat, convertors))

if __name__ == '__main__':
	main()
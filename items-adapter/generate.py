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
				if new_equivalence is not None:
					print(f"[w] Two equal names found while searching for {item['displayName']}; searching by id instead")
					new_equivalence = None
					break
				new_equivalence = search['name']

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
		if conversion is None:
			aliases[-1]['min-version'] = version # last append
			break
		next_version = convertors[i+1][0]

		try:
			if element != conversion[element]:
				element = conversion[element] # save the other element
				aliases[-1]['min-version'] = version
				aliases.append({'name': element, 'max-version': next_version})
		except KeyError as e:
			#if i == 0: raise e # not found in the first version
			aliases[-1]['min-version'] = version
			break

	return {
		'name': material,
		'aliases': aliases
	}

def get_material_list(latest_items: json) -> List[str]:
	r = []
	for latest_item in latest_items:
		r.append(latest_item['name'].upper())
	return r

def get_materials_list(versions: List[str], conversion_queue: List[Dict[str,str]]) -> List[Dict[str,Any]]:
	r = []
	convertors = list(reversed(list(zip(versions,conversion_queue))))
	for mat in get_material_list(get_mc_data(versions[-1])):
		r.append(generate_json_entry(mat, convertors))
	return r

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
		conversion['air'] = 'air' # add "no item"
		conversion_queue.append(conversion)
		
	# now we got the files; keep the "base" versions
	versions.remove('1.15.2') ; versions.append('1.15')
	versions.remove('1.16.2') ; versions.append('1.16')
	versions.sort(key=lambda s: list(map(int, s.split('.'))))

	with open("items.json", "w") as f:
		f.write( json.dumps(get_materials_list(versions, conversion_queue), indent=2) )

if __name__ == '__main__':
	main()
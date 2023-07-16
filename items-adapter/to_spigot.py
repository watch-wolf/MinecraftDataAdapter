#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List,Dict,Tuple,Any
import json
from data_provider import get_mc_data_versions,get_mc_data,get_spigot_enum_json
from generate import forward

def generate_conversion_list(conversion: Dict[str,str]) -> List[Dict[str,Any]]:
	r = []
	for (spigot_name,mcdata_name) in conversion.items():
		r.append({
			'spigot': spigot_name,
			'mc_data': mcdata_name
		})
	return r

def equal_conversion(conversion: Dict[str,str]) -> bool:
	for (new,old) in conversion.items():
		if new != old:
			return False
	return True

def main():
	versions = get_mc_data_versions()
	versions.sort(key=lambda s: list(map(int, s.split('.'))))
	latest_version = versions[-1]

	conversion = forward(get_mc_data(latest_version), get_spigot_enum_json(), {})

	print(f"[v] The Spigot names are { 'equal' if equal_conversion(conversion) else 'different' } to mc_data's")
	with open("mcdata_to_spigot.json", "w") as f:
		f.write( json.dumps(generate_conversion_list(conversion), indent=2) )

if __name__ == '__main__':
	main()
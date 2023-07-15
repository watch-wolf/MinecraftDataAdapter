#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List,Dict
import json
from distutils.version import StrictVersion
from data_provider import get_mc_data_versions,get_mc_data,get_spigot_enum,get_legacy_conversion

# It will try to convert from one version's items to the next one.
#
# The return will relate the new item name to the old one (even if it's the same).
# If the key isn't found then the conversion for that item wasn't possible (maybe it didn't exist?).
def forward(old: json, new: json, legacy_conversion: Dict[str,str]) -> Dict[str,str]:
	return None

def main():
	#versions = get_mc_data_versions()
	#versions.sort(key=StrictVersion)

	#print(get_mc_data('1.9'))
	#print(get_spigot_enum())
	print(get_legacy_conversion())

if __name__ == '__main__':
	main()
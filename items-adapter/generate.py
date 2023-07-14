#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List

# get minecraft-data JSON
from urllib.request import urlopen
import json

# get github folders
from bs4 import BeautifulSoup
import re

def get_mc_data_versions() -> List[str]:
	github_url = "https://github.com/PrismarineJS/minecraft-data/blob/master/data/pc/"

	result = urlopen(github_url)
	contents = result.read()
	#print(f"[v] {contents}")

	soup = BeautifulSoup(contents, 'html.parser')
	version_folders = soup.find_all(title=re.compile("^1\.\d+$")) # get all the firsts versions

	filename = []
	for i in version_folders:
			filename.append(i.extract().get_text())

	return filename

def get_mc_data(version: str) -> json:
	url = f"https://raw.githubusercontent.com/PrismarineJS/minecraft-data/master/data/pc/{version}/items.json"
	response = urlopen(url)
	return json.loads(response.read())

def main():
	print(get_mc_data_versions())

if __name__ == '__main__':
	main()
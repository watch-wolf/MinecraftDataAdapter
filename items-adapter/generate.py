#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List

# get minecraft-data JSON
from urllib.request import urlopen
from urllib.error import HTTPError,URLError
from socket import timeout as timedout
import json

# get github folders
from bs4 import BeautifulSoup
import re

def get_website_contents(url: str, timeout: int = 5) -> str:
	tries = 10
	while tries > 0:
		try:
			result = urlopen(url, timeout=timeout)
			return result.read().decode('utf-8')
		except HTTPError as error:
			print('[e] HTTP Error: Data of %s not retrieved because %s\nURL: %s', url, error, url)
			break
		except URLError as error:
			if isinstance(error.reason, timedout):
				tries -= 1
			else:
				print('[e] URL Error: Data of %s not retrieved because %s\nURL: %s', url, error, url)
				break

	return None # timedout <tries> times

def get_mc_data_versions() -> List[str]:
	github_url = "https://github.com/PrismarineJS/minecraft-data/blob/master/data/pc/"
	contents = get_website_contents(github_url)

	#soup = BeautifulSoup(contents, 'html.parser')
	#print(soup.prettify())

	#version_folders = soup.find_all(title=re.compile("^1\.\d+$")) # get all the firsts versions
	#return [i.extract().get_text() for i in version_folders]

	return re.findall(r'"name":"(1\.\d+)"', contents)

def get_mc_data(version: str) -> json:
	url = f"https://raw.githubusercontent.com/PrismarineJS/minecraft-data/master/data/pc/{version}/items.json"
	contents = get_website_contents(url)
	return json.loads(contents)

def get_watchwolf_enum() -> List[str]:
	url = "https://hub.spigotmc.org/javadocs/bukkit/org/bukkit/Material.html"
	contents = get_website_contents(url)

	soup = BeautifulSoup(contents, 'html.parser')
	enum_table = soup.find("div", {"class": "summary-table"}).findAll("div", {"class": "col-first"}, recursive=False)

	return list(filter(lambda e : not e.startswith('LEGACY_') and e != 'Enum Constant',
		    [ i.getText() for i in enum_table ]
		))

def main():
	#print(get_mc_data_versions())
	#print(get_mc_data('1.9'))
	print(get_watchwolf_enum())

if __name__ == '__main__':
	main()
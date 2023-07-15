#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import List,Dict,Tuple,Any

# get minecraft-data JSON
from urllib.request import urlopen
from urllib.error import HTTPError,URLError
from socket import timeout as timedout
import json
import math

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

def get_spigot_enum() -> List[str]:
	url = "https://hub.spigotmc.org/javadocs/bukkit/org/bukkit/Material.html"
	contents = get_website_contents(url)

	soup = BeautifulSoup(contents, 'html.parser')
	enum_table = soup.find("div", {"class": "summary-table"}).findAll("div", {"class": "col-first"}, recursive=False)

	return list(filter(lambda e : not e.startswith('LEGACY_') and e != 'Enum Constant',
		    [ i.getText() for i in enum_table ]
		))

class LegacyConversionEntry:
	def __init__(self, name: str, aliases: List[str], sub_id: int = None):
		self.name = name
		self.aliases = aliases
		self.sub_id = sub_id
	
	@property
	def default_sub_id(self) -> bool:
		return self.sub_id is None or self.sub_id == 0
	
	def __eq__(self, obj: Any) -> bool:
		if not isinstance(obj, LegacyConversionEntry):
			return False
		
		return obj.name == self.name and obj.aliases == self.aliases and (obj.sub_id == self.sub_id or (math.isnan(obj.sub_id) and math.isnan(self.sub_id)))

	def __str__(self):
		return f"{self.name} (known aliases: {self.aliases}{ '' if self.default_sub_id else ('; sub-id: '+str(self.sub_id)) })"
	
	def __repr__(self):
		return self.__str__()

	@staticmethod
	def read_element(text: str, offset: int = 0) -> Tuple[LegacyConversionEntry,int]:
		while text[offset].isspace(): offset += 1 # trim

		name = ""
		while offset < len(text) and text[offset] != '(' and text[offset] != ',':
			name += text[offset]
			offset += 1

		if offset == len(text) or text[offset] == ',':
			return ( LegacyConversionEntry(name,[]), offset+1 )
		
		while text[offset].isspace(): offset += 1 # trim
		offset += 1 # skip '('
		while text[offset].isspace(): offset += 1 # trim

		sub_id = None
		if text[offset] != '"':
			# there's a sub_id
			sub_id = 0
			while text[offset].isdigit():
				sub_id = sub_id*10 + int(text[offset])
				offset += 1

			while text[offset].isspace(): offset += 1 # trim
			if text[offset] != ',':
				# conditional sub_id
				sub_id = float('nan')

				# skip the rest
				num_parenthesis = 0
				while text[offset] != ',' or num_parenthesis > 0:
					if text[offset] == '(': num_parenthesis += 1
					elif text[offset] == ')': num_parenthesis -= 1
					offset += 1

			offset += 1 # skip ','
			while text[offset].isspace(): offset += 1 # trim

		# aliases
		aliases = []
		while text[offset] != ')':
			offset += 1 # skip '"'
			alias = ""
			while text[offset] != '"':
				alias += text[offset]
				offset += 1

			offset += 1 # skip '"'
			aliases.append(alias)
			
			while text[offset].isspace() or text[offset] == ',': offset += 1 # trim
			
		offset += 1 # skip ')'
		while offset < len(text) and text[offset].isspace(): offset += 1 # trim

		return ( LegacyConversionEntry(name,aliases,sub_id), offset )

# from an old material to the latest one
def get_legacy_conversion() -> Dict[str,str]:
	url = "https://raw.githubusercontent.com/CryptoMorin/XSeries/master/src/main/java/com/cryptomorin/xseries/XMaterial.java"
	contents = get_website_contents(url)
	contents = re.search(r'public enum XMaterial {\s*([^;]+)', contents).group(1)
	contents = re.sub(r'\s*\/\*[\s\S]*?\*\/\s*', '', contents)

	entries = []
	offset = 0
	while offset < len(contents):
		(e,offset) = LegacyConversionEntry.read_element(contents, offset=offset)

		# TODO add extra ones (e.g. "Wooden Planks"/"planks" is "OAK_PLANKS", with only known alias "wood")

		entries.append(e)
	#print(entries)

	conversion = {}
	for entry in entries:
		if not entry.default_sub_id: continue
		for alias in entry.aliases:
			conversion[alias] = entry.name

	return conversion
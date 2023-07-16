#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

def main():
	items_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "./items-adapter/items.json")
	out_class = 'ItemType'
	out_file = out_class + '.java'
	package = 'dev.watchwolf.entities.items'
    
	items = None
	with open(items_file) as f:
		items = json.load(f)
	
	with open(out_file, "w") as f:
		f.write(f"""
package {package};

/**
 * This file was auto-generated.
 * Please refer to <a href="https://github.com/watch-wolf/MinecraftDataAdapter">minecraft-data adapter project</a>.
 */
public enum ItemType {{
""")
		
		entries_str = ""
		for item in items:
			entries_str += '\t' + item["name"].upper() + '("' + item["aliases"][-1]["min-version"] + '"),\n'
		f.write(entries_str[:-2] + ';\n')

		f.write("""
	private final String minVersion;
	private ItemType(String minVersion) {
		this.minVersion = minVersion;
	}

	public String getMinVersion() {
		return this.minVersion;
	}
}
""")

if __name__ == '__main__':
	main()
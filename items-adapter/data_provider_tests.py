#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from data_provider import LegacyConversionEntry

class TestStringMethods(unittest.TestCase):
	def test_only_name(self):
		run = 'ACACIA_CHEST_BOAT'
		expect = LegacyConversionEntry("ACACIA_CHEST_BOAT", [])
	
		self.assertEqual(LegacyConversionEntry.read_element(run)[0], expect)

	def test_simple(self):
		run = 'ACACIA_BOAT("BOAT_ACACIA")'
		expect = LegacyConversionEntry("ACACIA_BOAT", ["BOAT_ACACIA"])
        
		self.assertEqual(LegacyConversionEntry.read_element(run)[0], expect)
	
	def test_skip(self):
		run = 'ACACIA_FENCE,ACACIA_FENCE_GATE'
		first_expect = LegacyConversionEntry("ACACIA_FENCE", [])
		second_expect = LegacyConversionEntry("ACACIA_FENCE_GATE", [])
        
		result = LegacyConversionEntry.read_element(run)
		self.assertEqual(result[0], first_expect)
		self.assertEqual(LegacyConversionEntry.read_element(run, offset=result[1])[0], second_expect)
    
	def test_complete(self):
		run = 'ACACIA_SAPLING(4, "SAPLING"),ACACIA_SIGN("SIGN_POST", "SIGN")'
		expect = LegacyConversionEntry("ACACIA_SAPLING", ["SAPLING"], sub_id=4)

		self.assertEqual(LegacyConversionEntry.read_element(run)[0], expect)
    
	def test_complex_subid(self):
		run = 'BLUE_BED((supports(12) ? 11 : 0), "BED_BLOCK", "BED")'
		expect = LegacyConversionEntry("BLUE_BED", ["BED_BLOCK","BED"], sub_id=float('nan'))

		result = LegacyConversionEntry.read_element(run)
		self.assertEqual(result[0], expect, f"Expected {expect}, but got {result[0]}")

if __name__ == '__main__':
	unittest.main()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import datetime

total_regexp = re.compile("TOTAL TTC ([0-9.]+) \\u20ac")
description_regexp = re.compile("(Serveur .+ 1 mois)", re.DOTALL)
periode_regexp = re.compile("Date : (.+)")

french_months = ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']

def parse_invoice(content):
	"""
	Extract data form server'invoice
	"""

	# print(re.search(description_regexp, content).group(0))
	bill = {}
	# GET DESIGNATION
	bill["designation"] = re.search(description_regexp, content).group(0)

	# GET PRICE
	bill["price"] = re.search(total_regexp, content).group(1)

	# GET PERIODE
	date_string = re.search(periode_regexp, content).group(1)

	for index, month in enumerate(french_months) :
	    if re.search(month, date_string):
	        date_string = re.sub(month, str(index), date_string)

	bill["periode"] = datetime.datetime.strptime(date_string, "%d %m %Y").date()
	# bill["periode"] = 123
	print(bill['periode'])
	return bill
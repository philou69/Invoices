#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import re
import sys
import os
import csv
from collections import OrderedDict

DEVNULL = open(os.devnull, 'wb')

total_regexp = re.compile("TOTAL TTC ([0-9.]+) \\u20ac")
description_regexp = re.compile("(Serveur .+ 1 mois)", re.DOTALL)

test_file = "data/"


def read_file(path):
    """
    Open the PDF file and return its textual content
    """

    return subprocess.check_output("pdftotext -raw \"%s\" -" % path,
    shell=True, stderr=DEVNULL).decode('utf-8')


def parse_invoices(invoices):
    """
    Read all invoices, parse them and crawl for relevant information
    """

    lines = []

    for invoice in invoices:
        content = read_file(invoice)
        print(content)

        # READ TOTAL
        lines.append({
            "total": re.search(total_regexp, content).group(1)
        })

        # READ DESCRIPTION
        lines.append({
        	"description": re.search(description_regexp, content).group(0)
        })

    return lines

def write_in_file(lines):
	"""
	Write data in csv
	"""
	print(lines[0]['total'])
	if re.search('Serveur', lines[1]["description"]) :
		global test_file
		test_file += "server.csv"

	print(test_file)

if __name__ == "__main__":
    invoices = sys.argv[1:]
    if len(invoices) == 0:
        raise Exception("No file specified")

    lines = parse_invoices(invoices)
    write_in_file(lines)
    print(lines)

    # print lines

    # with open('liste_factures.csv', 'wb') as csvfile:
    #     spamwriter = csv.writer(csvfile, delimiter=',',
    #                             quotechlar='"', quoting=csv.QUOTE_MINIMAL)
    #     spamwriter.writerow(lines[0].keys())
    #     for line in lines:
    #         spamwriter.writerow(line.values())
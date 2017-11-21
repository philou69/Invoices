#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import re
import sys
import os
import mysql.connector
import datetime

DEVNULL = open(os.devnull, 'wb')

total_regexp = re.compile("TOTAL TTC ([0-9.]+) \\u20ac")
description_regexp = re.compile("(Serveur .+ 1 mois)", re.DOTALL)
periode_regexp = re.compile("Date : (.+)")

french_months = ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']

path_tmp = "PDF/tmp/"
path_storage = "PDF/Invoices/"
def read_file(path):
    """
    Open the PDF file and return its textual content
    """

    return subprocess.check_output("pdftotext -raw \"%s%s\" -" % (path_tmp, path), shell=True, stderr=DEVNULL).decode('utf-8')

def move_pdf(file):
    """
    Move the pdf in the rigth folder
    """
    os.rename("%s%s" % (path_tmp, file), "%s%s" %(path_storage, file))

def parse_invoices(invoices):
    """
    Read all invoices, parse them and crawl for relevant information
    """

    lines = []

    for invoice in invoices:
        if not os.path.exists("%s%s" %(path_storage, invoice)):
            content = read_file(invoice)

            # READ DESCRIPTION
            lines.append(re.search(description_regexp, content).group(0))

            # READ TOTAL
            lines.append(re.search(total_regexp, content).group(1))

            # READ PERIODE
            date_string = re.search(periode_regexp, content).group(1)
            for index, month in enumerate(french_months) :
                if re.search(month, date_string):
                    date_string = re.sub(month, str(index), date_string)

            date = datetime.datetime.strptime(date_string, "%d %m %Y").date()
            
            lines.append(date)
            move_pdf(invoice)

            insert_in_database(lines)

    return lines

def insert_in_database(lines):
    """
    Write data in datbase
    """
    db = connect_mysql()
    cursor = db.cursor()

    add_invoice = ("INSERT INTO invoice"
        "(designation, price, periode)"
        "VALUES(%s, %s, %s)"
        )
    cursor.execute(add_invoice, lines)
    emp_no = cursor.lastrowid

    db.commit()
    cursor.close()
    db.close()


def connect_mysql():
    """
    Connection to database
    """
    db = mysql.connector.connect(user='root', password='Clophil090814@', host="127.0.0.1", database="Invoice")

    return db


if __name__ == "__main__":
    invoices = sys.argv[1:]
    if len(invoices) == 0:
        raise Exception("No file specified")

    lines = parse_invoices(invoices)

    if not lines:
        print("Les factures ont déjà été parser")
    else:
        insert_in_database(lines)

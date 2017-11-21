#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import re
import sys
import os
import mysql.connector
from Invoices import Serveur

DEVNULL = open(os.devnull, 'wb')



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
            print(content)
            if re.search("OVH", content):
                bill = Serveur.parse_invoice(content)
            
            if bill:
                lines.append(bill)
                move_pdf(invoice)

    return lines

def insert_in_database(lines):
    """
    Write data in datbase
    """
    db = connect_mysql()
    cursor = db.cursor()
    add_invoice = ("INSERT INTO invoice"
            "(designation, price, periode)"
            "VALUES (%(designation)s, %(price)s, %(periode)s)"
            )

    cursor.executemany(add_invoice, lines)
    
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

    if len(lines) == 0:
        print("Les factures ont déjà été parser")
    else:
        insert_in_database(lines)

        print("Facture(s) parser avec succès")
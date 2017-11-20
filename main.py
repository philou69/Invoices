#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

import PyPDF2

pdfReader = PyPDF2.PdfFileReader(open('PDF/facture.pdf', 'rb'))


pageObj = pdfReader.getPage(0)
page_content = pageObj.extractText()
print(page_content)
input('tape sur une touche piur fermer')
fileText = open("text.txt", "w")
# fileText.write(fileText.read())


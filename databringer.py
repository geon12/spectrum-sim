# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 16:58:00 2015

"""

#function that goes through xlsx to get data into python
#Based on Stackoverflow response from Colin Anderson: http://stackoverflow.com/questions/4371163/reading-xlsx-files-using-python
def xlsx(fname):
    import zipfile
    from xml.etree.ElementTree import iterparse
    zippy = zipfile.ZipFile(fname)
    try:
        words = [el.text for e, el in iterparse(zippy.open('xl/sharedStrings.xml')) if el.tag.endswith('}t')]
    except:
        words = {}
    rows = []
    row = {}
    val = ''
    for e, el in iterparse(zippy.open('xl/worksheets/sheet1.xml')):
        if el.tag.endswith('}v'): # <v>84</v>
            val = el.text
        if el.tag.endswith('}c'): # <c r="A3" t="s"><v>84</v></c>
            if el.attrib.get('t') == 's':
                val = words[int(val)]
            charac = el.attrib['r'] # AZ22
            while charac[-1].isdigit():
                charac = charac[:-1]
            row[charac] = val
            val = ''
        if el.tag.endswith('}row'):
            rows.append(row)
            row = {}
    return rows
    
#function loops through files to import Pure Component Data
def fileloop(directname):
    import os
    pureComponents = []
    for fn in os.listdir(directname):
        filename =  directname + "/" + fn
        pureComponents.append(xlsx(filename))
    
    return pureComponents

#create list of components from folder names
def filenamer(directname):
    import os
    pureComponentNames = []
    for fn in os.listdir(directname):
        filename = fn.replace(".xlsx", "")
        pureComponentNames.append(filename)
    
    return pureComponentNames

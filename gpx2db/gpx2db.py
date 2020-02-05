#!/python
# -*- coding: utf-8 -*-


"""
gps2db <db fichier.sqlite> <fichier.gpx>

connecter à la db
ouvrir le fichier GPX (lib )
pour chaque element 
    le stocker dans la DB
fermer la db
fermer le fichier
rendre compte
"""


# Diff Python2 vs python3
# https://python.doctor/page-syntaxe-differente-python2-python3-python-differences

# Pour que les print() fonctionnent
# en python2 (serveurs datastage) ET en python3 (poste de travail)
# print "\n".join([x, y])         -->   print(x, y, sep="\n")
# print >> sys.stderr, "erreur"   -->   print("Erreur", file=sys.stderr)
# print "une ligne ",             -->   print("une ligne", end="")
from __future__ import print_function
import os, sys
import sqlite3

def cleanNS(s) :
    if (s is None) :
        return ''
    return s[s.find('}') + 1:]

def forge_dWpt() :
    dWpt = dict()
    dWpt['lat'] = None
    dWpt['lon'] = None
    dWpt['name'] = None
    dWpt['time'] = None
    dWpt['type'] = "WPT"
    dWpt['sym'] = "TRIANGLE"
    return dWpt
    
tWptTag = ('name', 'time', 'type', 'sym')


##  Controler les 2 parametres de la ligne de commande
if (len(sys.argv) != 3) :
    print("usage : " + sys.argv[0] + " dirAdh <fichier.sqlite> <fichier.gpx>", file=sys.stderr)
    sys.exit()
else :
    if (os.path.isfile(sys.argv[1]) and os.path.isfile(sys.argv[2])) :
        print("Ok pour [" + sys.argv[1] + "] et [" + sys.argv[2] + "]")
        dbFilename = sys.argv[1]
        gpxFilename = sys.argv[2]
    else :
        print("ERR : Les fichiers indiques en parametres sont inacessibles !", file=sys.stderr)
        sys.exit()

##  Connexion a la base de donnee sqlite
try :
    dbCnx = sqlite3.connect(dbFilename)
    print("Connexion a la DB")
    dbCursor = dbCnx.cursor()
except Exception as e:
    print("Erreur de connexion a la DB", e, file=sys.stderr)
    sys.exit()
    # dbCnx.rollback()
    ### raise e
# finally:
    # conn.close()

try :
    ##  Version 1.4 
    ##  https://github.com/tkrajina/gpxpy
    import gpxpy
    print("import parser gpx")
except Exception as e:    
    print("Pb avec lib gpxpy", e, file=sys.stderr)
    sys.exit()

# fGpx = open(gpxFilename, 'r')
# for l in fGpx.readline().rstrip(\n\r) :


# fGpx = open(gpxFilename)
# gpx = gpxpy.parse(fGpx)
# fGpx.close()
# for waypoint in gpx.waypoints:
    # print('waypoint {0} -> ({1},{2})'.format( waypoint.name, waypoint.latitude, waypoint.longitude ))

    
# from xml.etree import ElementTree as ET
# tree = ET.parse(gpxFilename)
# for elem in tree.findall("{http://www.topografix.com/GPX/1/1}wpt"):
    # print(elem)

##  https://docs.python.org/3.4/library/xml.etree.elementtree.html    
##  https://docs.python.org/fr/2/library/xml.etree.elementtree.html
from lxml import etree
tree = etree.parse(gpxFilename)
NSMAP = {"gpx": "http://www.topografix.com/GPX/1/1", "opencpn": "http://www.opencpn.org"}
sqlInsertWpt = """INSERT INTO WPs
(lat, lon, name, ts, sym, type)
VALUES
(?, ?, ?, ?, ?, ?)
;
"""

for elem in tree.findall("gpx:wpt", namespaces=NSMAP):
    dWpt = forge_dWpt()
    tag = cleanNS(elem.tag)
    dWpt['lat'] = elem.attrib['lat']
    dWpt['lon'] = elem.attrib['lon']
    # print(elem.tag, elem.attrib, "[" + tag + "]")
    for i in elem :
        t = cleanNS(i.tag)
        if (i.text is not None and t in tWptTag) : 
            dWpt[t] = i.text
        # print(i.tag, i.attrib, i.text)
        # if (i.tag == "{http://www.topografix.com/GPX/1/1}extensions") :
            # for ext in i.findall("opencpn:*", namespaces=NSMAP) :
                # print(ext.tag, ext.attrib, ext.text)
    print(dWpt)   
    try :
        dbCursor.execute(sqlInsertWpt, (dWpt['lat'], dWpt['lon'], dWpt['name'], dWpt['time'], dWpt['sym'], dWpt['type']))
        print("id :", dbCursor.lastrowid)
        ## python dbCursor.lastrowid / SQL last_insert_rowid()
        ##  https://stackoverflow.com/questions/6242756/how-to-retrieve-inserted-id-after-inserting-row-in-sqlite-using-python
        dbCnx.commit()
    except sqlite3.Error as err :
        print("ERR: Pb insert", err)
# import xml.etree.ElementTree as ET
# tree = ET.parse(gpxFilename)
# root = tree.getroot()
# print(root.tag)
# for elem in root.findall("{http://www.topografix.com/GPX/1/1}wpt") :
    # print(elem.tag, elem.attrib)
    # lat = elem.find("{http://www.topografix.com/GPX/1/1}name").text
    # print(lat)
    
# fGpx.close()
dbCursor.close()
dbCnx.close()
        
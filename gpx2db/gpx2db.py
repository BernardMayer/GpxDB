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

fGpx = open(gpxFilename)
gpx = gpxpy.parse(fGpx)
fGpx.close()


for waypoint in gpx.waypoints:
    print('waypoint {0} -> ({1},{2})'.format( waypoint.name, waypoint.latitude, waypoint.longitude ))

# fGpx = open(gpxFilename, 'r')
# for l in fGpx.readline().rstrip(\n\r) :
    

# fGpx.close()
dbCnx.close()
        
#!/usr/bin/env python3

import os
import re
import json
import sys

def siteFileToList(siteFile):
    file = open(siteFile, 'r', encoding="utf8")
    lines = file.readlines()
    siteList = []
    for line in lines:
        site = line.strip()
        if site:  
            siteList.append(site)
    return siteList

directory = sys.argv[1]
nuevoMedioPago = sys.argv[2]
nuevoProtocolo = sys.argv[3]
listaSiteDirectory = sys.argv[4]

medioPagoLine = 'idsmediospago =>'
protocolLine = 'idsprotocolos =>'

siteline = ' =>' 
siteList = siteFileToList(listaSiteDirectory)
print("lista de sitios: " + str(siteList))

findSite = False
changeMP= False
for x in os.listdir(directory):
    if x.endswith(".conf"):
        file = open(directory + '/' + x, 'r', encoding="utf8")
        lines = file.readlines()
        lineCounter = 0
        for line in lines:
            #siteIsInLine = any(site in line for site in siteList)
            for site in siteList:
                siteL = '"' + site + '"' + siteline
                if siteL in line:
                    print("se encontro el sitio: " + site)
                    findSite = True
                    continue
                if medioPagoLine in line and findSite == True:
                    pagos = re.findall(r'\d+', line)
                    if nuevoMedioPago in pagos:
                        break
                    pagos.append(nuevoMedioPago)
                    pagosListToStr = "".join([elem for elem in json.dumps(pagos)])
                    lines[lineCounter] = '\t' * 2 + medioPagoLine + pagosListToStr + ',' + '\n'
                    changeMP = True
                    continue
                if protocolLine in line and changeMP == True:
                    protocolos = re.findall(r'\d+', line)
                    protocolos.append(nuevoProtocolo)
                    listToStr = ' '.join([str(elem) for elem in protocolos])
                    protocoloListToStr = "".join([elem for elem in json.dumps(protocolos)])
                    lines[lineCounter] = '\t' * 2 + protocolLine + protocoloListToStr + ',' + '\n'
                    changeMP = False
                    findSite = False
            lineCounter += 1
        newfile = open(directory + '/' + x, 'w', encoding="utf8")
        newfile.writelines(lines)




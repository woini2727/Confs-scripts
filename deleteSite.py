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


def lineReplacer(lineToReplace):
    newLine = lineToReplace.replace('"', '')
    newLine = newLine.replace('=>', '')
    newLine = newLine.replace('{', '')
    newLine = newLine.replace(' ', '')
    newLine = newLine.replace('\n', '')
    return newLine


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
changeMP = False
index = 0
for x in os.listdir(directory):
    changeFile = False
    if x.endswith(".conf"):
        file = open(directory + '/' + x, 'r', encoding="utf8")
        lines = file.readlines()
        lineCounter = -1
        for line in lines:
            lineCounter += 1
            siteNumber = lineReplacer(line)
            if siteNumber in siteList:
                findSite = True
                continue

            if medioPagoLine in line and findSite:
                pagos = re.findall(r'\d+', line)
                if nuevoMedioPago not in pagos:
                    findSite = False
                    continue
                index = pagos.index(nuevoMedioPago)
                pagos.remove(nuevoMedioPago)
                pagosListToStr = "".join([elem for elem in json.dumps(pagos)])
                lines[lineCounter] = '\t' * 2 + medioPagoLine + pagosListToStr + ',' + '\n'
                changeFile = True
                changeMP = True
                continue

            if protocolLine in line and changeMP:
                protocolos = re.findall(r'\d+', line)
                protocolos.pop(index)
                index = 0
                listToStr = ' '.join([str(elem) for elem in protocolos])
                protocoloListToStr = "".join([elem for elem in json.dumps(protocolos)])
                lines[lineCounter] = '\t' * 2 + protocolLine + protocoloListToStr + ',' + '\n'

        if changeFile:
            newfile = open(directory + '/' + x, 'w', encoding="utf8")
            newfile.writelines(lines)

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


hostftp2 = '10.225.0.129'
userftp2 = 'uswn0486_phe'
passftp2 = 'ZXcv2022'
sftp = '1'
directory = sys.argv[1]
listaSiteDirectory = sys.argv[2]


siteline = ' =>'
siteList = siteFileToList(listaSiteDirectory)
print("lista de sitios: " + str(siteList))
ftpFileLine = 'remotefileftp => '

for x in os.listdir(directory):
    changeFile = False
    if x.endswith(".conf"):
        file = open(directory + '/' + x, 'r', encoding="utf8")
        lines = file.readlines()
        lineCounter = -1
        fileFtpPath = ''
        for line in lines:
            lineCounter += 1
            siteNumber = lineReplacer(line)
            if siteNumber in siteList:
                findSite = True
                continue
            if line == ftpFileLine:
                fileFtpPath = ftpFileLine
            

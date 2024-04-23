import os
import re
import json
import sys

directory = sys.argv[1]
nuevoMedioPago = sys.argv[2]
nuevoProtocolo = sys.argv[3]
medioPagoLine = 'idsmediospago =>'
protocolLine = 'idsprotocolos =>'

for x in os.listdir(directory):
    if x.endswith(".conf"):
        file = open(directory + '/' + x, 'r', encoding="utf8")
        lines = file.readlines()
        lineCounter = 0
        for line in lines:
            if medioPagoLine in line:
                pagos = re.findall(r'\d+', line)
                if nuevoMedioPago in pagos:
                    break
                pagos.append(nuevoMedioPago)
                pagosListToStr = "".join([elem for elem in json.dumps(pagos)])
                lines[lineCounter] = '\t' * 2 + medioPagoLine + pagosListToStr + ',' + '\n'
            if protocolLine in line:
                protocolos = re.findall(r'\d+', line)
                listToStr = ' '.join([str(elem) for elem in protocolos])
                protocolos.append(nuevoProtocolo)
                protocoloListToStr = "".join([elem for elem in json.dumps(protocolos)])
                lines[lineCounter] = '\t' * 2 + medioPagoLine + protocoloListToStr + ',' + '\n'
            lineCounter += 1
        newfile = open(directory + '/' + x, 'w', encoding="utf8")
        newfile.writelines(lines)

#!/usr/local/bin/python3.8
# -*- coding: utf-8 -*-

import sys
import os
import GenerateGeneralHtmlFile

def startProgram():

    file = open(os.path.normpath(sys.argv[1]), 'r')
    list_servers = []
    try:
        for line in file:
            list_servers.append(line.replace('\n', ' '))
    finally:
        file.close()
    list_tmp = []
    for x in list_servers:
        list_tmp.append(x.split(':'))

    listAddresses = []
    for x in list_tmp:
        listAddresses.append(x[0])

    listPorts = []

    for x in list_tmp:
        listPorts.append(int(x[1]))

    user = sys.argv[2]
    password = sys.argv[3]
    outputFilePath = os.path.normpath(sys.argv[4])

    GenerateGeneralHtmlFile.generateHtmlTableHeader(listAddresses, user, password, listPorts, outputFilePath)

startProgram()



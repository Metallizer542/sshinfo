import sys

import HtmlFormatter


def startProgram():

    if sys.argv[1] == '-h' or sys.argv[1] == '--hosts':
        file = open(sys.argv[2], 'r')
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
    else:
        print('Не задан путь к фалу списка серверов')
        sys.exit(1)


    if sys.argv[3] == '-u' or sys.argv[3] == '--user':
        user = sys.argv[4]
    else:
       print('Не задан параметр имени пользователя')
       sys.exit(1)

    if sys.argv[5] == '-p' or sys.argv[5]== '--password':
        password = sys.argv[6]
    else:
        print('Не задан параметр пароля пользователя')
        sys.exit(1)

    if sys.argv[7] == '-o' or sys.argv[7] == '--output':
        outputFilePath = sys.argv[8]
    else:
        print('Не задан путь для файла вывода')
        sys.exit(1)

    HtmlFormatter.generateHtmlTableHeader(listAddresses, user, password, listPorts, outputFilePath)

startProgram()



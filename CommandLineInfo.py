import sys

#param_listServerPathName = sys.argv[1]
#param_listServerPathValue = sys.argv[2]
#param_userName = sys.argv[3]
#param_userValue = sys.argv[4]
#param_userPassword = sys.argv[5]
#param_userPasswordValue = sys.argv[6]
#param_fileOutputName = sys.argv[7]
#param_fileOutputValue = sys.argv[8]


def prepareServerList():
    #if param_listServerPathName == '-h' or param_listServerPathName == '--hosts':

        file = open('/Users/daniilkutyrev/Desktop/servers.txt', 'r')
        list_servers = []
        try:
            for line in file:
                list_servers.append(line.replace('\n', ' '))
        finally:
            file.close()
        list_ports = []
        for x in list_servers:
            list_ports.append(x.split(':'))
        return list_ports

def getServerAddress():
    listAddresse = []
    for x in prepareServerList():
        listAddresse.append(x[0])
    return listAddresse

def getServerPort():
    listPorts = []
    for x in prepareServerList():
        listPorts.append(int(x[1]))
    return listPorts



   # else:
    #    print('не задан путь к фалу списка серверов')
     #   sys.exit(1)


def getUserName():
    #if param_userName == '-u' or param_userName == '--user':
       # return param_userValue
        return 'intertrust'
    #else:
    #    print('не задан параметр имени пользователя')
    #   sys.exit(1)


def getUserPassword():
    #if param_userPassword == '-p' or param_userPassword == '--password':
       # return param_userPasswordValue
        return '39CgjVfkHtf<ea'
    #else:
    #    print('не задан параметр пароля пользователя')
    #    sys.exit(1)



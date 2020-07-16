from HtmlTables import HtmlTables
from GetServerInfo import GetServerInfo
import time


def generateHtmlTableHeader(hosts,user,password,ports,filepath):


    l = len(hosts)
    printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)

    file = open(filepath, 'w')
    file.write('<table border="1">')
    file.write('<thead>')
    file.write('<tr>')
    file.write('<th> Узел </th>')
    file.write('<th> Адрес </th>')
    file.write('<th> Учетные данные для подключения </th>')
    file.write('<th> Операционная система </th>')
    file.write('<th> CPU </th>')
    file.write('<th> RAM </th>')
    file.write('<th> Установленное ПО </th>')
    file.write('<th> HDD </th>')
    file.write('</tr>')
    file.write('</thead>')
    x = 0
    while(x<len(hosts)):
        client = GetServerInfo.getSShConnection(hosts[x], user, password, ports[x])
        print('идет подключение к серверу' + hosts[x]+':'+ports[x])
        time.sleep(0.1)
        generateHTMLTableBody(file, client, hosts[x], ports[x], user, password)
        printProgressBar(x + 1, l, prefix='Progress:', suffix='Complete', length=50)
        print('сбор информации с сервера ' + hosts[x] + ':' + ports[x] + 'завершен')
        x = x + 1
    file.write('</table')
    file.close()


def generateHTMLTableBody(file, client, host, port, user, password):
    baseProgram = HtmlTables.BaseProgrammInstalledHtml(client)
    hddInfo=HtmlTables.HDDInfoHtml(client)
    file.write('<tbody>')
    file.write('<tr>')
    file.write('<td>' + HtmlTables.ServerNameInfoHtml(client) + '</td>' + '\n')
    file.write('<td>' + HtmlTables.ServerAddresseInfoHtml(client) + '</br>' + 'SSH из сети Интертраст </br>' + host + ':' + str(port) + '</td>' + '\n')
    file.write('<td>' + 'SSH: User - ' + user + '</br>' + ' Password - ' + password + '</td>' + '\n')
    file.write('<td>' + HtmlTables.OsInfoHtml(client) + '</td>' + '\n')
    file.write('<td>' + HtmlTables.CPUinfoHtml(client) + '</td>' + '\n')
    file.write('<td>' + HtmlTables.MemoryInfoHtml(client) + '</td>' + '\n')
    for programm in baseProgram:
        file.write('<td>')
        file.write(programm)
        file.write('</td>')
    for hdd in hddInfo:
        file.write('<td>')
        file.write(hdd)
        file.write('</td>')
    file.write('</tr>')
    file.write('</tbody>')

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=printEnd)
    if iteration == total:
        print()






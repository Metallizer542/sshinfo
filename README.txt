Инструкция по использованию утилиты

1) Скачать и установить Python версии 3.8
2) Установит pip
3) через pip установить зависимости paramiko и tabulate
4) запуск скрипта осуществляется коммандой:

   /Users/daniilkutyrev/PycharmProjects/sshinfo/CmdStartProgram.py /Users/daniilkutyrev/Desktop/servers.txt user password /Users/daniilkutyrev/Desktop/test.html

   где:

    /Users/daniilkutyrev/PycharmProjects/sshinfo/CmdStartProgram.py - путь до файла скрипта CmdStartProgram.py
    /Users/daniilkutyrev/Desktop/servers.txt - путь до файлика со списком серверов для подключения
        Важно: в файле писать адреса в виде ip адрес хоста:порт (пример 169.254.10.37:3522)
               в файле не доолжно быть пустых строк
    user - юзернейм пользователя под которым выполняется вход на сервер (для windows параметр задается без кавычек)
    password - пароль пользователя (для windows параметр задается без кавычек)
    /Users/daniilkutyrev/Desktop/test.html - путь до файла вывода данных в формате html

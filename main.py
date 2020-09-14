import ftplib


def ftp_connect():
    while True:
        site_address = input('Please enter FTP address: ')
        username = input('Username: ')
        password = input('Password: ')
        try:
            with ftplib.FTP(site_address, username, password) as ftp:
                print('Current Directory', ftp.pwd())
                ftp.dir()
                print('Valid commands are cd/get/ls/exit (e.g. get README.txt)')
                ftp_command(ftp)
                break
        except ftplib.all_errors as e:
            print('Failed to connect ', e)


def ftp_command(ftp):
    while True:
        command = input('Enter a command: ')
        commands = command.split()

        if commands[0] == 'cd': # change directory
            try:
                ftp.cwd(commands[1])
                print('Current Directory', ftp.pwd())
                ftp.dir()
            except ftplib.error_perm as e: # not found, no permission
                error_code = str(e).split(None, 1)
                if error_code[0] == '550':
                    print(error_code[1], 'Directory may not exist or you do not have the correct permissions')

        elif commands[0] == 'get':
            try:
                ftp.retrbinary('RETR ' + commands[1], open('downloads/' + commands[1], 'wb').write)
                print('File successfully downloaded')
            except ftplib.error_perm as e: # not found, no permission
                error_code = str(e).split(None, 1)
                if error_code[0] == '550':
                    print(error_code[1], 'Directory may not exist or you do not have the correct permissions')

        elif commands[0] == 'post':
            try:
                file = open(commands[1], 'rb')
                ftp.storbinary('STOR ' + commands[1], file)
                print('File successfully uploaded')
            except ftplib.all_errors as e:
                print(e)

        elif commands[0] == 'ls':
            print('Current Directory', ftp.pwd())
            ftp.dir()

        elif commands[0] == 'exit':
            ftp.quit()
            print('Ending session!')
            break

        else:
            print('Invalid command, try again (valid options: cd/get/ls/exit')


if __name__ == "__main__":
    print('Welcome to Python FTP')
    ftp_connect()

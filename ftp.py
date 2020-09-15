import ftplib


class FTPClient:
    def __init__(self):
        self.ftp = None
        self.domain = ""
        self.username = ""
        self.password = ""
        self.ftp = None

    def set_fields(self, domain, username, password):
        self.domain = domain
        self.username = username
        self.password = password

    def connect(self):
        self.ftp = ftplib.FTP(self.domain, self.username, self.password)

    def ls(self):
        try:
            ls = []
            self.ftp.retrlines('MLSD', ls.append)

            important = []
            for entry in ls:
                entry = entry.split(";")
                to_add = f"{entry[0]}\t{entry[1]}\t{entry[len(entry) - 1]}"
                important.append(to_add)
            return "\n".join(important)
        except ftplib.error_perm as e:  # not found, no permission
            error_code = str(e).split(None, 1)
            if error_code[0] == '550':
                return error_code[1]

    def get(self, file_name, download_directory):
        try:
            self.ftp.retrbinary('RETR ' + file_name, open(download_directory + "/" + file_name, 'wb').write)
            return 'File successfully downloaded'
        except ftplib.error_perm as e:  # not found, no permission
            return "ERROR:" + e

    def post(self, files):
        try:
            for file in files:
                file_name = file
                if "/" in file_name:
                    file_name = file_name[file_name.rindex("/") + 1:]
                file = open(file, 'rb')
                self.ftp.storbinary('STOR ' + file_name, file)
            return 'Files successfully uploaded'
        except ftplib.all_errors as e:
            return e


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

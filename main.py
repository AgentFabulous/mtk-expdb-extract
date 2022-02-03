import os
import shutil


def sanitize_logs(logs):
    log_str = '\n'.join(logs)
    log_str = str.replace(log_str, '\x00', '\n')
    logs = log_str.split('\n')
    logs_out = []
    for line in logs:
        if len(line) > 5:
            logs_out.append(('    ' + line) if line[0].isascii() else line[2:] + '\n')
    del logs
    return logs_out


def main():
    f = open('expdb', 'r', encoding='ISO-8859-1')
    lines = f.readlines()
    dumps = []
    dump = {}
    reading_pllk = False
    reading_linux = False
    for line in lines:
        if "Preloader Start=" in line:
            reading_pllk = True
            reading_linux = False
            if dump != {}:
                dumps.append(dump)
            dump = {
                'pl_lk': [],
                'linux': [],
            }
        elif "[LK]jump to K64" in line:
            reading_pllk = False
            reading_linux = True
        if reading_pllk:
            dump['pl_lk'].append(line)
        if reading_linux:
            dump['linux'].append(line)
    shutil.rmtree('out')
    os.mkdir('out')
    for i in range(len(dumps)):
        ddir = 'out/' + str(i+1)
        os.mkdir(ddir)
        with open(ddir + '/pl_lk', 'w', encoding='ISO-8859-1') as f:
            f.writelines(dumps[i]['pl_lk'])
        with open(ddir + '/linux', 'w', encoding='ISO-8859-1') as f:
            f.writelines(sanitize_logs(dumps[i]['linux']))


if __name__ == '__main__':
    main()

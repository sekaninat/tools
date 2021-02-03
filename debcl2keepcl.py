import re
from datetime import datetime

def new_sec(ver, date, log):
    new_sec = '\n'
    new_sec += f'## [{ver}] - {datetime.strftime(date, "%Y-%m-%d")}\n'
    new_sec += '### Changed\n'
    new_sec += log
    return new_sec

if __name__ == '__main__':
    out = '# Changelog\n\n'
    out += '## [Unreleased]\n'
    version = None
    with open('debian/changelog') as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('szn-mobile-vectmap-server'):
                if version:
                    out += new_sec(version, date, log)                
                version = re.match(
                    r'szn-mobile-vectmap-server \((?P<ver>\d+\.\d+\.\d+(\-\d+)?)\).*',
                    line).groupdict()['ver']
                date = None
                log = ""
            elif line.startswith('--'):
                strDate = re.match(
                    r'-- .*<.*@.*>  .{3}, (?P<date>\d{1,2} .{3} \d{4}) .*',
                    line).groupdict()['date']
                if len(strDate) == 10:
                    strDate = '0' + strDate
                date = datetime.strptime(strDate, '%d %b %Y')
            else:
                if line:
                    if line[0] == '*':
                        line = '-' + line[1:]
                    if not re.match(r'^\[.*\]$', line):
                        log += line + '\n'
        out += new_sec(version, date, log)                
    print(out)
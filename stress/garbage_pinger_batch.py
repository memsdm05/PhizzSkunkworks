import subprocess
import sys

proc = []

url = sys.argv[1]
clients = int(sys.argv[2])

for i in range(clients):
    proc.append(subprocess.Popen(f'pypy3 garbage_pinger.py {url}'.split(' ')))

input()

for i in proc:
    i.kill()
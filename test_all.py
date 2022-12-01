import subprocess
import secrets
import time

number_of_tests=30

def get_ctf_cmd():
    index = secrets.randbelow(3)
    if index == 0:
        return 'python3 docker/cookies/cookies_solution.py'.split(' ')
    if index == 1:
        return 'python3 docker/mirror/mirror_solution.py'.split(' ')
    if index == 2:
        return 'nc 10.2.0.48 1233 < docker/connection_failed/solution'.split(' ')

def test_all():
    procs = []
    for index in range(number_of_tests):
        procs.append(subprocess.Popen(get_ctf_cmd()))
        time.sleep(0.1)

    for index in range(number_of_tests):
        procs[index].wait()
    
def test():
    proc = subprocess.Popen('nc 10.2.0.48 1233 < docker/connection_failed/solution'.split(' '))
    proc.wait()

if __name__ == '__main__':
    test_all()
import threading
import os
import random
from colorama import init, Fore
import requests
init(autoreset=True)
# print(os.cpu_count())

max_workers = os.cpu_count() -5
semaphore = threading.Semaphore(max_workers)

colors = [
Fore.RED, Fore.GREEN, Fore.YELLOW,
Fore.BLUE, Fore.MAGENTA, Fore.CYAN
]

def worker(host,task_number):
    with semaphore:
        Host = host if host.startswith('http') else 'http://' + host
        try:
            result=requests.get(Host, timeout=3).status_code
            print(random.choice(colors)+f" server stats result for({host}) task_num({task_number}):{result}")
        except requests.exceptions.RequestException:
            print(colors[0]+f'time out error for {host} task_num {task_number}')
if __name__ == "__main__":
    threads=[]
    host=[]
  
    while (h:= input('give host ip or domain name(type e for exit): ')).lower() != 'e':
        host.append(h)
    for i,Host in enumerate(host):
        t = threading.Thread(target=worker, args=(Host,i,))
        threads.append(t)
    for t in threads:
            t.start()
    for t in threads:t.join()
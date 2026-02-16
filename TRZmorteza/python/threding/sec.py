'''
    Has 50 fake tasks

    Uses max 4 workers

    Each task sleeps random 1–5 sec
'''
import threading
import time
import random
from colorama import init, Fore
colors=[Fore.RED,
        Fore.BLUE,
        Fore.YELLOW,
        Fore.GREEN]
task_count=50
max_worker=4
init(autoreset=True)
semaphore = threading.Semaphore(max_worker)
"""
chatgpt version with active thread count
def countdown(count):
    global active_count
    with semaphore:
        with active_lock:
            active_count += 1
            print(Fore.CYAN + f"Active threads: {active_count}")
        # work simulation
        time.sleep(random.randint(1,5))
        with active_lock:
            active_count -= 1
            print(Fore.CYAN + f"Thread finished. Active threads: {active_count}")
need values and set up
active_lock = threading.Lock()
active_count = 0


"""
def countdown(count):
    with semaphore:
        current_color = random.choice(colors)
        print(current_color+f'starting count down for task number {count}')
        for i in range(1,10):
            time.sleep(1)
            print(current_color+str(i),end=',')
        print(current_color+f'finished count down for task number {count}')
if __name__ == "__main__":
    threads=[]
    for i in range(task_count):
        t = threading.Thread(target=countdown, args=(i,))
        threads.append(t)
    for t in threads:
        t.start()
    print('all tasks started')
    for t in threads:
        t.join()
    print(Fore.PURPLE+'all tasks finished')
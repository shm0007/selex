import concurrent.futures
import time
def run_instance(i):
    print("Enter ",i)
    time.sleep(5)
    print("Exit" , i )
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(run_instance, range(50))
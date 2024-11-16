from concurrent.futures import ThreadPoolExecutor
import threading
import time


############################################
#
# Access without locking.
#
##########
class FakeDatabase:
    def __init__(self):
        self.value = 0

    def update(self, name):
        print(f"Thread {name}: starting update")

        local_copy = self.value
        local_copy += 1
        
        time.sleep(0.1)
        
        self.value = local_copy
        
        print(f"Thread {name}: finishing update")
############################################
############################################
#
# Access with locking.
#
##########
# class FakeDatabase:
#     def __init__(self):
#         self.value = 0
#         self._lock = threading.Lock()

#     def update(self, name):
#         print(f"Thread {name}: starting update")
#         print(f"Thread {name} about to lock")

#         with self._lock:
#             print(f"Thread {name} has lock")

#             local_copy = self.value
#             local_copy += 1
#             time.sleep(0.1)

#             self.value = local_copy

#             print(f"Thread {name} about to release lock")
            
#         print(f"Thread {name} after release")
#         print(f"Thread {name}: finishing update")
############################################


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"

    database = FakeDatabase()
    print(f"Testing update. Starting value is {database.value}")

    with ThreadPoolExecutor(max_workers=2) as executor:
        for index in range(2):
            executor.submit(database.update, index)
    print(f"Testing update. Ending value is {database.value}")

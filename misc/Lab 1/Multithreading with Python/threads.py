import threading 
import time


def thread_function(name, sleep_time):
    print(f"Thread {name}: starting.")
    time.sleep(sleep_time)
    print(f"Thread {name}: stopping.")


############################################
#
# Basic threads.
#
##########
if __name__ == "__main__":
    for index in range(3):
        t = threading.Thread(target=thread_function, args=(index, 2))
        t.start()
        print(f"Waiting for the thread {index} to finish.")
############################################
############################################
#
# Basic threads with join.
#
##########
# if __name__ == "__main__":
#     for index in range(3):
#         t = threading.Thread(target=thread_function, args=(index, 2))
#         t.start()
#         print(f"Waiting for the thread {index} to finish.")
#         t.join() # attention 
############################################
############################################
#
# Basic threads with join at different times.
#
##########
# if __name__ == "__main__":
#     t1 = threading.Thread(target=thread_function, args=("t1", 10))
#     t1.start()
    
#     t2 = threading.Thread(target=thread_function, args=("t2", 2))
#     t2.start()
#     print(f"Waiting for the thread t2 to finish.")
#     t2.join()

#     t3 = threading.Thread(target=thread_function, args=("t3", 2))
#     t3.start()
#     print(f"Waiting for the thread t3 to finish.")
#     t3.join()

#     print(f"Waiting for the thread t1 to finish.")
#     t1.join() # attention
############################################
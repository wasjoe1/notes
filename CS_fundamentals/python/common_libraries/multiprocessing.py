# multiprocessing

from multiprocessing import Process, Value, Array
# Process is used to spawn another process
# Value is used to create a shared value (shared mem via shm) between processes
# Array is used to create a shared array (shared mem via shm) between processes
def worker_function(value, array):
    value += 1
    array[0] = 'something'
value = 0
array = [0,1,2]
p = Process(target=worker_function, args=(value, array)) # python Process object created, OS process not yet created
p.start() # has to start the process via fork() ; OS child process created & running
p.join() # parent's process blocks (waits) until child process exits, child process resources r cleaned up (zombie process reaped)
        # if parent terminates first wihout calling join(wait), the child process becomes orphaned, then only later it will be a zombie for a brief moment before init auto calling wait() & child is reaped

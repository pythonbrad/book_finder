import _thread
import time

class Task:
    def __init__(self):
        #We init the tast list
        self.task_list = []
        #We init the state
        self.running = 0
    def is_free(self):
        return False if self.task_list else True
    def add(self, func):
        #We add a new task
        self.task_list.append(func)
    def run(self):
        #We update running at 1
        self.running = 1
        #We execute the tasks
        _thread.start_new(self.executor, ())
        print("Thread started")
    def stop(self):
        #We stop the tasks execution
        self.running = 0
        print("Thread stopped")
    def executor(self):
        #We verify the state
        while self.running:
            #We verify if a task exists
            if self.task_list:
                #We execute this task
                self.task_list[0]()
                #We remove this task
                self.task_list.pop(0)
            else:
                #If not task, we wait
                time.sleep(1)
            #We repeat the processus
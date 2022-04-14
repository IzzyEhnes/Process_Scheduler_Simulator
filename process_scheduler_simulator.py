from random import randrange
from math import ceil
from copy import deepcopy

TIME_QUANTUM_MAX = 5

# Parent class
class OS:
    def __init__(self, process_list):
        # wait time per process, turn around time per process, throughput
        self.process_list = process_list
        self.statistics = [[], [], 0.0]


    # Prints the process list with each process on a new line
    def print_process_list(self):
        for line in self.process_list:
            print(*line)


    # Computes the total time a process is in the ready queue
    def compute_wait_times(self):
        wait_time = 0
        for process in self.process_list:
            self.statistics[0].append(wait_time)
            wait_time += int(process[1])


    # Prints the wait time for each process
    def print_wait_time(self):
        self.compute_wait_times()
        process_num = 0
        for process in self.process_list:
            print(type(self).__name__ + " wait of p" + str(process[0]) + " = " + str(self.statistics[0][process_num]))
            process_num += 1


    # Computes and returns the average wait time for all of the processes
    def compute_avg_wait_time(self) -> float:
        avg_wait = sum(self.statistics[0]) / len(self.statistics[0])
        return round(avg_wait, 6)

    
    # Prints the average wait time for all of the processes
    def print_avg_wait_time(self):
        print("average wait time for " + str(len(self.process_list)) + " processes = " + str(self.compute_avg_wait_time()))


    # Computes the span of time from the moment of submission to completion time for each process
    def compute_turn_around_time(self):
        turn_around_time = 0
        for process in self.process_list:
            turn_around_time += int(process[1])
            self.statistics[1].append(turn_around_time)


    # Prints the turn around time for each process
    def print_turn_around_times(self):
        self.compute_turn_around_time()
        process_num = 0
        for process in self.process_list:
            print(type(self).__name__ + " turn-around time for p" + str(process[0]) + " = " + str(self.statistics[1][process_num]))
            process_num += 1

    
    # Computes and returns the average turn around time for all of the processes
    def compute_avg_turn_around_times(self) -> float:
        avg_wait = sum(self.statistics[1]) / len(self.statistics[1])
        return round(avg_wait, 6)


    # Prints the average turn around time for all of the processes
    def print_avg_turn_around_time(self):
        print("average turn-around time for " + str(len(self.process_list)) + " processes = " + str(self.compute_avg_turn_around_times()))

    
    # Computes and returns the number of processes completed per time unit (ms)
    def compute_throughput(self) -> float:
        num_processes = len(self.process_list)
        self.statistics[2] = round(num_processes / self.statistics[1][num_processes - 1], 6)

    
    # Prints the throughput for all of the processes
    def print_throughput(self):
        self.compute_throughput()
        print(type(self).__name__ + " throughput for " + str(len(self.process_list)) + " processes = " + str(self.statistics[2]) + " process/ms")



# First Come First Serve class; child of OS class
class FCFS(OS):
    def __init__(self, process_list):
        super().__init__(process_list)
        self.process_list = process_list
        self.statistics = [[], [], 0.0]



# High Priority First class; child of OS class
class HPF(OS):
    def __init__(self, process_list):  
        super().__init__(process_list)
        self.process_list = process_list
        self.statistics = [[], [], 0.0]


    # Sorts the processes in order of priority
    def sort_list(self):
        temp_list = list(self.process_list)
        temp_list.sort(key=lambda priority: priority[2])
        self.process_list = tuple(temp_list)



# Round Robin class; child of OS class
class RR(OS):
    def __init__(self, process_list):
        super().__init__(process_list)
        self.process_list = process_list
        self.statistics = [[], [], 0.0]


    # Find and return the ID of the process that will take the least amount of time
    def find_quickest_process_id(self, ready_queue):
        return min(ready_queue, key=lambda x: x[1])[0]


    # Checks whether or not the process that is initially found to take the least amount of time 
    # has a remaining time that is greater than the quantum
    def quickest_process_greater_than_quantum(self, ready_queue, quickest_process_id, quantum) -> bool:
        for process in ready_queue:
            if process[0] == quickest_process_id:
                return process[1] > quantum

    
    # Runs the preemptive RR schedule
    def complete_RR_schedule(self):

        quantum_max = randrange(2, TIME_QUANTUM_MAX + 1)  #  max number of ms a process is able to execute

        for quantum in range(1, quantum_max + 1):
            for overhead in range(0, quantum + 1):  # overhead is cost (in ms) to switch to a different process
                time = 0
                ready_queue = deepcopy(list(self.process_list))  # queue of processes that have not yet completed
                turn_around_time = [0] * len(self.process_list)  # a list to store the span of time each process takes to complete

                while len(ready_queue) != 0:
                    quickest_process_id = self.find_quickest_process_id(ready_queue)

                    # for each process that hasn't yet completed, allow it to execute for quantum ms;
                    # repeat for as many rounds as it takes until the process that is initially found to take the 
                    # least amount of time has a remaining time that is <= the quantum
                    while self.quickest_process_greater_than_quantum(ready_queue, quickest_process_id, quantum):
                        for process_num in range(0, len(ready_queue)):
                            temp_process = deepcopy(ready_queue[0])
                            ready_queue.pop(0)
                            temp_process[1] -= quantum
                            ready_queue.append(temp_process)

                            time += (quantum + overhead)

                    # loop through processes (but not completing a full round), allowing them to execute for quantum ms
                    # until the process that is initially found to take the least amount of time is at the front of the queue
                    while quickest_process_id != ready_queue[0][0]:
                        # if the process at the front of the queue will complete before the process that is initially found 
                        # to take the least amount of time, let it complete and remove it from the ready queue
                        if (ready_queue[0][1] - quantum <= 0):
                            time += ready_queue[0][1]

                            turn_around_time[ready_queue[0][0] - 1] = time
                            ready_queue.pop(0)
                            
                            time += overhead
                            
                        # allow the process at the front of the queue to execute for quantum ms and move it to end of ready queue
                        else:
                            temp_process = deepcopy(ready_queue[0])
                            ready_queue.pop(0)
                            temp_process[1] -= quantum
                            ready_queue.append(temp_process)

                            time += (quantum + overhead)
                    
                    # let the process that is initially found to take the least amount of time complete and remove it from queue 
                    time += ready_queue[0][1]
                    turn_around_time[ready_queue[0][0] - 1] = time
                    ready_queue.pop(0)
                    time += overhead

                self.print_RR_schedule(quantum, overhead, turn_around_time)


    # Prints the RR schedule's current quantum, overhead, and the turn around times, throughput, and average turn around time for the processes
    def print_RR_schedule(self, quantum, overhead, turn_around_time):

        print("preemptive RR schedule, quantum = ", quantum, " overhead = ", overhead)

        process_list_with_TA = deepcopy(self.process_list)

        # add turn around time to associated process
        for process_id in range(0, len(process_list_with_TA)):
            process_list_with_TA[process_id].append(turn_around_time[process_id])

        process_list_with_TA.sort(key=lambda ta_time: ta_time[3])  # sort list by turn around time

        for process in range(0, len(turn_around_time)):
            print("RR TA time for finished p" + str(process_list_with_TA[process][0]) + " = " + str(process_list_with_TA[process][3]) + 
                    ", needed: " + str(process_list_with_TA[process][1]) + " ms, and: " + 
                    str(ceil(process_list_with_TA[process][1] / quantum)) + " time slices.")

        throughput_ms = round((len(turn_around_time) / max(turn_around_time)), 7)
        throughput_us = round((throughput_ms * 1000), 4)
        print("RR Throughput, " + str(len(turn_around_time)) + " processes, with q: " + str(quantum) + ", o: " + str(overhead) + 
                ", is: " + str(throughput_ms) + " p/ms, or " + str(throughput_us) + " p/us")
        
        average_ta = round((sum(turn_around_time) / len(turn_around_time)), 4)
        print("Average RR TA, " + str(len(turn_around_time)) + " processes, with q: " + str(quantum) + ", o: " + str(overhead) + 
                ", is: " + str(average_ta))

        print()
            


# Returns the processes input by the user (in the form of process id, time (in ms), and priority)
def get_user_input() -> list:
    print("Enter triples: process id, time in ms, and priority (Ctrl-D to end input):")
    print("For example: \n1 12 0\n3  9 1\n2 99 9")
    print("process 1 needs 12 ms and has priority 0, very high,")
    print("process 3 needs  9 ms and has priority 1.")
    print("and so on ...")

    content = []
    while True:
        try:
            line = input()
            line = " ".join(line.split()).split()
        except EOFError:
            break
        line = list(map(int, line))
        content.append(line)

    return list(content)



# Runs the simulation for a FCFS OS, HPF OS, and RR OS, after getting user inputted processes
def run_simulation():
    process_list = get_user_input()
    print()

    # Simulate FCFS OS
    fcfs = FCFS(process_list)
    print("Process list in FCFS order as entered:")
    fcfs.print_process_list()
    print("End of list.\n")
    fcfs.print_wait_time()
    fcfs.print_avg_wait_time()
    fcfs.print_turn_around_times()
    fcfs.print_avg_turn_around_time()
    fcfs.print_throughput()
    print("<><> end FCFS schedule <><>\n")

    # Simulate HPF OS
    hpf = HPF(process_list)
    print("Process list in HPF order:")
    hpf.sort_list()
    hpf.print_process_list()
    print("End of list.\n")
    hpf.print_wait_time()
    hpf.print_avg_wait_time()
    hpf.print_turn_around_times()
    hpf.print_avg_turn_around_time()
    hpf.print_throughput()
    print("<><> end HPF schedule <><>\n")

    # Simulate RR OS
    rr = RR(process_list)
    print("Process list for RR in order entered:")
    rr.print_process_list()
    print("End of list.\n")
    rr.complete_RR_schedule()
    print("<><> end preemptive RR schedule <><>")



run_simulation()

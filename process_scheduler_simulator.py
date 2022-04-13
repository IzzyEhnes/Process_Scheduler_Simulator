import sys

# Parent class
class OS:
    # wait time per process, turn around time per process, throughput
    statistics = [[], [], 0.0]

    def get_user_input():
        print("Enter triples: process id, time in ms, and priority (Ctrl-D to end input):")
        print("For example: \n1 12 0\n3  9 1\n2 99 9")
        print("process 1 needs 12 ms and has priority 0, very high,")
        print("process 3 needs  9 ms and has priority 1.")
        print("and so on ...")

        content = sys.stdin.read()
        content = " ".join(content.split()).split()

        triples = list()
        while content:
            triples.append(content[:3])
            content = content[3:]

        OS.process_list = triples


    def print_process_list():
        for line in OS.process_list:
            print(' '.join(line))


    def compute_wait_times():
        wait_time = 0
        for process in OS.process_list:
            OS.statistics[0].append(wait_time)
            wait_time += int(process[1])


    def print_wait_time(self):
        self.compute_wait_times()
        process_num = 0
        for process in self.process_list:
            print(self.__name__ + " wait of p" + str(process_num + 1) + " = " + str(self.statistics[0][process_num]))
            process_num += 1


    def compute_avg_wait_time() -> float:
        avg_wait = sum(OS.statistics[0]) / len(OS.statistics[0])
        return round(avg_wait, 6)

    
    def print_avg_wait_time(self):
        print("average wait for " + str(len(self.process_list)) + " processes = " + str(self.compute_avg_wait_time()))


    def compute_turn_around_time():
        turn_around_time = 0
        for process in OS.process_list:
            turn_around_time += int(process[1])
            OS.statistics[1].append(turn_around_time)


    def print_turn_around_times(self):
        self.compute_turn_around_time()
        process_num = 0
        for process in self.process_list:
            print(self.__name__ + " turn-around time for p" + str(process_num + 1) + " = " + str(self.statistics[1][process_num]))
            process_num += 1

    
    def compute_avg_turn_around_times() -> float:
        avg_wait = sum(OS.statistics[1]) / len(OS.statistics[1])
        return round(avg_wait, 6)


    def print_avg_turn_around_time(self):
        print("average turn-around time for " + str(len(self.process_list)) + " processes = " + str(self.compute_avg_turn_around_times()))

    
    def compute_throughput(self) -> float:
        num_processes = len(self.process_list)
        self.statistics[2] = round(num_processes / self.statistics[1][num_processes - 1], 6)

    
    def print_throughput(self):
        self.compute_throughput(self)
        print(self.__name__ + " throughput for " + str(len(self.process_list)) + " processes = " + str(self.statistics[2]) + " process/ms")



# First Come First Serve class; child of OS class
class FCFS(OS):
    pass



# High Priority First class; child of OS class
class HPF(OS):
    def sort_list():
        HPF.process_list.sort(key=lambda priority: priority[2])



# Round Robin class; child of OS class
class RR(OS):
    pass



def run_simulation():
    OS.get_user_input()
    print()

    # Simulate FCFS OS
    print("Process list in FCFS order as entered:")
    FCFS.print_process_list()
    print("End of list.\n")
    FCFS.print_wait_time(FCFS)
    FCFS.print_avg_wait_time(FCFS)
    FCFS.print_turn_around_times(FCFS)
    FCFS.print_avg_turn_around_time(FCFS)
    FCFS.print_throughput(FCFS)
    print("<><> end FCFS <><>\n")

    # Simulate HPF OS
    print("Process list in HPF order:")
    HPF.sort_list()
    HPF.print_process_list()
    print("End of list.\n")



run_simulation()
TIME_QUANTUM_MAX = 5

# Parent class
class OS:
    
    def __init__(self, process_list):
        # wait time per process, turn around time per process, throughput
        self.process_list = process_list
        self.statistics = [[], [], 0.0]

    def print_process_list(self):
        for line in self.process_list:
            print(*line)


    def compute_wait_times(self):
        wait_time = 0
        for process in self.process_list:
            self.statistics[0].append(wait_time)
            wait_time += int(process[1])


    def print_wait_time(self):
        self.compute_wait_times()
        process_num = 0
        for process in self.process_list:
            print(type(self).__name__ + " wait of p" + str(process[0]) + " = " + str(self.statistics[0][process_num]))
            process_num += 1


    def compute_avg_wait_time(self) -> float:
        avg_wait = sum(self.statistics[0]) / len(self.statistics[0])
        return round(avg_wait, 6)

    
    def print_avg_wait_time(self):
        print("average wait for " + str(len(self.process_list)) + " processes = " + str(self.compute_avg_wait_time()))


    def compute_turn_around_time(self):
        turn_around_time = 0
        for process in self.process_list:
            turn_around_time += int(process[1])
            self.statistics[1].append(turn_around_time)


    def print_turn_around_times(self):
        self.compute_turn_around_time()
        process_num = 0
        for process in self.process_list:
            print(type(self).__name__ + " turn-around time for p" + str(process[0]) + " = " + str(self.statistics[1][process_num]))
            process_num += 1

    
    def compute_avg_turn_around_times(self) -> float:
        avg_wait = sum(self.statistics[1]) / len(self.statistics[1])
        return round(avg_wait, 6)


    def print_avg_turn_around_time(self):
        print("average turn-around time for " + str(len(self.process_list)) + " processes = " + str(self.compute_avg_turn_around_times()))

    
    def compute_throughput(self) -> float:
        num_processes = len(self.process_list)
        self.statistics[2] = round(num_processes / self.statistics[1][num_processes - 1], 6)

    
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

    print(content)

    return tuple(content)


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
    print("<><> end FCFS <><>\n")

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
    print("<><> end HPF <><>\n")

    # Simulate RR OS
    rr = RR(process_list)
    print("Process list for RR in order entered:")
    rr.print_process_list()
    print("End of list.\n")

run_simulation()
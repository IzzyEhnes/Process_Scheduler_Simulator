import sys

# Parent class
class OS:
    def print_process_list():
        for line in OS.process_list:
            print(' '.join(line))



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



get_user_input()
print()
HPF.sort_list()
HPF.print_process_list()
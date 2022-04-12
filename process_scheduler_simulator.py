import sys

# First Come First Serve OS class
class FCFS:
    pass



# High Priority First OS class
class HPF:
    pass



# Round Robin OS class
class RR:
    pass



def get_user_input():
    print("Enter triples: process id, time in ms, and priority (Ctrl-D to end input):")
    print("For example: \n1 12 0\n3  9 1\n2 99 9")
    print("process 1 needs 12 ms and has priority 0, very high,")
    print("process 3 needs  9 ms and has priority 1.")
    print("and so on ...")

    content = sys.stdin.read()
    content = " ".join(content.split()).split()
    print(content)

    triples = list()
    while content:
        triples.append(content[:3])
        content = content[3:]

    print(triples)

get_user_input()
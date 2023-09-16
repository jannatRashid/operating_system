class Process:
    def __init__(self, process_id, arrival_time, execution_time):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.execution_time = execution_time
        self.remaining_time = execution_time
        self.start_time = 0
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.utilization = 0

def srtf_scheduling(processes):
    current_time = 0
    execution_order = []
    remaining_processes = processes.copy()
    active_process = None

    while remaining_processes:
        # Find the process with the shortest remaining time
        shortest_remaining_time = float('inf')
        for process in remaining_processes:
            if process.arrival_time <= current_time and process.remaining_time < shortest_remaining_time:
                shortest_remaining_time = process.remaining_time
                active_process = process

        if active_process:
            # Record execution order
            execution_order.append(active_process.process_id)

            # Update start time
            if active_process.start_time == 0:
                active_process.start_time = current_time

            # Decrement remaining time
            active_process.remaining_time -= 1

            # Check if the process is completed
            if active_process.remaining_time == 0:
                active_process.completion_time = current_time + 1
                active_process.turnaround_time = active_process.completion_time - active_process.arrival_time
                active_process.waiting_time = active_process.turnaround_time - active_process.execution_time
                active_process.utilization = (active_process.execution_time / active_process.turnaround_time) * 100
                remaining_processes.remove(active_process)

            current_time += 1
        else:
            current_time += 1

    return execution_order

def print_gantt_chart(execution_order):
    gantt_chart = []
    current_time = 0

    for process_id in execution_order:
        while current_time < len(gantt_chart):
            if gantt_chart[current_time] == "":
                break
            current_time += 1
        gantt_chart.extend([f"P{process_id}"] * (current_time + 1 - len(gantt_chart)))

    print("\nGantt Chart:")
    print("|", end="")
    for time_slot in gantt_chart:
        print(time_slot.center(3), end="|")
    print()

if __name__ == "__main__":
    num_processes = int(input("Enter the number of processes (3 to 5): "))
    
    if num_processes < 3 or num_processes > 5:
        print("Number of processes must be between 3 and 5.")
        exit()

    processes = []
    for i in range(num_processes):
        arrival_time = int(input(f"Enter arrival time for Process {i + 1}: "))
        execution_time = int(input(f"Enter execution time for Process {i + 1} (<= 10): "))
        
        if execution_time > 10:
            print("Execution time must be <= 10.")
            exit()

        processes.append(Process(i + 1, arrival_time, execution_time))

    execution_order = srtf_scheduling(processes)
    print_gantt_chart(execution_order)

    print("\nProcess\tTurnaround Time\tWaiting Time\tUtilization")
    for process in processes:
        print(f"P{process.process_id}\t{process.turnaround_time}\t\t{process.waiting_time}\t\t{process.utilization:.2f}%")

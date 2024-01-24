import os
import copy

# Initialize Jobs through User Inputs
jobs = {}
print("Enter job details (format: job_name arrival_time burst_time priority), type 'confirm' when done")
job_input = input("Enter first job / type 'confirm' to finish: ")

# Sample data if no inputs are given
sample_jobs = {
    'A': [0, 3, 3],
    'B': [2, 4, 2],
    'C': [5, 1, 1]
}

# Splits the input
while job_input.lower() != 'confirm':
    job_details = job_input.split()
    jobs[job_details[0]] = [int(job_details[1]), int(job_details[2]), int(job_details[3])]
    job_input = input("Enter next job or type 'confirm' to finish: ")

# If no jobs were added, insert sample data
if not jobs:
    jobs = sample_jobs

# initializations
inputtedJobs = f'JOBS: {jobs}'
copyJobs = copy.deepcopy(jobs)
remainingJobs = copy.deepcopy(jobs)
currTime = 0
queue = {}
ongoing = {}
completed = {}
tat = 0
wT = 0

eta = 0
for item in sample_jobs.values():
    eta += item[1]

# Insert your logic here
while True:
    
    for job, details in jobs.items():
        if details[0] == currTime:
            queue[job] = details

    #Sorting the queue list according to this respectively: Priority>Bursttime>Name
    queue = dict(sorted(queue.items(), key=lambda x: x[1][2]))

    #if ongoing is empty and queue isn't, transfer first item in queue to ongoing
    if not ongoing and queue:
        item = min(queue, key=lambda x: queue[x][2])
        ongoing = {item: queue[item]}
        del queue[item]
        
    #if queue got new job, ongoing job will be pulled back to queue
    elif ongoing and queue:
        for job, details in ongoing.items():
            queue[job] = details
        ongoing = {}
        item = min(queue, key=lambda x: queue[x][2])
        ongoing = {item: queue[item]}
        del queue[item]
        
    queue = dict(sorted(queue.items(), key=lambda x: x[1][2]))
    
    #Ongoing decrements its burstime as it passes through time
    if ongoing:
        ongoing_job = list(ongoing.keys())[0]
        ongoing[ongoing_job][1] -= 1
        #if ongoing job reaches 0,  it will be sent to completed list
        if ongoing[ongoing_job][1] == 0:
            tat = currTime - copyJobs[ongoing_job[0]][0] + 1
            wT = tat - copyJobs[ongoing_job[0]][1]
            completed[ongoing_job] = copyJobs[ongoing_job] + [tat, wT]
            del remainingJobs[ongoing_job]
            del ongoing[ongoing_job]
    
    
    sortedCompleted = dict(sorted(completed.items()))
    #Print Logs
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
        Current Time: {currTime}
        Proccesor: {ongoing}
        Queue: {queue}
        Completed: {sortedCompleted}
        """)
    #Tabulate
    print("{:<2} {:<2} {:<2} {:<2} {:<2} {:<2}".format("JOB", "AT", "BT", "P", "TAT", "WT"))
    for job, values in sortedCompleted.items():
        print("{:<3} {:<2} {:<2} {:<2} {:<3} {:<2}".format(job, values[0], values[1], values[2], values[3], values[4]))
    
    
    
    #increment to increase time
    currTime += 1
    
    #if no more jobs and met the expected eta
    if currTime == eta + 1:
        break

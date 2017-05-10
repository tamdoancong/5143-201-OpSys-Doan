#!/usr/bin/python3 
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/components')
import random
import time

from sim_components import *


"""
This is a starter pack for a cpu scheduling project. The code / classes provided are to give you a
head start in creating the scheduling simulation. Obviously this is a simulation, so the majority
of the concepts are "simulated". For example, process "burst times" and "IO times" are known
a-priori (not so in real world). Things like memory are abstracted from addressable locations and
page tables to total "blocks" needed.
"""


###################################################################################################

# === Class: MLFQ===

class MLFQ(object):
    """Multi-Level Feedback Queue

    - Some general requirements for a MLFQ:
        - Each queue needs its own scheduling algorithm (typically Fcfs).
        - The method used to determine when to upgrade a process to a higher-priority queue.
        - The method used to determine when to demote a process to a lower-priority queue.
        - The method used to determine which queue a process will enter when that process needs
        service.

    - Rule 1: If Priority(A) > Priority(B), A runs (B doesn't).
    - Rule 2: If Priority(A) = Priority(B), A & B run in RR.
    - Rule 3: When a job enters the system, it is placed at the highest priority (the topmost
              queue).
    - Rule 4: Once a job uses up its time allotment at a given level (regardless of how many times
              it has given up the CPU), its priority is reduced (i.e., it moves down one queue).
    - Rule 5: After some time period S, move all the jobs in the system to the topmost queue.

    - **Attributes**:
        - self.num_levels
        - self.queues
    """
    def __init__(self, num_levels=2):
        self.num_levels = num_levels
        self.queues = []

        for i in range(self.num_levels):
            self.queues.append(Fifo())

    def new(self,proc):
        """This method admits a new process into the system.

        - **Args:**
            - None
        - **Returns:**
            - None
        """
        self.queues[0].add(proc)
        #pass

    def __str__(self):
        """Visual dump of class state.

        - **Args:**
            - None
        - **Returns:**
            - None
        """
        return my_str(self)

###################################################################################################

# === Class: Scheduler===

class Scheduler(object):
    """
    New:        In this status, the Process is just made or created.
    Running:    In the Running status, the Process is being executed.
    Waiting:    The process waits for an event to happen for example an input from the keyboard.
    Ready:      In this status the Process is waiting for execution in the CPU.
    Terminated: In this status the Process has finished its job and is ended.
    """
    def __init__(self, *args, **kwargs):
        self.clock = Clock()
        self.memory = Memory()                  
        self.cpu = Cpu()
        self.accounting = SystemAccounting()
        self.semPool = SemaphorePool(num_sems=5, count=1)
        self.job_scheduling_queue = Fifo()
        self.ready_queue = MLFQ()
        self.IO_waiting_queue = Fifo()
        self.finished_jobs = Fifo()



    def new_process(self,job_info):
        """New process entering system gets placed on the 'job_scheduling_queue'.
        - **Args**:
            - job_info (dict): Contains new job information.
        - **Returns**:
            - None
        """
        print( "Event: A   Time: " + str(self.clock.current_time()) )
        tempProc = Process(**job_info)
        if(tempProc.mem_required <= self.memory.mem_size) :
            self.job_scheduling_queue.add(tempProc)  
        else :
            print ("This job exceeds the system's main memory capacity.")



    def perform_io(self,info):
        """Current process on cpu performs io
        """
        print("Event: I   Time: " + info['time'] )
        if self.cpu.busy() :
            tempProc = self.cpu.remove_process()
            tempProc.acct.IO_startTime = self.clock.current_time()
            tempProc.acct.IO_burstTime = int(info["ioBurstTime"])
            tempProc.acct.IO_compTime = tempProc.acct.IO_startTime + tempProc.acct.IO_burstTime
            self.IO_waiting_queue.add(tempProc)
            self.IO_waiting_queue.Q.sort(key=lambda x: x.acct.IO_compTime)


    def sem_acquire(self,info):
        """Acquire one of the semaphores
        """
        print("Event: W   Time: " + str(self.clock.current_time()) )
        if self.cpu.busy() :
            if self.semPool.semaphores[int(info["semaphore"])].count > 0 :
                self.semPool.semaphores[int(info["semaphore"])].count += -1;
            else:
                tempProc = self.cpu.remove_process()
                self.semPool.semaphores[int(info["semaphore"])].acquired_queue.add(tempProc)
                self.semPool.semaphores[int(info["semaphore"])].count += -1

    def sem_release(self,info):
        """Release one of the semaphores
        """
        print("Event: S   Time: " + str(self.clock.current_time()) )
        self.semPool.semaphores[int(info["semaphore"])].count += 1
        if len(self.semPool.semaphores[int(info["semaphore"])].acquired_queue.Q) > 0 :
            proc = self.semPool.semaphores[int(info["semaphore"])].acquired_queue.first()
            self.ready_queue.queues[0].add(proc)
            self.semPool.semaphores[int(info["semaphore"])].acquired_queue.remove()
            if self.cpu.running_process.priority == 2 :
                self.ready_queue.queues[1].add( self.cpu.remove_process() )

        

###################################################################################################

# === Class: Simulator===

class Simulator(object):
    """
    Not quite sure yet
    """
    def __init__(self, **kwargs):

        # Must have input file to continue
        if 'input_file' in kwargs:
            self.input_file = kwargs['input_file']
        else:
            raise Exception("Input file needed for simulator")
        
        # Can pass a start time in to init the system clock.
        if 'start_clock' in kwargs:
            self.input_file = kwargs['start_clock']
        else:
            self.start_clock = 0

        # Read jobs in apriori from input file.
        self.jobs_dict = load_process_file(self.input_file,return_type="Dict")

        # create system clock and do a hard reset it to make sure
        # its a fresh instance. 
        self.system_clock = Clock()
        self.system_clock.hard_reset(self.start_clock)

        # Initialize all the components of the system. 
        self.scheduler = Scheduler()    
        self.memory = Memory()
        self.cpu = Cpu()
        self.accounting = SystemAccounting()

        # A = new process enters system             -> calls scheduler.new_process
        # D = Display status of simulator           -> calls display_status
        # I = Process currently on cpu performs I/O -> calls scheduler.perform_io 
        # S = Semaphore signal (release)            -> calls scheduler.sem_acquire
        # W = Semaphore wait (acquire)              -> calls scheduler.sem_release
        self.event_dispatcher = {
            'A': self.scheduler.new_process,
            'D': self.display_status,
            'I': self.scheduler.perform_io,
            'W': self.scheduler.sem_acquire,
            'S': self.scheduler.sem_release
        }



        # Start processing jobs:
        
        tempStdOut = sys.stdout
        sys.stdout = open("OutputFile.txt", "w+")
        # While there are still jobs to be processed---------------------------------------------------------------------
        while len(self.jobs_dict) > 0  or not self.isFinished() :# should be changed probably!
           
            if len(self.scheduler.IO_waiting_queue.Q) > 0 :# check I/O queue
                proc = self.scheduler.IO_waiting_queue.first()
                if self.scheduler.clock.current_time() == proc.acct.IO_compTime :
                    self.scheduler.ready_queue.queues[0].add(proc)
                    self.scheduler.IO_waiting_queue.remove()
                    print( "Event: C   Time: " + str(self.scheduler.clock.current_time()) )

            self.putJobsOnReadyQueue()
            
            if self.scheduler.cpu.busy() :
                self.cpu.running_process.acct.num_bursts += 1 # PROCESS Finished
                if self.cpu.running_process.acct.num_bursts == self.cpu.running_process.burst_time :
                    tempProc = self.scheduler.cpu.remove_process()
                    self.memory.deallocate(tempProc.process_id)
                    tempProc.acct.end_time = self.system_clock.current_time()
                    tempProc.acct.turnaround_time = tempProc.acct.end_time - tempProc.arrival_time
                    self.scheduler.finished_jobs.add(tempProc)
                    print( "Event: T   Time: " + str(self.scheduler.clock.current_time()) )

                elif self.cpu.running_process.priority == 1 : # PROCESS USED 100 bursts
                    if self.system_clock.current_time() == self.cpu.process_start_time + 100 :
                        self.scheduler.cpu.running_process.priority = 2
                        self.scheduler.ready_queue.queues[1].add( self.scheduler.cpu.remove_process() )
                        print( "Event: E   Time: " + str(self.scheduler.clock.current_time()) )

                elif self.cpu.running_process.priority == 2 : # PROCESS USED 300 bursts
                    if self.system_clock.current_time() == self.cpu.process_start_time + 300 :
                        self.scheduler.ready_queue.queues[1].add( self.scheduler.cpu.remove_process() )
                        print( "Event: E   Time: " + str(self.scheduler.clock.current_time()) )
                    elif len(self.scheduler.ready_queue.queues[0].Q) > 0 :
                        self.scheduler.ready_queue.queues[1].add( self.scheduler.cpu.remove_process() )
                        

            # Events are stored in dictionary with time as the key
            key = str(self.system_clock.current_time())
            # If current time is a key in dictionary, run that event.
            if key in self.jobs_dict.keys():
                event_data = self.jobs_dict[key]
                event_type = event_data['event']
                # Call appropriate function based on event type
                self.event_dispatcher[event_type](event_data)
                # Remove job from dictionary
                del self.jobs_dict[key]
            #-------------------------------------------------------


            self.putJobsOnReadyQueue()


            if not self.scheduler.cpu.busy() : # Put a process on cpu
                if self.scheduler.ready_queue.queues[0].size() > 0 : # first level of MLFQ
                    tempProcess = self.scheduler.ready_queue.queues[0].remove()
                    tempProcess.priority = 1
                    if tempProcess.acct.num_bursts == 0:
                        tempProcess.acct.start_time = self.system_clock.current_time()
                    self.scheduler.cpu.run_process(tempProcess)
                elif self.scheduler.ready_queue.queues[1].size() > 0 : # second level of MLFQ
                    self.scheduler.cpu.run_process(self.scheduler.ready_queue.queues[1].remove())


            self.system_clock += 1

        #----------------------------------------------------------------------------------------------------------------



        print("\nThe contents of the FINAL FINISHED LIST")# Final output----------------------------------------------
        print("----------------------------------------\n")
        if len(self.scheduler.finished_jobs.Q) > 0 :
            print("Job #  Arr. Time  Mem. Req.  Run Time  Start Time  Com. Time")
            print("-----  ---------  ---------  --------  ----------  ---------\n")
            for job in self.scheduler.finished_jobs.Q :
                print( str(job.process_id).rjust(5) + "  " + str(job.arrival_time).rjust(9) , end = "" )
                print("  " + str(job.mem_required).rjust(9) + "  " + str(job.burst_time).rjust(8) , end = "" )
                print("  " + str(job.acct.start_time).rjust(10) + "  " + str( job.acct.end_time ).rjust(10) )
        else :
            print("The Final Finished List is empty.")

        turnaroundSum = 0
        waitSum = 0
        if len(self.scheduler.finished_jobs.Q) > 0 :
            for job in self.scheduler.finished_jobs.Q :
                turnaroundSum += job.acct.turnaround_time
                waitSum += job.acct.wait_time
            turnAve = turnaroundSum/len(self.scheduler.finished_jobs.Q)
            waitAve = waitSum/len(self.scheduler.finished_jobs.Q)
            print( "\n\nThe Average Turnaround Time for the simulation was %.3f units." % round(turnAve,3))
            print("\nThe Average Job Scheduling Wait Time for the simulation was %.3f units." % round(waitAve,3))
            print("\nThere are " + str(self.memory.available()) + " blocks of main memory available in the system.\n")
        #-------------------------------------------------------------------------------------------------------------

        sys.stdout = tempStdOut
        print("Simulation finished, OutputFile.txt file created.")


    def isFinished(self): # returns 1 if the simulation is finished
        if self.cpu.busy() : 
            return 0
        elif len(self.scheduler.IO_waiting_queue.Q) > 0 or len(self.scheduler.job_scheduling_queue) > 0 :
            return 0
        elif len(self.scheduler.ready_queue.queues[0].Q) > 0 or len(self.scheduler.ready_queue.queues[1].Q) > 0  :
            return 0
        else : 
            return 1


    def putJobsOnReadyQueue(self) :#----------------------------------------------------------------
        """If jobs fit in memory put them on ready queue.
        - **Args**:
            - None
        - **Returns**:
            - None
        """
        if self.scheduler.job_scheduling_queue.size() > 0 :
            if self.memory.fits(self.scheduler.job_scheduling_queue.first().mem_required) :
                tempProc = self.scheduler.job_scheduling_queue.remove()
                tempProc.acct.wait_time = self.scheduler.clock.current_time() - tempProc.arrival_time
                self.scheduler.ready_queue.queues[0].add(tempProc)
                self.memory.allocate(tempProc)
    #------------------------------------------------------------------------------------------------


    def display_status(self,info):

        print( "Event: D   Time: " + str(self.scheduler.clock.current_time()) )

        print("\n************************************************************\n")
        print("The status of the simulator at time "+info["time"]+".\n")
        print("The contents of the JOB SCHEDULING QUEUE")
        print("----------------------------------------\n")
        if len(self.scheduler.job_scheduling_queue.Q) > 0 :
            print("Job #  Arr. Time  Mem. Req.  Run Time")
            print("-----  ---------  ---------  --------\n")
            for job in self.scheduler.job_scheduling_queue.Q :
                print(str(job.process_id).rjust(5) + "  " + str(job.arrival_time).rjust(9) , end = "" )
                print("  " + str(job.mem_required).rjust(9) + "  " + str(job.burst_time).rjust(8))
        else :
            print("The Job Scheduling Queue is empty.")


        print("\n\nThe contents of the FIRST LEVEL READY QUEUE")
        print("-------------------------------------------\n")
        if len(self.scheduler.ready_queue.queues[0].Q) > 0 :
            print("Job #  Arr. Time  Mem. Req.  Run Time")
            print("-----  ---------  ---------  --------\n")
            for job in self.scheduler.ready_queue.queues[0] :
                print(str(job.process_id).rjust(5) + "  " + str(job.arrival_time).rjust(9) , end = "" )
                print("  " + str(job.mem_required).rjust(9) + "  " + str(job.burst_time).rjust(8))
        else :
            print("The First Level Ready Queue is empty.")


        print("\n\nThe contents of the SECOND LEVEL READY QUEUE")
        print("--------------------------------------------\n")
        if len(self.scheduler.ready_queue.queues[1].Q) > 0 :
            print("Job #  Arr. Time  Mem. Req.  Run Time")
            print("-----  ---------  ---------  --------\n")
            for job in self.scheduler.ready_queue.queues[1] :
                print(str(job.process_id).rjust(5) + "  " + str(job.arrival_time).rjust(9) , end = "" )
                print("  " + str(job.mem_required).rjust(9) + "  " + str(job.burst_time).rjust(8))
        else :
            print("The Second Level Ready Queue is empty.")


        print("\n\nThe contents of the I/O WAIT QUEUE")
        print("----------------------------------\n")
        if len(self.scheduler.IO_waiting_queue.Q) > 0 :
            print("Job #  Arr. Time  Mem. Req.  Run Time  IO Start Time  IO Burst  Comp. Time")
            print("-----  ---------  ---------  --------  -------------  --------  ----------\n")
            for job in self.scheduler.IO_waiting_queue.Q :
                print( str(job.process_id).rjust(5) + "  " + str(job.arrival_time).rjust(9) , end = "" )
                print("  " + str(job.mem_required).rjust(9) + "  " + str(job.burst_time).rjust(8) , end = "" )
                print("  " + str(job.acct.IO_startTime).rjust(13) + "  " + str(job.acct.IO_burstTime).rjust(8) , end = "" )
                print("  " + str( job.acct.IO_compTime).rjust(10) )
        else :
            print("The I/O Wait Queue is empty.")


        numDic = {'0':'ZERO', '1':'ONE', '2':'TWO', '3':'THREE', '4':'FOUR'}
        for i in range(5):
            print("\n\nThe contents of SEMAPHORE " + numDic[str(i)])
            print("------------------------------\n")
            print("The value of semaphore " + str(i) + " is " + str(self.scheduler.semPool.semaphores[i].count) + ".\n")
            if len(self.scheduler.semPool.semaphores[i].acquired_queue.Q) > 0 :
                for job in self.scheduler.semPool.semaphores[i].acquired_queue.Q :
                    print(job.process_id)
            else :
                print("The wait queue for semaphore " + str(i) + " is empty.")


        print("\n\nThe CPU  Start Time  CPU burst time left")
        print("-------  ----------  -------------------\n")
        if self.cpu.busy() :
            print(self.cpu.running_process.process_id.rjust(7) + "  " + str(self.cpu.running_process.acct.start_time).rjust(10) , end = "" )
            print("  " + str(self.cpu.running_process.burst_time - self.cpu.running_process.acct.num_bursts).rjust(19))
        else : 
            print("The CPU is idle.")

        print("\n\nThe contents of the FINISHED LIST")
        print("---------------------------------\n")
        if len(self.scheduler.finished_jobs.Q) > 0 :
            print("Job #  Arr. Time  Mem. Req.  Run Time  Start Time  Com. Time")
            print("-----  ---------  ---------  --------  ----------  ---------\n")
            for job in self.scheduler.finished_jobs.Q :
                print(str(job.process_id).rjust(5) + "  " + str(job.arrival_time).rjust(9) , end = "" )
                print("  " + str(job.mem_required).rjust(9) + "  " + str(job.burst_time).rjust(8) , end = "" )
                print("  " + str(job.acct.start_time).rjust(10) + "  " + str( job.acct.end_time).rjust(10) )
        else :
            print("The Final Finished List is empty.")


        print("\nThere are " + str(self.memory.available()) + " blocks of main memory available in the system.\n")



    def __str__(self):
        """
        Visual dump of class state.
        """
        return my_str(self)





###################################################################################################
# Test Functions
###################################################################################################

def run_tests():
    print("############################################################")
    print("Running ALL tests .....\n")
#    temp = input('Enter your input:')
    test_process_class()
    test_class_clock()
    test_cpu_class()
    test_memory_class()
    test_semaphore_class()


if __name__ == '__main__':

    file_name1 = os.path.dirname(os.path.realpath(__file__))+'/input_data/jobs_in_c.txt'
    file_name2 = os.path.dirname(os.path.realpath(__file__))+'/input_data/jobs_in_test.txt'
#    temp = input('Enter your input:')
    S = Simulator(input_file=file_name1)
    



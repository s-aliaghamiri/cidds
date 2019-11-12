import threading
import matplotlib.pyplot as plt
from base.DAG import DAG
import time
import random

startTime = 0

def getTime():
    global startTime
    if startTime == 0:
        startTime = time.time()
    
    timeNow = time.time()
    time_ = timeNow - startTime
    print(int(time_))
    return int(time_)

def start_helper(sim):

    '''

    :param sim: simulator object
    :return: dag : DAG
    '''

    # Set plots for resulting dag image
    plt.rc('axes', labelsize=20)
    plt.rc('xtick', labelsize=20)
    plt.rc('ytick', labelsize=20)

    plt.figure(figsize=(25, 10))

    if sim.algorithm == "cac":
        # Call the DAG to generate transactions
        dag = DAG(rate=sim.alpha, algorithm=sim.algorithm, plot=True, numUsers=sim.numTotalUser, numMalUsers=sim.numMalUser)

        threads = []
        for userId in range(sim.numTotalUser):
            threads.append(threading.Thread(target=cac_for_user, args=(dag, userId, sim.traUser)))
        
        for t in threads:
            t.start()
        
        for t in threads:
            t.join()

    else:
        # Call the DAG to generate transactions
        dag = DAG(rate=sim.alpha, algorithm=sim.algorithm, plot=True)

        for i in range(sim.transactions):
            dag.generate_next_node()

    # Return the result
    return dag

def cac_for_user(dag, userId, transactions):
    for i in range(transactions):
        timee = getTime()
        dag.generate_next_node_for_cac_user(userId=userId, time=timee)
        time.sleep(random.uniform(0, 3))
    # dag.generate_next_node_for_cac_user(userId=userId, time=timee)

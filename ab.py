

from __future__ import division
import scipy.stats 
import numpy
import math
import random
import datetime



def confidence_level(convA, nA, convB, nB):
    pA = convA/nA
    pB = convB/nB
    try:
        Z = (pB - pA) / math.sqrt((pA * (1 - pA))/nA + (pB * (1 - pB))/nB)
    except:
        Z = 0
    conf = scipy.stats.norm.sf(-Z)
    return(conf)


def min_imps_needed(convA, nA, convB, nB):  
    pA = convA/nA
    pB = convB/nB
    imps_needed = 6.13 * (pA * (1 - pA) + pB * (1 - pB))/((pA - pB)*(pA - pB))
    return(imps_needed)


def set_checkpoint(baseline, lift):
    variance = (1 + lift) * baseline * (1 - (1 + lift) * baseline) + baseline * (1 - baseline) 
    diff = ((1 + lift) * baseline - baseline)**2
    checkpoint = 7.84 * variance / diff / 6
    return(checkpoint)


def conv_count_for_each_imp(convrate, max_imps):
    samples = numpy.random.random(size = max_imps) 
    conv_or_not = max_imps * ['NA']
    for i in range(max_imps):
        if(samples[i] <= convrate):
            conv_or_not[i] = 1
        else:
            conv_or_not[i] = 0 
    sum_conv = numpy.cumsum(conv_or_not)
    #print sum_conv
    return(sum_conv)

"""
f = open('asdf.txt', 'w')
for i in range(40):
    n = float(i+1)/100 
    A = set_checkpoint(n, 0.1)
    strA = "%.0f" % A 
    f.write(strA + '\n') 
    print A 
f.close()
"""




def ab_sim(convrateA, convrateB, number_of_tries, max_imps):
    nt = number_of_tries
    

    stop_imps = nt * ['NA']
    winner = nt * ['NA']
    for i in range(nt):    
        

        sum_convA = conv_count_for_each_imp(convrateA, max_imps)
        sum_convB = conv_count_for_each_imp(convrateB, max_imps)
        
        end = 0 
        j = 1
        while(end != 1):     
            cA = float(sum_convA[j-1])
            cB = float(sum_convB[j-1])                         
            conf = confidence_level(cA, j, cB, j)               
            try:
                imps_needed = min_imps_needed(cA, j, cB, j)
            except:
                imps_needed = 1000000   
            
            if(conf >= 0.95 and j >= 1100):
                stop_imps[i] = j  
                winner[i] = 2 
                end = 1
            
            if(conf <= 0.05 and j >= 1100):   
                stop_imps[i] = j 
                winner[i] = 1
                end = 1   
            
            if(j == max_imps and (cA - cB) > 0):         
                winner[i] = 3
                end = 1
          
            if(j == max_imps and (cA - cB) < 0):
                winner[i] = 4
                end = 1
            
            if(j == max_imps and cA == cB):
                winner[i] = 5 
                end = 1

            j += 1 

    
    Awin = len([i for i in winner if i == 1])
    Bwin = len([i for i in winner if i == 2])
    Awon = len([i for i in winner if i == 3])
    Bwon = len([i for i in winner if i == 4])
    

    print " convrateA: ", convrateA, "     convrateB: ", convrateB
    stop_imps_all = [i for i in stop_imps if i != 'NA']
    mean_stop_imps = scipy.mean(stop_imps_all)
    print mean_stop_imps    

    print " Out of ", nt, " trials, default version A wins with 95% confidence ", Awin, " times."
    print " Out of ", nt, " trials, test version B wins with 95% confidence ", Bwin, " times."
    print " Out of ", nt, " trials, default version A had more conversions at 40k imps ", Awon, " times."
    print " Out of ", nt, " trials, test version B had more conversions at 40k imps ", Bwon, " times. \n\n\n"



st = datetime.datetime.now()



          


ab_sim(0.2, 0.202, 200, 40000)
ab_sim(0.2, 0.204, 200, 40000)
ab_sim(0.2, 0.206, 200, 40000)
ab_sim(0.2, 0.21, 200, 40000)
ab_sim(0.2, 0.22, 200, 40000)
ab_sim(0.2, 0.24, 200, 40000)


"""
ab_sim(0.1, 0.101, 200, 40000)
ab_sim(0.1, 0.102, 200, 40000)
ab_sim(0.1, 0.103, 200, 40000)
ab_sim(0.1, 0.105, 200, 40000)
ab_sim(0.1, 0.11, 200, 40000)
ab_sim(0.1, 0.12, 200, 40000)


ab_sim(0.05, 0.0505, 200, 40000)
ab_sim(0.05, 0.051, 200, 40000)
ab_sim(0.05, 0.0515, 200, 40000)
ab_sim(0.05, 0.0525, 200, 40000)
ab_sim(0.05, 0.055, 200, 40000)
ab_sim(0.05, 0.06, 200, 40000)
          


ab_sim(0.02, 0.0202, 200, 40000)
ab_sim(0.02, 0.0204, 200, 40000)
ab_sim(0.02, 0.0206, 200, 40000)
ab_sim(0.02, 0.021, 200, 40000)
ab_sim(0.02, 0.022, 200, 40000)
ab_sim(0.02, 0.024, 200, 40000)
"""


ed = datetime.datetime.now()
print(ed - st)








          
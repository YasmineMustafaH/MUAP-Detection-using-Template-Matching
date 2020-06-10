import os,sys
from scipy import stats
import numpy as np
from scipy import signal
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt 

#-------------------------------------Moving Average Window----------------------------------------------------------------------------------
def movingAverageWindow(signal,N):
   result = []
   for i in range(len(signal)):
     result.append(np.sum(signal[i-N:i]))
   return np.multiply(result,(1/float(N)))
#--------------------------------------------------------------------------------------------------------------------------------------------   
def EMG_Decomposition(array,T):
   
      # step one: 
    # Set Threshold 
    # rectify the signal (apply absolute)
    array = np.array(array)
    rectified = abs(array)
    
    # Moving Average Window
    smoothed = movingAverageWindow(rectified,T)

    # Threshold is set to the noise 
    noise = 3*np.std(rectified[0:100])

    # detect the peak of each muap
    window = []
    muap = []
    index = []
    flag = 1

    peaks = []
    for i in range(len(smoothed)):
        if(smoothed[i] > noise ):
            peaks.append(i)
    
    # get the consecutive T values above the threshold using the flag 
    # then get the peak of these consecutive values
    for i in range(len(peaks)-1):
        if((peaks[i+1]-peaks[i])==1):
            window.append(array[peaks[i]])
            index.append(peaks[i])
        else:
            flag = 0 
        if(flag==0):
            if((len(window)>T)):
              window = np.array(window)
              max = np.argmax(window)   
              muap.append(index[max])
            window = []
            index = []
            flag = 1
    



  #-------------------------------------------------------------------------------------------------------------------------------------------------------        
  # Step 2:  
   # get window of each muap in the original signal
    DiffTh = 12**5
    muap_window = []
    for i in range(len(muap)):
       muap_window.append(array[muap[i]-int(T/2):muap[i]+int(T/2)])


    templates = []
    templates.append(muap_window[0])

    # classification holds the index of template of each MUAP 
    classification = []
    test = 0

    for i in range(len(muap_window)):
      for k in range(len(templates)):
        sum = 0
        for j in range(T):
              sum = sum + ((muap_window[i][j]-templates[k][j])**2)
        if(sum < DiffTh):
              classification.append(k)
              test= test +1
              # Update the template 
              templates[k] = (muap_window[i] + templates[k]) / 2.0
              break
      if(sum >= DiffTh):
            templates.append(muap_window[i])
            classification.append(len(templates)-1)
    print(len(templates))        
 # -----------------------------------------------------------------------------------------------------------
 # PLOTTING
 # plotting is not generic because it answers the specific questions in the assignment
    markers = []
    classes = []
    for i in range(len(muap)):
      if(muap[i]>=30000 and muap[i]<=35000):
        markers.append(muap[i]-30000)    
        classes.append(classification[i])

    samples = []
    for i in range(30000,35001):
        samples.append(array[i]) 



    for i in range(len(markers)):
        if(classes[i]==0):
            plt.scatter(markers[i],1000, marker="*",color='green')
        elif(classes[i]==1):
            plt.scatter(markers[i],1000, marker="*",color='red')
        elif(classes[i]==2):
            plt.scatter(markers[i],1000, marker="*",color='blue')


    plt.plot(samples) 
    plt.show()

    fig = plt.figure() 
 
    x1=fig.add_subplot(131)
    x1.plot(templates[0],color='green')
    x1.title.set_text('MUAP 1')

    x2=fig.add_subplot(132)
    x2.plot(templates[1],color='red')
    x2.title.set_text("MUAP 2")


    x2=fig.add_subplot(133)
    x2.plot(templates[2],color='blue')
    x2.title.set_text("MUAP 3")
    fig.tight_layout()

    # shift subplots down
    fig.subplots_adjust(top=0.85)
 
    plt.show()


    

    return muap , classification

#-----------------------------------------------------------------------------------------------------------------------------
with open('C:/Users/yasmi/Desktop/20-4/Data.txt') as file_in:
      array = []
      for line in file_in:
        array.append(float(line))
T=20


EMG_Decomposition(array,T)
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 18:09:43 2024

@author: Alessandro Restelli
"""
import serial
import time
import numpy as np
import pyvisa
from matplotlib import pyplot as plt
from timeit import timeit


class Scope():
    
    def __init__(self):
        rm = pyvisa.ResourceManager()
        self.scope = rm.open_resource('USB0::0x0957::0x17A4::MY53100338::INSTR',write_termination='\n',read_termination = '\n')
        

    
    def setup(self):
        #self.scope.write('*RST')
        
        # self.scope.write(':CHANnel1:DISPlay ON')
        # self.scope.write(':CHANnel2:DISPlay ON')
        # self.scope.write(':CHANnel3:DISPlay OFF')
        # self.scope.write(':CHANnel4:DISPlay OFF')
        
        # self.scope.query('*OPC?')
        # self.scope.write(':CHANnel1:OFFSet 0')
        # self.scope.query('*OPC?')
        # self.scope.write(':CHANnel2:OFFSet 1')
        
        self.scope.query('*OPC?')
        self.scope.write(':WAVeform:FORMat WORD')
        self.scope.query('*OPC?')
        self.scope.write(':WAVEFORM:POINTS:MODE RAW') 
        self.scope.query('*OPC?')
        self.scope.write(':WAVEFORM:POINTS 50000')
        
    def set_v_scale(self,values=[1,1,1,1]):
        self.scope.query('*OPC?')        
        self.scope.write(':CHANnel1:SCALe '+str(values[0]))
        self.scope.query('*OPC?')
        self.scope.write(':CHANnel2:SCALe '+str(values[1]))
        self.scope.query('*OPC?')
        self.scope.write(':CHANnel3:SCALe '+str(values[2]))
        self.scope.query('*OPC?')
        self.scope.write(':CHANnel4:SCALe '+str(values[3]))
        
    def set_timescale(self, microseconds):
        self.scope.query('*OPC?')
        self.scope.write(':TIMebase:SCALe '+str(microseconds)+'E-6')
        
    def scopes_set_timeoffset(self, microseconds):
        self.scope.query('*OPC?')
        self.scope.write(':TIMebase:POSition '+str(microseconds)+'E-6')
    
    def set_trigger(self,source='CHAN2',level=1):
        # source can  be EXTernal, CHAN1, etc
        # Level is the voltage level to set the trigger
      
        
        # Autoscale was only deemed necessary for scope 1, by trial and error...
        #self.scope2.write(':AUToscale')
        self.scope.query('*OPC?')
        self.scope.write(':TRIGGER:MODE EDGE')
        self.scope.query('*OPC?')
        self.scope.write(':TRIGGER:EDGE:SLOPE POSITIVE')
        self.scope.query('*OPC?')
        self.scope.write(':TRIGger:EDGE:SOURce '+source)
        self.scope.query('*OPC?')
        self.scope.write(':TRIGger:EDGE:LEVel '+str(level))
        self.scope.query('*OPC?')
        self.scope.write(':TRIGger:SWEep NORMal ')
        self.scope.query('*OPC?')
        
    def get_traces(self,num_datapoints=50000):
        # returns (data,time) tuple
        # data is a numpy array of shape [channel,voltage] and time is just [time]
       
        data = np.zeros([2,num_datapoints])
        
        
        self.scope.write(':STOP')
        
        self.scope.query('*OPC?')
        self.scope.write(':WAVeform:SOURce CHAN1')
        self.scope.query('*OPC?')
        self.scope.write(":WAV:DATA?")
        data_from_scope = self.scope.read_raw()[9:-2]
        data[0,:] = np.frombuffer(data_from_scope,dtype = np.uint16)
        
        self.scope.query('*OPC?')
        self.scope.write(':WAVeform:SOURce CHAN2')
        self.scope.query('*OPC?')
        self.scope.write(":WAV:DATA?")
        data_from_scope = self.scope.read_raw()[9:-2]
        data[1,:] = np.frombuffer(data_from_scope,dtype = np.uint16)
        self.scope.write(':RUN')
        
    
        
        
        #timeinc = float(self.scope3.query(':WAVeform:XINCrement?'))
        #time = np.arange(0,timeinc*num_datapoints,timeinc)
        
        return data#,time
       


def run():
    scope=Scope()
    
    scope.setup()
    #scope.set_v_scele(1)
    #scope.set_timescale(1e-9)
    #scope.set_trigger(level = 1.0)
    
    data=scope.get_traces()

    plt.plot(data[0])
    plt.plot(data[1])
    plt.show()
    




        
if __name__ == "__main__":
    print(timeit( run, number=1))
    
#!/usr/bin/python3
##    Pitch Perfect recorder, application for real time recording and 
##    display of fundamental frequency.
##    Copyright (C) 2019 Adrian Cheater
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pyqtgraph as pg
import numpy as np
from scipy import signal
import math
import random
import cmath
import pyaudio
import wave
import sys
import os

signalData = []
BINS = 1024
RATE = 44100
CHUNK = BINS*2
FORMAT = pyaudio.paInt16
CHANNELS = 1

p = pyaudio.PyAudio()

path = sys.argv[1]
if os.path.isfile( path ):
    print( "You would be overwriting", path, "Aborting!" )
    sys.exit(1)

wf = wave.open( path, "wb" )
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)

app = pg.QtGui.QApplication([])
win = pg.GraphicsWindow(title="Basic plotting examples")
win.resize(1900,1080)
win.setWindowTitle('pyqtgraph example: Plotting')

#signalGraph = win.addPlot(title="Signal Graph")
#sigPlot = signalGraph.plot(pen='y')

#fftOutput = win.addPlot(title="FFT Output")
#fftPlot = fftOutput.plot(pen='y')

zoomFFTOutput = win.addPlot(title="Zoom FFT Output")
zoomFFTOutput.setYRange(0,10000)
zoomFFTPlot = zoomFFTOutput.plot(pen='y')

def gen_tone_data( sampleRate, samples ):
    f1 = 200 
    f2 = 220
    dt = 1/sampleRate
    pi2dt = 2.0*math.pi*dt;

    return [ 2*math.sin(pi2dt*f1*i)+1*math.sin(pi2dt*f2*i) for i in range(samples)]
    #return [ 2*math.sin(pi2dt*f1*i)+1*math.sin(pi2dt*f2*i)+(random.random()-0.5) for i in range(samples)]

def myfft( signalBuf, sampleRate, nBins, offset ):
    outBins = (nBins//2) 
    binWidth = (sampleRate/2) / outBins
#    print( "sampleRate", sampleRate, "min", offset, "outbins", outBins, "binWidth", binWidth, "max", (outBins-1)*binWidth+offset )
    return [ [ offset + i * binWidth for i in range(outBins) ], [abs(x) for x in np.fft.fft(signalBuf,n=nBins)[0:outBins] ] ]

def shiftFrequency( samples, sampleRate, adjustBy ):
    dt = 1/sampleRate
    pi2dtcf = 2*math.pi*dt*adjustBy
    vals = [ cmath.exp(1j*pi2dtcf*i)*samples[i] for i in range(len(samples)) ]
    return vals

def zoom_fft( samples, sampleRate, nBins, fStart, fEnd ):
    bandwidth = (fEnd - fStart)
    decFactor = sampleRate//bandwidth//2
    shifted = shiftFrequency( samples, sampleRate, -fStart )
    resampled = signal.decimate(shifted,decFactor,ftype='fir')
    newSampleRate = sampleRate//decFactor
#    print("decFactor",decFactor,"newSampleRate",newSampleRate)
    vals = myfft( resampled, newSampleRate, nBins, fStart )    
    return vals

def callback( in_data, frame_count, time_info, status ):
    wf.writeframes( in_data )

    signalData = np.frombuffer(in_data,dtype=np.int16)
    #signalData = gen_tone_data( RATE, frame_count )
    #sigPlot.setData( signalData )

    #fftData = myfft(signalData, RATE, BINS, 0.0)
    #fftPlot.setData( *fftData )

    zoomFFTData = zoom_fft( signalData, RATE, BINS, 140, 300 )
    zoomFFTPlot.setData( *zoomFFTData )
    
    return (None, pyaudio.paContinue)

stream = p.open( format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, stream_callback=callback )
stream.start_stream()
app.exec()
stream.stop_stream()
stream.close()
wf.close()
p.terminate()


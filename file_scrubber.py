##    Pitch Perfect playback, application for playback and scrubbing for 
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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyqtgraph as pg
import pyaudio
import numpy as np
import wave
import time
import math
import cmath
from scipy import signal
import sys

BINS=1024
CHUNK=2*BINS

app = QApplication([])
win = pg.GraphicsWindow(title="file play")
win.resize(1024,640)

#slider = QSlider(Qt.Horizontal)
#win.centralLayout.addWidget(slider)
#signalGraph = win.addPlot(title="Signal")
#sigPlot = signalGraph.plot(pen='y')
#signalGraph.setYRange(-10000,10000)

#fftOutput = win.addPlot(title="FFT")
#fftPlot = fftOutput.plot(pen='y')

zoomFFTOutput = win.addPlot(title="Zoom FFT")
zoomFFTOutput.setYRange(0,10000)
zoomFFTPlot = zoomFFTOutput.plot(pen='y')

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
    vals = myfft( resampled, newSampleRate, nBins, fStart )    
    return vals

def callback( in_data, frame_count, time_info, status ):
    data = wavefile.readframes(frame_count)
    curFrame = wavefile.tell()
    totalFrames = wavefile.getnframes()
    rate = wavefile.getframerate()
    if curFrame == totalFrames: app.quit()
    
    signalData = np.frombuffer(data,dtype=np.int16)
    #sigPlot.setData( signalData )

    #fftData = myfft(signalData, rate, BINS, 0.0)
    #fftPlot.setData( *fftData )

    zoomFFTData = zoom_fft( signalData, rate, BINS, 140, 300 )
    zoomFFTPlot.setData( *zoomFFTData )
    return (data, pyaudio.paContinue)

print("starting up")
wavefile = wave.open(sys.argv[1],'rb')
rate = wavefile.getframerate()
bytes_per_sample = wavefile.getsampwidth()
channels = wavefile.getnchannels()

p = pyaudio.PyAudio()
stream = p.open( format=p.get_format_from_width(bytes_per_sample), channels=channels, rate=rate, frames_per_buffer=CHUNK, output=True, stream_callback=callback )

stream.start_stream()
print("Starting app")
app.exec()

print("Shutting down")
stream.stop_stream()
stream.close()
wavefile.close()
p.terminate()

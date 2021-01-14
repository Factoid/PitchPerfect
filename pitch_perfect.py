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

import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import wave
import pyaudio
import numpy as np
import math
import cmath
from scipy import signal
import os
from collections import deque

def myfft( signalBuf, sampleRate, nBins, offset ):
    outBins = (nBins//2) 
    binWidth = (sampleRate/2) / outBins
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

class Example( QMainWindow ):
    BINS=512
    RANGE=BINS

    LOW = 80
    HIGH = LOW+BINS
    CHUNK=RANGE*2
    
    def __init__(self):
        super(Example,self).__init__()
       
        self.stream = None
        self.p = pyaudio.PyAudio()

        if( not os.path.isdir( "data" ) ): os.mkdir("data")

        self.resize(1024, 640)  # The resize() method resizes the widget.
        self.setWindowTitle("Pitch Perfect")  # Here we set the title for our window.

        playbar = QWidget()
        sizePolicy = QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        self.record = QPushButton("Record")
        self.open = QPushButton("Open")
        self.stop = QPushButton("Stop")

        self.open.clicked.connect(self.open_file)
        self.record.clicked.connect(self.record_file)
        self.stop.clicked.connect(self.stop_file)

        self.s1 = QScrollBar(Qt.Horizontal)
        self.s1.sliderMoved.connect(self.sliderMoved)

        signalGraph = pg.PlotWidget()
        signalGraph.setTitle("Zoom FFT")
        self.sigPlot = signalGraph.plot(pen='y')
        signalGraph.setXRange(self.LOW,self.HIGH)

        pitchGraph = pg.PlotWidget()
        pitchGraph.setTitle("F0 Tracking")
        self.pitchPlot = pitchGraph.plot(pen='b')
        pitchGraph.setYRange(self.LOW,self.HIGH)
        
        center = QWidget()
        self.setCentralWidget(center)

        pb_layout = QHBoxLayout()
        playbar.setLayout(pb_layout)
        pb_layout.addWidget(self.open)
        pb_layout.addWidget(self.record)
        pb_layout.addWidget(self.stop)
        self.stop.hide()
        
        layout = QVBoxLayout()
        center.setLayout(layout)
        layout.addWidget(playbar)
        layout.addWidget(self.s1)
        layout.addWidget(signalGraph)
        layout.addWidget(pitchGraph)

        self.show()  # The show() method displays the widget on the screen.

        self.pitches = deque(maxlen=200)

    def stop_file(self, event):
        self.stream.stop_stream()
        self.stop.hide()
        self.record.show()
        self.open.show()
        self.timer.stop()

    def open_file(self, event):
        fname = QFileDialog.getOpenFileName(self, "Open File", "data", "Audio Files (*.wav)")
        if( self.stream != None ): self.stream.stop_stream()
        if( fname == None or fname == "" ): return

        self.wavefile = wave.open(fname[0],'rb')
        self.s1.setMaximum(self.wavefile.getnframes())
        self.s1.setPageStep(10*44100//self.CHUNK)
        self.rate = self.wavefile.getframerate()
        bytes_per_sample = self.wavefile.getsampwidth()
        channels = self.wavefile.getnchannels()
        self.stream = self.p.open( format=self.p.get_format_from_width(bytes_per_sample), channels=channels, rate=self.rate, frames_per_buffer=self.CHUNK, output=True, stream_callback=self.audio_callback)
        self.stream.start_stream()
        self.stop.show()
        self.record.hide()
        self.open.hide()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDisplay)
        self.timer.start(20)

    def updateDisplay(self):
        self.pitchPlot.setData( self.pitches )

    def record_file(self, event):
        fname = QFileDialog.getSaveFileName(self, "Save File", "data", "Audio Files (*.wav)")
        if( self.stream != None ): self.stream.stop_stream()
        if( fname == None or fname == "" ): return

        self.wavefile = wave.open(fname[0],'wb')
        self.wavefile.setnchannels(1)
        self.wavefile.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        self.rate=44100
        self.wavefile.setframerate(self.rate)
        self.stream = self.p.open( format=pyaudio.paInt16, channels=1, rate=self.rate, input=True, frames_per_buffer=self.CHUNK, stream_callback=self.write_audio_callback )
        self.stream.start_stream()
        self.stop.show()
        self.record.hide()
        self.open.hide()

    def write_audio_callback( self, in_data, frame_count, time_info, status ):
        self.wavefile.writeframes( in_data )
        #signalData = np.frombuffer(in_data,dtype=np.int16)
        #zoomFFTData = zoom_fft( signalData, self.rate, self.BINS, self.LOW, self.HIGH )
        #self.updatePitches(zoomFFTData)
        
        return (None, pyaudio.paContinue)

    def stacked(self, vals):
        for i in range(1,len(vals)):
            for j in range(i+1,len(vals)):
                ratio = vals[j][0]/vals[i][0]
                frac = ratio - int(ratio)
                if frac < 0.05 or frac > 0.95:
                    #breakpoint()
                    #print( "adding", vals[j][0], "to", vals[i][0] )
                    vals[i] = (vals[i][0], vals[i][1] + vals[j][1])
        return vals
        
    def updatePitches(self, zoomFFTData):
#stacking approach
#        vals = self.stacked( list(zip(*zoomFFTData)) )
        best = max( zip(*zoomFFTData), key=lambda x: x[1] )
        self.pitches.append( best[0] )

#strongest signal approach
#        vals = list(zip(*zoomFFTData))
        #breakpoint()
#        softest = min( vals, key=lambda x: x[1])[1]
#        loudest = max( vals, key=lambda x: x[1])[1]
#        fvals = list(filter(lambda x: (x[1]-softest)/(loudest-softest) >= 0.75,vals))
#        if( len(fvals) > 0 ):
#            best = min( fvals,key=lambda x: x[0] )
#            self.pitches.append( fvals[0][0] )
#        else:
#            self.pitches.append( 0 )
        
    def audio_callback( self, in_data, frame_count, time_info, status ):
        data = self.wavefile.readframes(frame_count)
        curFrame = self.wavefile.tell()
        self.s1.setValue(curFrame)
        totalFrames = self.wavefile.getnframes()
        if( curFrame == totalFrames ):
            self.stop.click()
            return (None, pyaudio.paComplete)

        signalData = np.frombuffer(data,dtype=np.int16)
        zoomFFTData = zoom_fft( signalData, self.rate, self.BINS, self.LOW, self.HIGH )
        self.sigPlot.setData( *zoomFFTData )
        self.updatePitches(zoomFFTData)
        
        return (data, pyaudio.paContinue)

    def sliderMoved(self):
        print( self.s1.value() )

    def closeEvent(self, event):
        reply = QMessageBox.question(self,"Quit Application","Really quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if( reply == QMessageBox.Yes ):
            event.accept()
            if self.stream: self.stream.stop_stream()
        else:
            event.ignore()

app = QApplication(sys.argv)
ex = Example()
sys.exit(app.exec_())  # Finally, we enter the mainloop of the application.

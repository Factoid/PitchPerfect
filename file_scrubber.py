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
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import pyqtgraph as pg
import wave
import pyaudio
import numpy as np
import math
import cmath
from scipy import signal

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
    BINS=1024
    CHUNK=2*BINS
    
    def __init__(self):
        super(Example,self).__init__()
       
        self.stream = None

        self.resize(1024, 640)  # The resize() method resizes the widget.
        self.setWindowTitle("Hello, World!")  # Here we set the title for our window.
        self.setWindowIcon( QIcon("icon.png") )

        self.statusBar().showMessage("Running!")

        playbar = QWidget()
        sizePolicy = QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        self.play = QPushButton("Play")
        self.open = QPushButton("Open")

        self.play.setSizePolicy(sizePolicy)
        self.play.clicked.connect(self.play_clicked)
        self.open.clicked.connect(self.open_file)

        self.s1 = QScrollBar(Qt.Horizontal)
        self.s1.sliderMoved.connect(self.sliderMoved)

        signalGraph = pg.PlotWidget()
        signalGraph.setTitle("Zoom FFT")
        self.sigPlot = signalGraph.plot(pen='y')
        signalGraph.setYRange(0,10000)
        
        center = QWidget()
        self.setCentralWidget(center)

        pb_layout = QHBoxLayout()
        playbar.setLayout(pb_layout)
        pb_layout.addWidget(self.open)
        pb_layout.addWidget(self.play)
        
        layout = QVBoxLayout()
        center.setLayout(layout)
        layout.addWidget(playbar)
        layout.addWidget(self.s1)
        layout.addWidget(signalGraph)

        self.show()  # The show() method displays the widget on the screen.

    def open_file(self, event):
        fname = QFileDialog.getOpenFileName(self, "Open File", "data", "Audio Files (*.wav)")
        if( self.stream != None ):
            self.stream.stop_stream()

        self.wavefile = wave.open(fname,'rb')
        self.rate = self.wavefile.getframerate()
        bytes_per_sample = self.wavefile.getsampwidth()
        channels = self.wavefile.getnchannels()
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open( format=self.p.get_format_from_width(bytes_per_sample), channels=channels, rate=self.rate, frames_per_buffer=self.CHUNK, output=True, stream_callback=self.audio_callback)
        self.stream.start_stream()

    def audio_callback( self, in_data, frame_count, time_info, status ):
        data = self.wavefile.readframes(frame_count)
        curFrame = self.wavefile.tell()
        totalFrames = self.wavefile.getnframes()
#        rate = self.wavefile.getframerate()

        #self.statusBar().showMessage( str(100.0 * curFrame / totalFrames) + "%" )
        #print( curFrame, totalFrames, str(100.0 * curFrame / totalFrames) + "%" )
        signalData = np.frombuffer(data,dtype=np.int16)
        #sigPlot.setData( signalData )

        #fftData = myfft(signalData, self.rate, self.BINS, 0.0)
        #fftPlot.setData( *fftData )

        zoomFFTData = zoom_fft( signalData, self.rate, self.BINS, 100, 400 )
        self.sigPlot.setData( *zoomFFTData )
        return (data, pyaudio.paContinue)

    def sliderMoved(self):
        print( self.s1.value() )

    def closeEvent(self, event):
        self.statusBar().showMessage("Wait, what?")
        reply = QMessageBox.question(self,"Message","Really quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if( reply == QMessageBox.Yes ):
            event.accept()
        else:
            self.statusBar().showMessage("Whew!")
            event.ignore()

    def play_clicked(self, event):
        print("Clicked!")

app = QApplication(sys.argv)
ex = Example()
sys.exit(app.exec_())  # Finally, we enter the mainloop of the application.

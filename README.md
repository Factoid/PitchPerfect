# PitchPerfect
Open source resources for SLP and vocal training

The aim of this software is to help develop cross platform tools for analyzing speech
with a focus on providing real time feedback for those involved in vocal therapy either
as patients or practitioners.

This is a work in progress, presently very limited in function and user friendlyness,
as they are tools that I am personally using in my own vocal training.

The software is written in python3, and has dependencies on PyQt4, pyqtgraph, numpy
scipy, and pyaudio. It should be cross platform but it is being developed on Linux

The record and playback functions have now been unified in the pitch_perfect.py application.
Upon launch you will be able to choose a file for playback, or a file for recording.

Once playback or recording has begun you may click stop to end the operation.

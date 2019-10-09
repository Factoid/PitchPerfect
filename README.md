# PitchPerfect
Open source resources for SLP and vocal training

The aim of this software is to help develop cross platform tools for analyzing speech
with a focus on providing real time feedback for those involved in vocal therapy either
as patients or practitioners.

This is a work in progress, presently very limited in function and user friendlyness,
as they are tools that I am personally using in my own vocal training.

The software is written in python3, and has dependencies on PyQt4, pyqtgraph, numpy
scipy, and pyaudio. It should be cross platform but it is being developed on Linux

Assuming you can configure your environment to run it, the two scripts work as follows

Recording:
python3 ./recorder.py <output/path/to/file.wav>

Playback:
python3 ./file_scrubber.y <input/file/to/view.wav>

Notes:
The recorder will not allow you to record over an existing file, you must delete the file first
If your OS permits, you can use a temp file like /dev/null for output so you can just play around
with the visualizer

The playback application will display the same 140-300 Hz band from a previously recorded file, automatically
closing when the playback is complete.

# PitchPerfect
Open source resources for SLP and vocal training

The aim of this software is to help develop cross platform tools for analyzing speech
with a focus on providing real time feedback for those involved in vocal therapy either
as patients or practitioners.

The long term goal of the project is to deveop a free and open application that is easy
to use, and valuable for both individuals working on their voice, and SLP practitioners
who may be guiding them.

Ideally this project will be able to conduct a baseline assessment, and use that to
simulate possible voices that could be achieved safely, allowing individuals to find
one they feel suits them. From there, the software will be able to guide individuals through
exercises and techniques designed to help them reach that goal, while also providing
useful real time visual feedback and coaching.

It is not intended to replace the expertise of an SPL, but to reduce barriers for those 
who may not be able to access professional services, and enhance the ways in which SLPs can
provide services.

More research may be required to achieve this goal, but the shorter term of producing an
effective feedback tool for clients, SLPs, and researchers, is achievable now.

##GstOpusVis
The Opus library is a free/open codec for real time audio compression. Of iterest to this
project is that lossy audio compression is about finding simple and efficent ways of
encoding sound such that they can be resynthesized in a way that is difficult for a listener
to differentiate from the original audio. This simplified view of the audio may make it
easier to visualzie and detect elements of speech that contirbute to how a voice is identified
especially with respect to gender assumptions.

Opus is especially useful because it can employ a LPC, Critical Band Spectra or both
to efficiently and accurately capture essential elements of speech in real time.

GStreamer is a cross platform audio codec designed for modular creation of media processing
chains. This allows us to focus on the missing component, the visualization of encoded opus packets,
without having to implement systems for capturing audio, encoding it, or playing it back.

##Pitch_Perfect.py
The initial work, kept for posterity is the pitch_perfect.py script. The current work
is focused on using the gstreamer framework to develop a visualizer for the SILK and CELT
compression models used by Opus.

The pitch_perfect.py application is written in python3, and has dependencies on PyQt5, pyqtgraph, numpy
scipy, and pyaudio. It should be cross platform but it is being developed on Linux

The record and playback functions have now been unified in the pitch_perfect.py application.
Upon launch you will be able to choose a file for playback, or a file for recording.

Once playback or recording has begun you may click stop to end the operation.

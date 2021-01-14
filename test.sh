#!/bin/sh

gst-launch-1.0 --gst-plugin-path=./ autoaudiosrc ! opusenc bandwidth=narrowband audio-type=voice frame-size=10 ! opusvis ! opusdec ! autoaudiosink

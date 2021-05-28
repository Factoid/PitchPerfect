#!/bin/sh

#gst-launch-1.0 --gst-plugin-path=./build autoaudiosrc ! opusenc bandwidth=narrowband audio-type=voice frame-size=10 ! opusvis ! fakesink
gst-launch-1.0 --gst-plugin-path=./build autoaudiosrc ! opusenc bandwidth=narrowband audio-type=voice frame-size=10 ! opusvis ! opusdec ! autoaudiosink

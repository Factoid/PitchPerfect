#!/bin/sh

gst-launch-1.0 --gst-plugin-path=./ autoaudiosrc ! opusenc ! opusvis ! opusdec ! autoaudiosink

import sys

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GLib, Gst

def bus_call(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.EOS:
        sys.stdout.write("End-of-stream\n")
        loop.quit()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        sys.stderr.write("Error: %s: %s\n" % (err, debug))
        loop.quit()
    return True

def main(args):
    Gst.init(None)
    reg = Gst.Registry.get()
    reg.scan_path("./")
    
#autoaudiosrc ! opusenc bandwidth=narrowband audio-type=voice frame-size=10 ! opusvis ! opusdec ! autoaudiosink
    pipeline = Gst.Pipeline.new("opus-pipeline")
    src = Gst.ElementFactory.make("autoaudiosrc","mic")
    enc = Gst.ElementFactory.make("opusenc", "enc")
    vis = Gst.ElementFactory.make("opusvis", "vis")
    dec = Gst.ElementFactory.make("opusdec", "dec")
    sink = Gst.ElementFactory.make("autoaudiosink","sink")

    pipeline.add(src)
    pipeline.add(enc)
    pipeline.add(vis)
    pipeline.add(dec)
    pipeline.add(sink)
    src.link(enc)
    enc.link(vis)
    vis.link(dec)
    dec.link(sink)

    # create and event loop and feed gstreamer bus mesages to it
    loop = GLib.MainLoop()

    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect ("message", bus_call, loop)
    
    # start play back and listed to events
    pipeline.set_state(Gst.State.PLAYING)
    try:
      loop.run()
    except:
      pass

if __name__ == '__main__':
    sys.exit(main(sys.argv))

# Setup
```bash
sudo apt install python3-pyaudio
python3 -m pip install PyQt5 pyqtgraph numpy scipy pyaudio
```

# Opus setup [Not needed]

```bash
sudo apt install libgstreamer1.0-dev
sudo apt install libgstreamer-plugins-base1.0-dev
mkdir lib
cd lib/
git clone https://github.com/Factoid/opus --recursive
cd opus/
./autogen.sh
./configure
make
cd ../..
./make.sh
```
# Running

1. `python3 pitch_perfect.py`
1. Press record
1. Name it test.wav
1. Speak
1. Press stop
1. Open the file using the open button
1. Analysis should run

## What Analysis Means

I really dont know I didnt write the software

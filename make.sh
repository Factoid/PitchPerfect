cd lib/opus
make
cd ../../

mkdir -p ./build

gcc -g3 -Wall -fPIC -I./lib/opus/include -I./lib/opus -I./lib/opus/celt $(pkg-config --cflags gstreamer-1.0 gstreamer-audio-1.0) -c -o build/gstopusvis.o src/gstopusvis.c
if test $? -ne 0; then
    exit 1
fi

gcc -g3 -Wl,--whole-archive ./lib/opus/.libs/libopus.a -Wl,--no-whole-archive -shared -o build/gstopusvis.so build/gstopusvis.o $(pkg-config --libs gstreamer-1.0 gstreamer-audio-1.0)
if test $? -ne 0; then
    exit 1
fi

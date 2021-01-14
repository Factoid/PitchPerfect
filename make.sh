gcc -Wall -Werror -fPIC -I./opus/include -I./opus -I./opus/celt $(pkg-config --cflags gstreamer-1.0 gstreamer-audio-1.0) -c -o gstopusvis.o gstopusvis.c
if test $? -ne 0; then
    exit 1
fi

gcc -Wl,--whole-archive ./opus/.libs/libopus.a -Wl,--no-whole-archive -shared -o gstopusvis.so gstopusvis.o $(pkg-config --libs gstreamer-1.0 gstreamer-audio-1.0)
if test $? -ne 0; then
    exit 1
fi

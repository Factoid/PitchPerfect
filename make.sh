gcc -Wall -Werror -fPIC $(pkg-config --cflags gstreamer-1.0 gstreamer-audio-1.0 opus) -c -o gstopusvis.o gstopusvis.c
if test $? -ne 0; then
    exit 1
fi

gcc -shared -o gstopusvis.so gstopusvis.o $(pkg-config --libs gstreamer-1.0 gstreamer-audio-1.0 opus)
if test $? -ne 0; then
    exit 1
fi

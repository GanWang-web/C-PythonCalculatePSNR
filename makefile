CC=gcc
CFLAGS= -fPIC -shared -Wall -Werror

c_functions.so: c_functions.o
	${CC} ${CFLAGS} c_functions.o -o c_functions.so
c_functions.o: c_functions.c
	${CC} -c c_functions.c
clean:
	rm *.so c_functions
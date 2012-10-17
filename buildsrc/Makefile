
# Output
#
TARGET = ../bin/build-bakery

# Libraries
#
INCLUDES = 
LIBS = 

# Sources
#
HEADERS = 
SOURCES = main.o

# Flags
#
DEBUGFLAGS =
CFLAGS = 
LDFLAGS = 

# Plumbing
# http://www.cs.colby.edu/maxwell/courses/tutorials/maketutor/
# 
CXX = g++

all: $(TARGET)

%.o: %.c $(HEADERS)
	$(CXX) -c -o $@ $< $(CFLAGS) $(INCLUDES)

$(TARGET): $(SOURCES)
	$(CXX) -o $@ $^ $(CFLAGS) $(LDFLAGS) $(LIBS)

clean:
	rm -f $(SOURCES)

distclean:
	rm -f $(SOURCES) $(TARGET)


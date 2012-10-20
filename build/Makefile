
# Output
#
TARGET = build-bakery

# Libraries
#
INCLUDES = 
LIBS = 

# Sources
#
HEADERS = scan.h \
		  manifest.h \
		  headers.h
SOURCES = main.o \
		  scan.o \
		  manifest.o \
		  headers.o

# Flags
#
CFLAGS = -Wall
LDFLAGS = 

# Plumbing
# http://www.cs.colby.edu/maxwell/courses/tutorials/maketutor/
# 
CXX = g++

all: $(TARGET)

%.o: %.cpp $(HEADERS)
	$(CXX) -c -o $@ $< $(CFLAGS) $(INCLUDES)

$(TARGET): $(SOURCES)
	$(CXX) -o $@ $^ $(CFLAGS) $(LDFLAGS) $(LIBS)

clean:
	rm -f $(SOURCES)

distclean:
	rm -f $(SOURCES) $(TARGET)


---
layout: post
title: Makefile templates for building C++
---

Simple makefile for building a C++ binary on Linux using GCC and SDL2 libraries. To be used as a replacement for a `g++` command or extended.

```
TARGET=$(shell basename $$(pwd))
SOURCES=$(shell echo *.cpp)
OBJECTS=$(SOURCES:.cpp=.o)
CXXFLAGS=-Wall -march=native -gdwarf-3 -std=c++1y -O3 -g $(shell sdl2-config --cflags)
LDFLAGS=$(shell sdl2-config --libs)
$(TARGET): $(OBJECTS)
	g++ $(OBJECTS) $(LDFLAGS) -o $(TARGET)
%.o: %.cpp
	g++ $(CXXFLAGS) -c $< -MT $@ -MMD -MP -MF $*.mk~
-include *.mk~
clean:
	rm -f *~
	rm -f *.o
	rm -f $(TARGET)

```

This is a modified version of the above that uses a file structure (src, obj, inc and bin directories) on the same level as the Makefile. 

Improvements:

* A default target needs to be added instead of leaving it to TARGET as the first one.
* Rethink the use of `create_dirs` target. 

Notes:
* `-MMD` flag is responsible for creating `.d` files.


```
CC = g++
TARGET=$(shell basename $$(pwd))

SRCDIR = src
OBJDIR = obj
INCDIR = inc
BINDIR = bin

SOURCES  := $(wildcard $(SRCDIR)/*.cpp)
INCLUDES := $(wildcard $(INCDIR)/*.h)
OBJECTS  := $(SOURCES:$(SRCDIR)/%.cpp=$(OBJDIR)/%.o)
rm       = rm -f

CXXFLAGS = -I./$(INCDIR) -Wall -std=c++14 -O3 -g
CXXFLAGS += -DENABLE_LOGGER
#CXXFLAGS += -DDEBUG_LOGGING_ENABLED
LFLAGS = -lpthread

$(BINDIR)/$(TARGET): create_dirs $(OBJECTS)
	@$(CC) $(OBJECTS) $(LFLAGS) -o $@
	@echo "Linking complete!"

$(OBJECTS): $(OBJDIR)/%.o : $(SRCDIR)/%.cpp
	@$(CC) $(CXXFLAGS) -MMD -c $< -o $@
	@echo "Compiled "$<" successfully!"

.PHONY: create_dirs
create_dirs:
	@if [ ! -d "./$(BINDIR)" ];then \
		mkdir $(BINDIR);\
	fi
	@if [ ! -d "./$(OBJDIR)" ];then \
		mkdir $(OBJDIR);\
	fi

.PHONY: clean
clean:
	@$(rm) $(OBJECTS)
	@$(rm) $(OBJDIR)/*.d
	@$(rm) $(BINDIR)/$(TARGET)
	@echo "Cleanup complete!"
```

TODO Add a template for calling subdir Makefiles from the master one.
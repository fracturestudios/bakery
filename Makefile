
all:
	python ./setup.py build
	cd ext/test && make all

clean:
	python ./setup.py clean && rm -fr build
	cd ext/test && make clean

distclean:
	python ./setup.py clean && rm -fr build
	cd ext/test && make distclean

install:
	python ./setup.py install
	cd ext/test && make install


from distutils.core import setup, Extension

NAME                    = 'bakery-test-extension'
DESC                    = 'Learning how to build C extensions'
DESCRIPTION             = 'Longer description text'
AUTHOR                  = 'Dave Kilian'
EMAIL                   = 'dave.kilian@gmail.com'
URL                     = 'http://github.com/fracturestudios/bakery'

MODULE                  = 'bakery.ext.test'
VERSION_MAJOR           = 1
VERSION_MINOR           = 0

DEFINES                 = [ 
                            ('VERSION_MAJOR', VERSION_MAJOR),
                            ('VERSION_MINOR', VERSION_MINOR),
                          ]
INCLUDEDIRS             = [ ]
LIBS                    = [ ]
LIBDIRS                 = [ ]
SOURCES                 = [ 
                            'testmodule.c' 
                          ]

def main():

    # http://docs.python.org/2/distutils/apiref.html
    module = Extension(MODULE,
                       define_macros = DEFINES,
                       include_dirs = INCLUDEDIRS,
                       libraries = LIBS,
                       library_dirs = LIBDIRS,
                       sources = SOURCES)

    setup(name = NAME,
          version = str(VERSION_MAJOR) + '.' + str(VERSION_MINOR),
          description = DESC,
          long_description = DESCRIPTION,
          author = AUTHOR,
          author_email = EMAIL,
          url = URL,
          ext_modules = [module])

if __name__ == '__main__':
    main()


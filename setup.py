from distutils.core import setup, Extension

NAME                    = 'bakery'
DESC                    = 'Game asset precompiler'
DESCRIPTION             = DESC
AUTHOR                  = 'Dave Kilian'
EMAIL                   = 'dave.kilian@gmail.com'
URL                     = 'http://github.com/fracturestudios/bakery'

MODULE                  = 'bakery'
VERSION_MAJOR           = 0
VERSION_MINOR           = 1

def main():
    setup(name = NAME,
          version = str(VERSION_MAJOR) + '.' + str(VERSION_MINOR),
          description = DESC,
          long_description = DESCRIPTION,
          author = AUTHOR,
          author_email = EMAIL,
          url = URL,
          packages = [ 'bakery', 'bakery.ext' ])

if __name__ == '__main__':
    main()


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

# TODO
# Build system currently works, and if you
# cd /Library/Python/2.7/site-packages
# you can import bakery.ext.test just fine.
# BUT the import fails if you're not in the right directory.
# This may not be a huge deal, because imp.load_dynamic() works as expected.
# Still is bothering me, however


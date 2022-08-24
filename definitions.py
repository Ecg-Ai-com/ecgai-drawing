# You can do this how Django does it: define a variable to the Project Root from a file that is in the top-level of
# the project. For example, if this is what your project structure looks like:
#
# project/
#     configuration.conf
#     definitions.py
#     main.py
#     utils.py
# In definitions.py you can define (this requires import os):
#
# ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root Thus, with the Project Root
# known, you can create a variable that points to the location of the configuration (this can be defined anywhere,
# but a logical place would be to put it in a location where constants are defined - e.g. definitions.py):
#
# CONFIG_PATH = os.path.join(ROOT_DIR, 'configuration.conf')  # requires `import os` Then, you can easily access the
# constant (in any of the other files) with the import statement (e.g. in utils.py): from definitions import
# CONFIG_PATH.
# https://stackoverflow.com/questions/25389095/python-get-path-of-root-project-structure/53465812
import pathlib

ROOT_DIR = pathlib.Path(__file__).parent.absolute()

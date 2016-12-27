#  _____ __ _____   _ __ _  _
# / _ \ V  V / _ \_| '_ \ || |
# \___/\_/\_/\___(_) .__/\_, |
#                  |_|   |__/
#
# UPLOAD EXAMPLES

# ############################################################

# If you don't want to pass your key each time,
# define it within the Client class.

>>> import owo
>>> my_client = owo.Client(API_KEY)

# Then the following methods can be changed to..

>>> my_client.upload_files("file.png", "file.py")

# The client also stores verbosity (default: False), which can be toggled using
# Client.toggle_verbose()
# Verbosity should be given using a kwarg to __init__, i.e.

>>> my_client = owo.Client(API_KEY, verbose=True)
>>> my_client.toggle_verbose()
>>> my_client.verbose
False

# ############################################################

# NON ASYNCHRONOUS EXAMPLES

# ############# #
# EXAMPLE INPUT #
# ############# #

# Import the wrapper in order to be used.
>>> import owo
# Specify which files **IN THE SAME FOLDER** that you would like to upload.
>>> owo.upload_files(API_KEY, "file.png", "file.py")

# ############## #
# EXAMPLE OUTPUT #
# ############## #

{"file.png": "url", "file.py": "url"}

# It is also possible to toggle verbosity
>>> owo.upload_files(API_KEY, "file.png", "file.py", verbose=True)

# ############## #
# EXAMPLE OUTPUT #
# ############## #

{
    'file.png': {'base domain 1': 'url 1', 'base domain 2': 'other url 1'},
    'file.py': {'base domain 1': 'url 2', 'base domain 2': 'other url 2'}
}

# ############################################################

# ASYNCHRONOUS EXAMPLES

# ############# #
# EXAMPLE INPUT #
# ############# #

>>> loop.run_until_complete(
...     owo.async_upload_files(API_KEY, "file.png", "file.py", loop=loop))
...

# ############## #
# EXAMPLE OUTPUT #
# ############## #

{"file.png": "url", "file.py": "url"}

# ############################################################

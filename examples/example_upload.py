#  _____ __ _____   _ __ _  _ 
# / _ \ V  V / _ \_| '_ \ || |
# \___/\_/\_/\___(_) .__/\_, |
#                  |_|   |__/ 
#
# UPLOAD EXAMPLES 

# ############################################################

# If you don't want to pass your key each time define it within the Client class.

>>> import owo
>>> my_client = owo.Client(API_KEY)

# Then the following methods can be changed to..

>>> my_client.upload_files("file.png", "file.py")

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

# ############################################################

# ASYNCHRONOUS EXAMPLES

# ############# #
# EXAMPLE INPUT #
# ############# #

>>> loop.run_until_complete(
...     owo.async_upload_files(API_KEY, "file.png", "file.py", loop=loop)
... )
...

# ############## #
# EXAMPLE OUTPUT #
# ############## #

{"file.png": "url", "file.py": "url"}

# ############################################################

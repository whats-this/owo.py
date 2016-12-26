#  _____ __ _____   _ __ _  _ 
# / _ \ V  V / _ \_| '_ \ || |
# \___/\_/\_/\___(_) .__/\_, |
#                  |_|   |__/ 
#
# SHORTEN EXAMPLES 

# ############################################################

# If you don't want to pass your key each time define it within the Client class.

>>> import owo
>>> my_client = owo.Client(API_KEY)

# Then the following methods can be changed to..

>>> my_client.shorten_urls("url1","url2")

<<<<<<< HEAD
=======
# The client also stores verbosity (default: False), which can be toggled using
# Client.toggle_verbose()
# Verbosity should be given using a kwarg to __init__, i.e.

>>> my_client = owo.Client(API_KEY, verbose=True)
>>> my_client.toggle_verbose()
>>> my_client.verbose
False

>>>>>>> origin/master
# ############################################################

# NON ASYNCHRONOUS EXAMPLES

# ############# #
# EXAMPLE INPUT #
# ############# #

# Import the wrapper in order to be used.
>>> import owo
# Specify which files **IN THE SAME FOLDER** that you would like to upload.
>>> owo.shorten_urls(API_KEY, "url1","url2")

# ############## #
# EXAMPLE OUTPUT #
# ############## #

["shortened url 1","shortened url 2"]

<<<<<<< HEAD
=======
# It is also possible to toggle verbosity
>>> owo.shorten_urls(API_KEY, "url1","url2", verbose=True)

# ############## #
# EXAMPLE OUTPUT #
# ############## #

[
	{'base domain 1': 'shortened url 1', 'base domain 2': 'other shortened url 1'},
	{'base domain 1': 'shortened url 2', 'base domain 2': 'other shortened url 2'}
]

>>>>>>> origin/master
# ############################################################

# ASYNCHRONOUS EXAMPLES

# ############# #
# EXAMPLE INPUT #
# ############# #

>>> import asyncio
>>> loop = asyncio.get_event_loop()
>>> my_client = owo.Client(API_KEY, loop=loop)
>>> loop.run_until_complete(
...     my_client.async_shorten_urls("url1","url2")
... )
...

# ############## #
# EXAMPLE OUTPUT #
# ############## #

["shortened url 1","shortened url 2"]

# ############################################################

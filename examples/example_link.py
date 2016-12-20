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

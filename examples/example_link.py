#  _____ __ _____   _ __ _  _
# / _ \ V  V / _ \_| '_ \ || |
# \___/\_/\_/\___(_) .__/\_, |
#                  |_|   |__/
#
# SHORTEN EXAMPLES

# ############################################################

# If you don't want to pass your key each time,
# define it within the Client class.

import owo

API_KEY = input("Please enter your API key: ")

url1 = "https://google.com"
url2 = "https://whats-th.is"
my_client = owo.Client(API_KEY)

# Then the following methods can be changed to..

my_client.shorten_urls(url1, url2)

# The client also stores verbosity (default: False), which can be toggled using
# Client.toggle_verbose()
# Verbosity should be given using a kwarg to __init__, i.e.

my_client = owo.Client(API_KEY, verbose=True)
my_client.toggle_verbose()
my_client.verbose  # False

# ############################################################

# NON ASYNCHRONOUS EXAMPLES

# Specify which urls you want to shorten.
owo.shorten_urls(API_KEY, url1, url2)

# Example output: ["shortened url 1", "shortened url 2"]

# It is also possible to toggle verbosity
owo.shorten_urls(API_KEY, url1, url2, verbose=True)

# Example output:
# [
#     {
#         'base domain 1': 'shortened url 1',
#         'base domain 2': 'other shortened url 1'
#     },
#     {
#         'base domain 1': 'shortened url 2',
#         'base domain 2': 'other shortened url 2'
#     }
# ]

# ############################################################

# ASYNCHRONOUS EXAMPLES

import asyncio

loop = asyncio.get_event_loop()
my_client = owo.Client(API_KEY, loop=loop)

loop.run_until_complete(
    my_client.async_shorten_urls(url1, url2))

# Example output: ["shortened url 1", "shortened url 2"]

# ############################################################

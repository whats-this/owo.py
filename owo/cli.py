#!/usr/bin/env python3.5

from __future__ import print_function

import argparse
import owo


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("key", help="Your API key")
    parser.add_argument("target", help="File to upload/URL to shorten")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", help="Return all domains",
                       action="store_true", default=False)
    group.add_argument("-u", "--url", help="Custom Base url", default=None)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--upload", help="Upload a file", action="store_true")
    group.add_argument("--shorten", help="Shorten a URL", action="store_true")

    args = parser.parse_args()

    get_verbose = args.verbose or args.url or False

    if args.upload:
        res = owo.upload_files(args.key, args.target, verbose=get_verbose)
        if args.url:
            print(res[args.target.lower()][args.url])
        else:
            print(res[args.target.lower()])

    elif args.shorten:
        res = owo.shorten_urls(args.key, args.target, verbose=get_verbose)
        if args.url:
            print(res[0][args.url])
        else:
            print(res[0])

    else:
        parser.error("Either --upload or --shorten should be given")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3.5

"""
owo.py background process
main use intended for mobile devices
usage: `$ owo-bg -p path -k API_KEY`
"""

import argparse
import owo
import os
import sys
import time
import shlex
import subprocess


def print_v(text):
    if args.verbose:
        print(text)


parser = argparse.ArgumentParser()
parser.add_argument("-k", "--key", help="API Key", required=True)

parser.add_argument("-p", "--path", help="Path to check file updates",
                    default="/sdcard/pictures/screenshots/")

parser.add_argument("-u", "--url", help="Base vanity url to use",
                    default="https://owo.whats-th.is/")

parser.add_argument("-v", "--verbose", help="Increase output verbosity",
                    action="store_true")

args = parser.parse_args()

sent_files = os.listdir(args.path)


def main():
    if not args.path.endswith("/"):
        args.path += "/"

    print("Starting background process...")
    while True:
        time.sleep(2)
        new_files = [f for f in os.listdir(args.path) if
                     f not in sent_files and os.path.isfile(args.path+f)]
        if new_files == []:
            continue
        for file in new_files:
            print_v("Found file: {}".format(file))
            try:
                urls = list(owo.upload_files(args.key, args.path+file,
                                             verbose=True).values())[0]

                url = urls.get(args.url)
                if url is None:
                    print("Vanity url base {} was not found, using default"
                          .format(args.url))
                    url = urls["https://owo.whats-th.is/"]

            except ValueError as e:
                print("Upload failed:\n{}".format(e.args[0]))

            except OverflowError:
                print("File too big: {}".format(file))
                sent_files.append(file)

            else:
                print_v("Upload successful.")
                sent_files.append(file)
                if (sys.executable ==
                        "/data/data/com.termux/files/usr/bin/python"):
                    # Mobile devices

                    try:
						# os.system won't raise an error
                        subprocess.run(
							shlex.split((
								"termux-notification "
								'--title "File uploaded" '
								'--content "{0}" '
								'--button1 "Copy link" '
								'--button1-action "termux-clipboard-set {0}" '
								'--button2 "Share" '
								'--button2-action "termux-share {0}" '
							).format(url))
						)
						
                        print_v("Sent notification")
                    except FileNotFoundError:
						# termux-api not installed
                        print("File uploaded: {}, URL: {}".format(
							file, url))
                else:
					# Non-mobile devices
                    print("File uploaded: {}, URL: {}".format(
						file, url))


if __name__ == "__main__":
    main()

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

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="Path to check file updates",
                    default="/sdcard/pictures/screenshots/")

parser.add_argument("-k", "--key", help="API Key", required=True)

parser.add_argument("-u", "--url", help="Base vanity url to use",
                    default="https://owo.whats-th.is/")

args = parser.parse_args()

sent_files = os.listdir(args.path)


def main():
    if not args.path.endswith("/"):
        args.path += "/"

    print("Starting backgroud process...")
    while True:
        time.sleep(2)
        new_files = [f for f in os.listdir(args.path) if
                     f not in sent_files and os.path.isfile(args.path+f)]
        if new_files == []:
            continue
        for file in new_files:
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
                sent_files.append(file)
                if (sys.executable ==
                        "/data/data/com.termux/files/usr/bin/python"):
                    # Mobile devices

                    try:
                        os.system("termux-notification -t \""
                                  "File uploaded\""
                                  " -c \"{0}\" -u \"{0}\"".format(
                                      url))

                        os.system("termux-clipboard-set {}".format(url))
                    except:
                        print("File uploaded: {}, URL: {}".format(
                                  file, url))
                else:
                    print("File uploaded: {}, URL: {}".format(
                              file, url))


if __name__ == "__main__":
    main()

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

from watchdog.observers.polling import PollingObserverVFS

from watchdog.events import FileSystemEventHandler

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="Path to check file updates",
                    default="/sdcard/pictures/screenshots")

parser.add_argument("-k", "--key", help="API Key", required=True)

parser.add_argument("-u", "--url", help="Base vanity url to use",
                    default="https://owo.whats-th.is/")

args = parser.parse_args()


class FileWatcher(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            if event.event_type == "created":
                try:
                    urls = list(owo.upload_files(args.key, event.src_path,
                                verbose=True).values())[0]

                    try:
                        url = urls[args.url]
                    except KeyError as e:
                        print("Vanity url base {} was not found, using default"
                              .format(e))
                        url = urls["https://owo.whats-th.is/"]

                except ValueError as e:
                    print("Upload failed:\n{}".format(e.args[0]))

                except OverflowError:
                    print("File too big: {}".format(event.src_path))

                else:
                    if (sys.executable ==
                            "/data/data/com.termux/files/usr/bin/python"):
                        # Mobile devices

                        try:
                            os.system("termux-notification -t \""
                                      "File uploaded, "
                                      "link copied to clipboard\""
                                      " -c \"{}\" -u \"{}\"".format(
                                        event.src_path, url))

                            os.system("termux-clipboard-set {}".format(url))
                        except:
                            print("File uploaded: {}, URL: {}".format(
                                event.src_path, url))
                    else:
                        print("File uploaded: {}, URL: {}".format(
                            event.src_path, url))


def main():
    observer = PollingObserverVFS(os.stat, os.listdir, .5)
    observer.schedule(FileWatcher(), path=args.path)
    observer.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()


if __name__ == "__main__":
    main()
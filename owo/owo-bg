# owo.py background process
# main use intended for mobile devices
# usage: `$ owo-bg -p path -k API_KEY`

import argparse
import owo
import os
import sys
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="Path to check file updates",
                    default="/sdcard/pictures/screenshots")
parser.add_argument("-k", "--key", help="API Key", required=True)

args = parser.parse_args()

files_sent = [f for f in os.listdir() if os.path.isfile(f)]  # Only send new files

print("Starting background task...")

while True:
    for file in [f for f in os.listdir() if os.path.isfile(f) and f not in files_sent]:

        if file not in files_sent:
            try:
                url = owo.upload_files(args.key, file)[0]

            except ValueError as e:
                print("Upload failed:\n{}".format(e.args[0]))

            except OverflowError:
                print("File too big: {}".format(file))
                files_sent.append(file)

            else:
                files_sent.append(file)
                if (sys.executable ==
                        "/data/data/com.termux/files/usr/bin/python"):
                    # Mobile devices

                    try:
                        subprocess.run("termux-notification -t File uploaded, "
                                       "link copied to clipboard\n"
                                       "-c {} -u {}".format(file, url)
                                                    .split(), shell=True)
                        subprocess.run("termux-clipboard-set {}".format(url)
                                       .split(), shell=True)
                    except:
                        print("File uploaded: {}, URL: {}".format(file, url))
                else:
                    print("File uploaded: {}, URL: {}".format(file, url))

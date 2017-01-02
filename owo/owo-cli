import argparse
import owo

parser = argparse.ArgumentParser()
parser.add_argument("key", help="Your API key")
parser.add_argument("target", help="File to upload/URL to shorten")
parser.add_argument("-v", "--verbose", help="Return all domains",
                    action="store_true", default=False)
group = parser.add_mutually_exclusive_group()
group.add_argument("--upload", help="Upload a file", action="store_true")
group.add_argument("--shorten", help="Shorten a URL", action="store_true")

args = parser.parse_args()

if args.upload:
    res = owo.upload_files(args.key, args.target, verbose=args.verbose)
    print(res[args.target])

elif args.shorten:
    res = owo.shorten_urls(args.key, args.target, verbose=args.verbose)
    print(res[0])

else:
    parser.error("Either --upload or --shorten should be given")

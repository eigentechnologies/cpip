import argparse
import json
import sys

from env_file import EnvFile

def get_package_urls():
    

# command line interface
parser = argparse.ArgumentParser(description='create conda lockfile from environment files.')
parser.add_argument('--list-explicit', '-l', required=True,
                    help="file containing the output of 'conda list --explicit'")
parser.add_argument('--env-export', '-e', required=True,
                    help="file containing the output of 'conda env export'")
parser.add_argument('--file', '-f', action='append',
                    help="environment file used to create the environment")
parser.add_argument('--temp-package', '-t', action='append',
                    help="temporary package to remove from the final environment")
args = parser.parse_args()

# package dependencies
tmp_pkgs = args.temp_package if args.temp_package else []
package_urls = get_package_urls(args.list_explicit)
pip_dependencies = EnvFile(args.env_export).pip_dependencies()

# file hashes
files = args.file if args.file else []
file_hashes = [EnvFile(f).hash() for f in files]

# dump in JSON format to stdout
metadata = {'platform': sys.platform, 'file_hashes': file_hashes, 'temp_packages': tmp_pkgs, 'package_urls': package_urls, 'pip': pip_dependencies}
json.dump(sys.stdout, metadata, indent=4, sort_keys=True)

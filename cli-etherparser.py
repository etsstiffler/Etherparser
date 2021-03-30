#  Copyright 2021 MAP2005
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import os
import sys
from os import path
import argparse
from modules.parser import Etherparser

def main():
    parser = argparse.ArgumentParser(description="Convert one ore more etherpad files into a readable format.")
    parser.add_argument("-l", "--log",
                        action="store_true",
                        default=True,
                        help="export the etherpad content in a log like format",
                        dest="export_log")
    parser.add_argument("-c", "--csv",
                        action="store_true",
                        default=False,
                        help="export the etherpad content in a csv format",
                        dest="export_csv")
    parser.add_argument("-u", "--author-list",
                        action="store_true",
                        default=False,
                        help="export the etherpad content as a list of the authors along with their contributions",
                        dest="export_author_list")
    parser.add_argument("-a", "--all",
                        action="store_true",
                        default=False,
                        help="export the etherpad content in all formats",
                        dest="export_all")
    parser.add_argument("--sep",
                        default=",",
                        help="the separator used for CSV files",
                        dest="separator")
    parser.add_argument("-o",
                        default=None,
                        type=str,
                        help="the output directory",
                        dest="output_dir")
    parser.add_argument("file",
                        nargs='+',
                        type=argparse.FileType('r'),
                        help="the etherpad files to parse")

    args = parser.parse_args()

    for file in args.file:
        if args.output_dir is not None:
            if not path.isdir(args.output_dir):
                try:
                    os.makedirs(args.output_dir)
                    output_dir = args.output_dir
                except FileExistsError:
                    parser.error(f"The file '{args.output_dir}' does already exist")
                    sys.exit(1)
            else:
                output_dir = args.output_dir
        else:
            output_dir = path.dirname(file.name)

        basename = "".join(path.basename(file.name).split('.')[:-1])
        etherparser = Etherparser.from_io(file)

        if args.export_log or args.export_all:
            etherparser.save_log(path.join(output_dir, basename + ".log"))
        if args.export_csv or args.export_all:
            etherparser.save_csv(path.join(output_dir, basename + ".csv"), args.separator)
        if args.export_author_list or args.export_all:
            etherparser.save_contributions(path.join(output_dir, basename + ".txt"))

if __name__ == "__main__":
    main()
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

import os as _os
from os import path as _path
import io as _io
import json as _json
from datetime import datetime as _datetime


class Changeset:
    """Represents a changeset in the etherpad file"""

    def __init__(self, author_id, content, timestamp):
        """init

        @param author_id: The ID of the author of this message
        @param content: The changeset including the operations
        @param timestamp: The timestamp as a `datetime.datetime` object
        """
        self.author_id = author_id
        self.content = content
        self.time = _datetime.fromtimestamp(timestamp)


class Etherparser:
    """Etherparser

    A class to parse the BBB Etherpad file. When instantiated, the object loads the etherpad data
    and extracts the author data and the complete changelog. It can read the data from a python
    dictionary, a json string or the etherpad file.
    It is also able to return the output in various formats, such as a log-like format or CSV.
    For better readability, it can output the changes sorted by the author.
    Instead of returning a string, it can write the output directly to a file.
    """

    def __init__(self, d: dict):
        """init

        Takes a python dictionary containing the data of the etherpad file as returned by `json.load`.
        To read the data from a json string or a file, see `Etherparser.from_string` and `Etherparser.from_file`.

        The author data is loaded and stored in `self.authors`. For details see `self.load_authors`.
        The change history is stored in `self.history`. See `self.load_history`.
        `self.max_author_name_length` contains the length of the longest author name.

        @param d: A dictionary containing the data from the etherpad file
        """
        self.d = d

        self.authors = self.load_authors()
        self.history = self.load_history()

        self.max_author_name_length = 0
        for name in self.authors.values():
            if len(name) > self.max_author_name_length:
                self.max_author_name_length = len(name)

    def load_authors(self) -> dict:
        """Loads the authors from `self.d`

        In the etherpad file, the authors are represented by a cryptic string, here called their ID.
        This method finds all declared authors in `self.d` and returns a dictionary with the IDs as keys
        and the real author names as values.

        As the result is stored in `self.authors`, this method should not be used.

        @return: A dictionary with the author IDs as keys and the author names as values
        """
        authors = {}
        for k, v in self.d.items():
            if k.startswith("globalAuthor"):
                authors.update({k.split(":")[-1]: self.d[k]["name"]})
        return authors

    def load_history(self) -> list:
        """Loads the change history from `self.d`

        For every change defined in the etherpad file, this method creates a `Changeset` object
        which contains the author ID, the changeset and a timestamp. See `Changeset`.
        It returns a list with all changeset objects.

        As the result is stored in `self.history`, this method should not be used.

        @return: A List containing changeset objects for every change made to the etherpad
        """
        history = []
        for key, value in self.d.items():
            # only changes
            if key.startswith("pad"):
                # get author
                try:
                    author = self.d[key]["meta"]["author"]
                    # the initial changeset should not be included
                    if not author:
                        continue
                except KeyError:
                    continue
                # get changeset
                try:
                    changeset = self.d[key]["changeset"]
                except KeyError:
                    continue
                # get timestamp
                try:
                    timestamp = self.d[key]["meta"]["timestamp"] / 1000
                except KeyError:
                    continue

                # append change to history
                history.append(Changeset(author, changeset, timestamp))
        return history

    def get_log(self, single_lines=False, only_insertions=False) -> str:
        """Returns the etherpad in a log-like format

        This method breaks the etherpad down and returns it as a log-like formatted conversation.
        With that, you get the changes in a chronological order, but there will be many singe characters
        and empty lines. At least empty output lines are be suppressed if `only_insertions` is True.

        The output may look like this:
        [25 Feb 2021 11:24:47] [   example author 1   ]: How did yo
        [25 Feb 2021 11:24:48] [   example author 1   ]: u learn code
        [25 Feb 2021 11:24:49] [   example author 1   ]:
        [25 Feb 2021 11:24:50] [   example author 1   ]: ing with python?
        [25 Feb 2021 11:24:57] [   example author 2   ]: J
        [25 Feb 2021 11:24:58] [   example author 2   ]: ust goo
        [25 Feb 2021 11:24:58] [   example author 2   ]: gle it

        [25 Feb 2021 11:25:11] [   example author 2   ]: https://www.python.org/about/gettingstarted/

        For better readability, have a look at `self.get_contributions`

        @param single_lines: Whether multi-line changes should be shown in only one line. Line feeds will be escaped
        @param only_insertions: Changes with no text will be stripped out
        @return: A log-like formatted conversation as a string
        """
        out = ""
        for changeset in self.history:
            time = changeset.time.strftime("%d %b %Y %H:%M:%S")
            author = self.authors[changeset.author_id]
            text = "".join(changeset.content.split('$')[1:])
            if single_lines:
                text = text.replace("\r", r"\r").replace("\n", r"\n")
            if only_insertions and not text:
                continue

            out += f"[{time}] [{author:^{self.max_author_name_length}}]: {text}\n"
        return out

    def get_csv(self, sep=',', only_insertions=False):
        """Returns the etherpad as a CSV format

        This method works similar to `self.get_log` except it uses the csv format.
        Line breaks in changes will be escaped. If `only_insertions` is True, changesets without text
        will be ignored. `sep` is the separator in the CSV format (default `,`).
        The separator may also occur in the changeset text (last column), it is not escaped.

        The output may look like this:
        25,2,2021,11,24,47,example author 1,How did yo
        25,2,2021,11,24,48,example author 1,u learn code
        25,2,2021,11,24,49,example author 1,
        25,2,2021,11,24,50,example author 1,ing with python?

        For better readability, have a look at `self.get_contributions`

        @param sep: The separator of the values
        @param only_insertions: Changes with no text will be stripped out
        @return: A CSV formatted string
        """
        out = ""
        for changeset in self.history:
            time = changeset.time

            author = self.authors[changeset.author_id]
            text = "".join(changeset.content.split('$')[1:]).replace("\r", r"\r").replace("\n", r"\n")
            if only_insertions and not text:
                continue

            out += f"{time.day}{sep}{time.month}{sep}{time.year}{sep}" \
                   f"{time.hour}{sep}{time.minute}{sep}{time.second}{sep}" \
                   f"{author}{sep}{text}\n"
        return out

    def get_contributions(self, indent="    "):
        """Returns every contribution separated by the author

        This method list all authors together with their contributions.
        The contributions are indented `indent` (default 4 spaces).
        The timestamps of the changes are dropped.

        The output may look like this:
        [example author 1]:
            How did you learn codeing with python?

        [example author 2]:
            Just google it
            https://www.python.org/about/gettingstarted/


        @param indent: The indent used for indentation
        @return: A list of authors and their contributions as a string
        """
        contributions = {author: "" for author in self.authors.keys()}
        # collect contributions of every author
        for changeset in self.history:
            try:
                contributions.update(
                    {
                        changeset.author_id: contributions[changeset.author_id] +
                                             "".join(changeset.content.split('$')[1:])
                    }
                )
            except KeyError:
                continue
        # convert to string
        out = ""
        for author_id, text in contributions.items():
            author = self.authors[author_id]
            out += f"[{author}]:\n{text}\\n\\n".replace("\n", "\n" + indent).replace(r"\n", "\n")
        return out

    def save_log(self, file: str, single_lines=False, only_insertions=False):
        """Saves the output of `self.get_log` to a file

        Calls `self.get_log` and writes the output to a file instead of returning it.
        For details see `self.get_log`.

        @param file: The path to the output file
        @param single_lines: Whether multi-line changes should be shown in only one line. Line feeds will be escaped
        @param only_insertions: Changes with no text will be stripped out
        """
        dirname = _path.dirname(file)
        if dirname:
            _os.makedirs(dirname, exist_ok=True)
        with open(file, "w") as f:
            f.write(self.get_log(single_lines=single_lines, only_insertions=only_insertions))

    def save_csv(self, file: str, sep=',', only_insertions=False):
        """Saves the output of `self.get_csv` to a file

        Calls `self.get_csv` and writes the output to a file instead of returning it.
        For details see `self.get_csv`.

        @param file: The path to the output file
        @param sep: The separator of the values
        @param only_insertions: Changes with no text will be stripped out
        """
        dirname = _path.dirname(file)
        if dirname:
            _os.makedirs(dirname, exist_ok=True)
        with open(file, "w") as f:
            f.write(self.get_csv(sep=sep, only_insertions=only_insertions))

    def save_contributions(self, file: str, indent="    "):
        """Saves the output of `self.get_contributions` to a file

        Calls `self.get_contributions` and writes the output to a file instead of returning it.
        For details see `self.get_contributions`.

        @param file: The path to the output file
        @param indent: The indent used for indentation
        """
        dirname = _path.dirname(file)
        if dirname:
            _os.makedirs(dirname, exist_ok=True)
        with open(file, "w") as f:
            f.write(self.get_contributions(indent=indent))

    @staticmethod
    def from_string(string: str):
        """Creates an Etherparser object from a string

        This is an alternate constructor. It takes a json string and returns an Etherparser object.

        @param string: The etherpad file as a json string
        @return: An Etherparser object
        """
        d = _json.loads(string)
        return Etherparser(d)

    @staticmethod
    def from_file(path: str):
        """Creates an Etherparser object from the etherpad file

        This is an alternate constructor. It takes the path of the etherpad file and returns an Etherparser object.

        @param path: The path to the etherpad file
        @return: An Etherparser object
        """
        with open(path) as f:
            d = _json.load(f)
        return Etherparser(d)

    @staticmethod
    def from_io(io: _io.TextIOWrapper):
        """Creates an Etherparser object from an opened file object

        This is an alternate constructor. It takes an opened file (TextIOWrapper) object
         as returned by the build-in function `open` and returns an Etherparser object.

        @param io: An TextIOWrapper object of the etherpad file
        @return: An Etherparser object
        """
        return Etherparser.from_string(io.read())

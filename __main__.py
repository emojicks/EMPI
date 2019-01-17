import json
import re


"""
{
    "library-name": {
        "version": 1.0,
        "description": ":joy:",
        "git-link": "http://something.com/some/thing.git"
    },
    "library-name2": {
        "version": 1.0,
        "description": ":joy:",
        "git-link": "https://something.com/some/thing.git"
    }
}
"""

URL_REGEX = re.compile(
    r"^"
    # protocol identifier
    r"(?:(?:https?|ftp)://)"
    # user:pass authentication
    r"(?:\S+(?::\S*)?@)?"
    r"(?:"
    # IP address exclusion
    # private & local networks
    r"(?!(?:10|127)(?:\.\d{1,3}){3})"
    r"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
    r"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
    # IP address dotted notation octets
    # excludes loopback network 0.0.0.0
    # excludes reserved space >= 224.0.0.0
    # excludes network & broadcast addresses
    # (first & last IP address of each class)
    r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
    r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
    r"|"
    # host name
    r"(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)"
    # domain name
    r"(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*"
    # TLD identifier
    r"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
    r")"
    # port number
    r"(?::\d{2,5})?"
    # resource path
    r"(?:/\S*)?"
    r"$"
    , re.UNICODE)  # Taken from https://github.com/insightindustry/validator-collection/


def get_library(name: str):

    with open('./libs.json') as f:
        libs = json.load(f)

        if name in libs.keys():
            return libs[name]

        return {}


def add_library(name: str, version: float, description: str, git_link: str):
    is_valid = URL_REGEX.match(git_link)

    if not is_valid:
        raise LookupError('Your link "{}" is not a valid URL.'.format(git_link))

    __libs = {}
    with open('./libs.json', 'r') as f:

        __libs = json.load(f)

        if not hasattr(__libs, name):

            __libs[name] = {'version': version, 'description': description, 'git-link': git_link}

    with open('./libs.json', 'w') as f:

        json.dump(__libs, f, indent=4)

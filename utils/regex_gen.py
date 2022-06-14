#!/usr/bin/env python3

import string
import sys

def main(major: str, minors: list):
    if minors:
        regex_string = f"""{{
    "begin": "({major})(?:(-)(?:({"|".join(minors)})|(\\\\S+)))?\\\\s+",
    "end": "\\\\S?(?=^@|^`@|^#)",
    "beginCaptures": {{
        "1": {{"name": "constant.language.major-token"}},
        "2": {{"name": "keyword.control.token-seperator"}},
        "3": {{"name": "constant.language.minor-token"}}
    }},
    "contentName": "string.unquoted.text",
    "patterns": [{{"include": "#macro-use"}}]
}},"""
    else:
        regex_string = f"""{{
    "begin": "({major})(?:(-)(?:\\\\S+))?\\\\s+",
    "end": "\\\\S?(?=^@|^`@|^#)",
    "beginCaptures": {{
        "1": {{"name": "constant.language.major-token"}},
        "2": {{"name": "keyword.control.token-seperator"}}
    }},
    "contentName": "string.unquoted.text",
    "patterns": [{{"include": "#macro-use"}}]
}},"""
    print(regex_string)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])



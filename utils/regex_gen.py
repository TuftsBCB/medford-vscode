#!/usr/bin/env python3

import sys
import os
from typing import Dict, List

from mfdls.medford_tokens import get_available_tokens

FILE_TOP = r"""{
    "scopeName": "source.mfd",
    "patterns": [
        {"include": "#metadata"},
        {"include": "#comment"},
        {"include": "#macro-def"}
    ],
    "repository": {
        "comment": {
            "name": "comment.line.number-sign.mfd",
            "match": "#.*$"
        },
        "metadata": {
            "begin": "(^@)",
            "end": "\\S?(?=^@|^`@|^#)",
            "beginCaptures": {
                "1": {"name": "keyword.control.metadata.mfd"}
            },
            "contentName": "meta.metadata.mfd",
            "patterns": [
"""

FILE_BOTTOM = r"""                {
                    "begin": "(?<=^@)(?:[^\\s-]+)(?:(-)(\\S+))?\\s+",
                    "end": "\\S?(?=^@|^`@|^#)",
                    "beginCaptures": {
                        "1": {"name": "keyword.control.token-seperator.mfd"}
                    },
                    "contentName": "string.unquoted.text.mfd",
                    "patterns": [
                        {"include": "#macro-use"},
                        {"include": "#latex"},
                        {"include": "#template"},
                        {"include": "#comment"}
                    ]
                }
            ]
        },
        "macro-def": {
            "begin": "(^`@)([^{\\s]+)\\s*",
            "end": "\\S?(?=^@|^`@|^#)",
            "beginCaptures": {
                "1": {"name": "keyword.control.macro"},
                "2": {"name": "support.variable.macro"}
            },
            "contentName": "entity.name.macro-body.mfd"

        },
        "macro-use": {
            "patterns": [
                {
                    "match": "(?<!^)(`@)([^{\\s]+)",
                    "captures": {
                        "1": {"name": "keyword.control.macro.mfd"},
                        "2": {"name": "support.variable.macro.mfd"}
                    }
                },
                {
                    "match": "(?<!^)(`@)({)([^}\\s]+)(})",
                    "captures": {
                        "1": {"name": "keyword.control.macro.mfd"},
                        "2": {"name": "punctuation.definition.macro-brace-begin.mfd"},
                        "3": {"name": "support.variable.macro.mfd"},
                        "4": {"name": "punctuation.definition.macro-brace-end.mfd"}
                    }
                }
            ]
        },
        "template": {
            "match": "\\[..\\]",
            "name": "invalid.illegal.template.mfd"
        },
        "latex": {
            "begin": "(\\$\\$)",
            "end": "(\\$\\$)",
            "beginCaptures": {"1": {"name": "keyword.control.beginlatex.mfd"}},
            "endCaptures": {"1": {"name": "keyword.control.endlatex.mfd"}},
            "contentName": "meta.latexblock.mfd",
            "patterns": [{"include": "text.tex.latex"}]
        }
    }
}
"""

def main(path: str):
    
    tokens: Dict[str, List[str]] = get_available_tokens()

    with open(path, "w") as f:
        f.write(FILE_TOP)
        for major, minors in tokens.items():
            f.write(generate_regex(major, minors))
        f.write(FILE_BOTTOM)


def generate_regex(major: str, minors: List[str]) -> str:
    if minors:
        regex_string = f"""                {{
                    "begin": "(?<=^@)({major})(?:(-)(?:({"|".join(minors)})|(\\\\S+)))?\\\\s+",
                    "end": "\\\\S?(?=^@|^`@|^#)",
                    "beginCaptures": {{
                        "1": {{"name": "constant.language.major-token"}},
                        "2": {{"name": "keyword.control.token-seperator"}},
                        "3": {{"name": "constant.language.minor-token"}}
                    }},
                    "contentName": "string.unquoted.text",
                    "patterns": [
                        {{"include": "#macro-use"}},
                        {{"include": "#latex"}},
                        {{"include": "#template"}}
                    ]
                }},
"""
    else:
        regex_string = f"""                {{
                    "begin": "(?<=^@)({major})(?:(-)(?:\\\\S+))?\\\\s+",
                    "end": "\\\\S?(?=^@|^`@|^#)",
                    "beginCaptures": {{
                        "1": {{"name": "constant.language.major-token"}},
                        "2": {{"name": "keyword.control.token-seperator"}}
                    }},
                    "contentName": "string.unquoted.text",
                    "patterns": [
                        {{"include": "#macro-use"}},
                        {{"include": "#latex"}},
                        {{"include": "#template"}}
                    ]
                }},
"""
    
    return regex_string

if __name__ == "__main__":
    main(sys.argv[1])



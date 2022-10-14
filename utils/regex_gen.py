#!/usr/bin/env python3

import sys
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

GENERIC_MAJOR = r"""                {
                    "begin": "(?<=^@)(?:[^\\s-]+)(?:(-)(\\S+))?\\s+",
                    "end": "\\S?(?=^@|^`@|^#)",
                    "beginCaptures": {
                        "1": {"name": "keyword.control.token-seperator.mfd"}
                    },
                    "contentName": "string.unquoted.text.mfd",
                    "patterns": [
                        {"include": "#major-desc"},
                        {"include": "#linking-token"},
                        {"include": "#~::minors"}
                    ]
                }
            ]
        },
"""


GENERIC_MINOR = r"""        "~::minors": {
            "begin": "(-)(?:(?:\\S+))?\\s+",
            "end": "\\S?(?=^@|^`@|^#)",
            "beginCaptures": {
                "1": {"name": "keyword.control.token-seperator"}
            },
            "contentName": "string.unquoted.text",
            "patterns": [
                {"include": "#data"}
            ]
        },
"""

FILE_BOTTOM = r"""        "major-desc": {
            "begin": "\\s+",
            "end": "\\S?(?=^@|^`@|^#)",
            "contentName": "string.unquoted.text",
            "patterns": [
                {"include": "#data"}
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
        },
        "data": {
            "patterns": [
                {"include": "#macro-use"},
                {"include": "#latex"},
                {"include": "#template"},
                {"include": "#comment"}
            ]
        }
    }
}
"""

def main(path: str):
    
    tokens: Dict[str, List[str]] = get_available_tokens()

    with open(path, "w") as f:
        f.write(FILE_TOP)
        for major in tokens.keys():
            f.write(generate_major(major))
        f.write(GENERIC_MAJOR)
        for major, minors in tokens.items():
            f.write(generate_minor(major, minors))
        f.write(GENERIC_MINOR)
        f.write(generate_linker(list(tokens.keys())))
        f.write(FILE_BOTTOM)


def generate_major(major: str) -> str:
    return f"""                {{
                    "begin": "(?<=^@)({major})",
                    "end": "\\\\S?(?=^@|^`@|^#)",
                    "beginCaptures": {{
                        "1": {{"name": "constant.language.major-token"}}
                    }},
                    "patterns": [
                        {{"include": "#major-desc"}},
                        {{"include": "#linking-token"}},
                        {{"include": "#{major}::minors"}}
                    ]
                }},
"""

def generate_minor(major: str, minors: List[str]) -> str:
    return f"""        "{major}::minors": {{
            "begin": "(-)(?:({"|".join(minors)})|(?:\\\\S+))?\\\\s+",
            "end": "\\\\S?(?=^@|^`@|^#)",
            "beginCaptures": {{
                "1": {{"name": "keyword.control.token-seperator"}},
                "2": {{"name": "constant.language.minor-token"}}
            }},
            "contentName": "string.unquoted.text",
            "patterns": [
                {{"include": "#data"}}
            ]
        }},
"""
def generate_linker(majors: List[str]) -> str:
    return f"""        "linking-token": {{
            "begin": "(-)(@)(?:({"|".join(majors)})|(\\\\S+))?\\\\s+",
            "end": "\\\\S?(?=^@|^`@|^#)",
            "beginCaptures": {{
                "1": {{"name": "keyword.control.token-seperator"}},
                "2": {{"name": "keyword.control.linking-token"}},
                "3": {{"name": "support.variable.linking-major"}}
            }},
            "contentName": "support.variable.linking-value",
            "patterns": [
                {{"include": "#data"}}
            ]
        }},
"""


if __name__ == "__main__":
    main(sys.argv[1])



from __future__ import division
from html.parser import HTMLParser

__author__ = "Giovanni Grano"
__license__ = "MIT"
__email__ = "grano@ifi.uzh.ch"

from typing import NamedTuple
from pathlib import Path

class ParserOutput(NamedTuple):
    total_mutants: int
    mutation_coverage: float
    line_coverage: float

class PitestHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._coverage_tag_index = 0
        self._coverage_tag_found = False
        self._total_mutants = None
        self._mutation_coverage = None
        self._line_coverage = None
    
    @classmethod
    def parse(cls, file: Path) -> ParserOutput:
        self = cls()
        self.feed(file.read_text())
        return ParserOutput(self._total_mutants, self._mutation_coverage, self._line_coverage)
    
    def handle_starttag(self, tag, attrs):
        if tag == "div" and dict(attrs).get('class', '').find("coverage_legend") != -1:
            self._coverage_tag_index += 1
            self._coverage_tag_found = True
    
    def handle_data(self, data: str):
        if self._coverage_tag_found:
            self._coverage_tag_found = False
            part, total = map(float, data.split('/'))
            if self._coverage_tag_index == 1:
                self._line_coverage = part / total if total > 0 else float("NaN")
            elif self._coverage_tag_index == 2:
                self._mutation_coverage = part / total if total > 0 else float("NaN")
                self._total_mutants = total


if __name__ == '__main__':
    test = PitestHTMLParser.parse("/Users/grano/Documents/PhD/mutation_tc_quality/scripts_mutation/"
                            "mutation_results/checkstyle/com.puppycrawl.tools.checkstyle.ant."
                            "CheckstyleAntTaskTest/201803080824/index.html")

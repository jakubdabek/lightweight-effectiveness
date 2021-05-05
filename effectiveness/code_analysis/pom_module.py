from __future__ import annotations

import fnmatch
import glob
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple


@dataclass
class PomModule:
    project_name: str
    name: str
    include_patterns: List[str]
    exclude_patterns: List[str]

    def __post_init__(self):
        self.include_patterns = [
            p.replace(".class", ".java") for p in self.include_patterns
        ]

    def find_cut_pairs(self, test_subdir: Path, src_subdir: Path) -> Iterable[CutPair]:
        tests = self.find_tests(test_subdir)
        return self.find_cuts(tests, src_subdir)

    def find_tests(self, test_subdir: Path) -> Iterable[Tuple[Path, str, str]]:
        excluded = {
            file
            for exclude in self.exclude_patterns
            for file in test_subdir.glob(exclude)
        }
        for include in self.include_patterns:
            for test_file in test_subdir.glob(include):
                if test_file not in excluded:
                    yield test_file, self.get_full_qualified_name(test_file), include

    def find_cuts(
        self, tests: Iterable[Tuple[Path, str, str]], src_subdir: Path
    ) -> Iterable[CutPair]:
        for test_path, test_qualified_name, include_pattern in tests:
            source_file_name = self.get_cut_name(test_path, include_pattern)
            for source_path in src_subdir.rglob(source_file_name):
                yield CutPair(
                    test_path,
                    test_qualified_name,
                    source_path,
                    self.get_full_qualified_name(source_path),
                )

    @staticmethod
    def get_cut_name(test_path: Path, include_pattern: str) -> str:
        """Returns the file name of the suspected class under test
        for a given test path and include pattern that found the test
        """
        # get only last part of the path
        include_pattern = include_pattern.rsplit('/', 1)[-1]

        known_patterns = {
            "*Test.java": (r"Test.java$", r".java"),
            "*Tests.java": (r"Tests.java$", r".java"),
            "Test*.java": (r"^Test", r""),
            "*TestCase.java": (r"TestCase.java$", r".java")
        }
        try:
            return re.sub(*known_patterns[include_pattern], test_path.name)
        except KeyError:
            print(f"* * * Unknown pattern: {include_pattern!r}")
            for sub in known_patterns.values():
                subbed = re.sub(*sub, test_path.name)
                if subbed != test_path.name:
                    return subbed

            # couldn't use any known patterns
            return test_path.name

    @staticmethod
    def get_full_qualified_name(path: Path) -> str:
        with open(path, encoding="utf8", errors='ignore') as f:
            for line in f:
                if line.startswith('package'):
                    package = line.replace('package', '').strip().strip(';')
                    name = path.stem
                    return f"{package}.{name}"


@dataclass
class CutPair:
    test_path: Path
    test_qualified_name: str
    source_path: Path
    source_qualified_name: str

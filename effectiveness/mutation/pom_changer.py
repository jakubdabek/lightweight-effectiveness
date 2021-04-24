import os
import sys
from pathlib import Path

from effectiveness.pom_utils import ET, POM_NSMAP, indent, obj_to_xml
from effectiveness.settings import PIT_VERSION


def pitest_plugin_element(class_to_mutate, test_to_run, mutator='ALL', threads=4) -> ET.Element:
    plugin = ET.Element('plugin')
    plugin_elements = {
        "groupId": "org.pitest",
        "artifactId": "pitest-maven",
        "version": PIT_VERSION,
        "configuration": {
            "failWhenNoMutations": "false",
            "targetClasses": dict(param=class_to_mutate),
            "targetTests": dict(param=test_to_run),
            "mutators": dict(mutator=mutator),
            "threads": threads,
            "avoidCallsTo": [
                dict(avoidCallsTo="java.util.logging"),
                dict(avoidCallsTo="org.apache.log4j"),
                dict(avoidCallsTo="org.slf4j"),
                dict(avoidCallsTo="org.apache.commons.logging"),
            ],
        },
    }

    return obj_to_xml(plugin, plugin_elements)


def add_pitest_plugin(
    pom: Path, target: Path, class_to_mutate: str, test_to_run: str, mutator='ALL'
):
    pom = ET.parse(pom)
    plugins = pom.find(".//pom:build//pom:plugins", POM_NSMAP)
    plugins.append(pitest_plugin_element(class_to_mutate, test_to_run, mutator))
    indent(pom, space=" " * 4)
    pom.write(target)


if __name__ == '__main__':
    original_pom, new_pom, class_to_mutate, test_to_run, operator = sys.argv[1:]
    add_pitest_plugin(original_pom, new_pom, class_to_mutate, test_to_run, operator)

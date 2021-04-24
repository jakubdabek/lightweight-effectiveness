from typing import Any, Dict, List, Union
from xml.etree import ElementTree as ET

POM_NAMESPACE = 'http://maven.apache.org/POM/4.0.0'
POM_NSMAP = {'pom': POM_NAMESPACE}
ET.register_namespace('', POM_NAMESPACE)


def obj_to_xml(top_level: ET.Element, obj: Union[Dict, List, Any]) -> ET.Element:
    if isinstance(obj, dict):
        for k, v in obj.items():
            obj_to_xml(ET.SubElement(top_level, k), v)
    elif isinstance(obj, list):
        for v in obj:
            obj_to_xml(top_level, v)
    else:
        top_level.text = str(obj)

    return top_level


# backport from python 3.9
def indent(tree: Union[ET.ElementTree, ET.Element], space="  ", level=0):
    """Indent an XML document by inserting newlines and indentation space
    after elements.

    *tree* is the ElementTree or Element to modify.  The (root) element
    itself will not be changed, but the tail text of all elements in its
    subtree will be adapted.

    *space* is the whitespace to insert for each indentation level, two
    space characters by default.

    *level* is the initial indentation level. Setting this to a higher
    value than 0 can be used for indenting subtrees that are more deeply
    nested inside of a document.
    """
    if isinstance(tree, ET.ElementTree):
        tree = tree.getroot()
    if level < 0:
        raise ValueError(f"Initial indentation level must be >= 0, got {level}")
    if not len(tree):
        return

    # Reduce the memory consumption by reusing indentation strings.
    indentations = ["\n" + level * space]

    def _indent_children(elem, level):
        # Start a new indentation level for the first child.
        child_level = level + 1
        try:
            child_indentation = indentations[child_level]
        except IndexError:
            child_indentation = indentations[level] + space
            indentations.append(child_indentation)

        if not elem.text or not elem.text.strip():
            elem.text = child_indentation

        for child in elem:
            if len(child):
                _indent_children(child, child_level)
            if not child.tail or not child.tail.strip():
                child.tail = child_indentation

        # Dedent after the last child by overwriting the previous indentation.
        if not child.tail.strip():
            child.tail = indentations[level]

    _indent_children(tree, 0)

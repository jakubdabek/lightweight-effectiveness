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

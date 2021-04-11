from effectiveness.settings import POM_NAMESPACE, POM_NSMAP

from xml.etree import ElementTree as ET

import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Union
from functools import partial

ET.register_namespace('', POM_NAMESPACE)


def get_projects(path: Path):
    return pd.read_csv(path)['project'].unique().str.split("/").str[1]


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

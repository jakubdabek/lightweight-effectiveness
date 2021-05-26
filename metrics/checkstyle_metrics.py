import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

from effectiveness.pom_utils import POM_NSMAP, obj_to_xml, indent
from metrics.settings import CHECKSTYLE_PLUGIN_VERSION

REPORT_DIRECTORY = "target/site"


def calculate_metrics(project: str):
    project_directory = Path.cwd() / "projects" / project
    report_directory = project_directory / REPORT_DIRECTORY
    configuration_file_name = "checkstyle.xml"

    # Adding configuration file "checkstyle.xml"
    create_configuration_file(project_directory, configuration_file_name)

    # Caching original pom
    pom = project_directory / "pom.xml"
    cached_pom = pom.with_name("~pom_cached.xml")
    try:
        shutil.copy2(pom, cached_pom)

        # Add plugin to pom.xml
        add_checkstyle_plugin(cached_pom, pom, configuration_file_name)

        subprocess.run(
            ["mvn", "site"],
            cwd=project_directory,
            shell=True,
            # timeout=settings.MUTATION_TIMEOUT,
            # check=True,
        )

        # Do something with results
        print("Calculating results")

    finally:
        # Restoring pom.xml
        pom.unlink()
        cached_pom.rename(pom)


def create_configuration_file(project_directory: Path, configuration_file_name: str):
    root = Element("module")
    root.set("name", "Checker")

    module_JavadocPackage = SubElement(root, "module")
    module_JavadocPackage.set("name", "JavadocPackage")

    module_TreeWalker = SubElement(root, "module")
    module_TreeWalker.set("name", "TreeWalker")

    # Metrics modules
    m1 = SubElement(module_TreeWalker, "module")
    m1.set("name", "BooleanExpressionComplexity")

    m2 = SubElement(module_TreeWalker, "module")
    m2.set("name", "ClassDataAbstractionCoupling")

    m3 = SubElement(module_TreeWalker, "module")
    m3.set("name", "ClassFanOutComplexity")

    m4 = SubElement(module_TreeWalker, "module")
    m4.set("name", "CyclomaticComplexity")

    m5 = SubElement(module_TreeWalker, "module")
    m5.set("name", "JavaNCSS")

    m6 = SubElement(module_TreeWalker, "module")
    m6.set("name", "NPathComplexity")

    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")

    configuration_file = open(project_directory / configuration_file_name, "w+")
    configuration_file.write("<!DOCTYPE module PUBLIC \"-//Puppy Crawl//DTD Check Configuration 1.3//EN\" "
                             "\"http://www.puppycrawl.com/dtds/configuration_1_3.dtd\">")
    configuration_file.write(xml_str.split("\n", 1)[1])
    configuration_file.close()


def add_checkstyle_plugin(pom: Path, target: Path, configuration_file_name: str):
    pom = ET.parse(pom)
    root = pom.getroot()
    plugins_element = pom.find("./pom:reporting/pom:plugins", POM_NSMAP)

    # Utworzenie węzłów reporting/plugins, jeśli nie istnieją
    if plugins_element is None:
        reporting_element = SubElement(root, "reporting")
        plugins_element = SubElement(reporting_element, "plugins")

    # Dodanie pluginu
    plugins_element.append(checkstyle_plugin_element(configuration_file_name))
    indent(pom, space=" " * 4)
    pom.write(target)


def checkstyle_plugin_element(config_location: str) -> Element:
    plugin = Element('plugin')
    plugin_elements = {
        "groupId": "org.apache.maven.plugins",
        "artifactId": "maven-checkstyle-plugin",
        "version": CHECKSTYLE_PLUGIN_VERSION,
        "configuration": {
            "configLocation": config_location
        }
    }
    return obj_to_xml(plugin, plugin_elements)

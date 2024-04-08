from utility.xml.compair_xml_files import CompairXmlFile
import CONSTS

added_key, removed_key, difference, commen  = CompairXmlFile().operation(
    CONSTS.ROOT_DIR + r'\xml_test.xml', CONSTS.ROOT_DIR + r'\xml_test_0.xml')

newline = '\n\n\n\n'
print(f"added_key: {added_key}{newline}removed_key:{removed_key}{newline}difference:{difference}{newline}commen: {commen}{newline}")

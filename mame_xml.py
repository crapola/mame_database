"""
XML loader.
"""
import configparser
import pathlib
import zipfile
from xml.etree import ElementTree

from machine import Machine


def element_text(elm:ElementTree.Element|None)->str:
	""" Get element text filed or empty string. """
	return elm.text if elm is not None and elm.text else ""

def load_machine_list(xml_path:str)->list[Machine]:
	""" Load machine list from .xml file. """
	print(f"Loading {xml_path} …")
	xml_input=xml_path
	if pathlib.Path(xml_path).suffix==".zip":
		z:zipfile.ZipFile=zipfile.ZipFile(xml_path)
		xml_input=z.open(z.infolist()[0])
	tree=ElementTree.parse(xml_input)
	machine_list=[]
	root=tree.getroot()
	for node in root:
		name:str=node.get("name") or ""
		source:str=node.get("sourcefile") or ""
		description:str=element_text(node.find("description"))
		year:str=element_text(node.find("year"))
		manufacturer:str=element_text(node.find("manufacturer"))
		parent:str=node.get("cloneof") or ""
		machine:Machine=Machine(name,source,description,year,manufacturer,parent,"category")
		machine_list.append(machine)
	return machine_list

def apply_categories(machines:list[Machine],catver_file:str)->None:
	"""
	Mutate the machines list to set category members according to catver.ini.
	"""
	config=configparser.ConfigParser(allow_no_value=True)
	config.read(catver_file)
	for m in machines:
		key:str=m.name
		try:
			m.category=config["Category"][key]
		except KeyError:
			pass

import configparser
from xml.etree import ElementTree

from machine import Machine


def element_text(elm:ElementTree.Element|None)->str:
	return elm.text if elm!=None and elm.text else "?"

# Some years are strings like "198?".
def element_year(elm:ElementTree.Element|None)->int:
	integer:int
	try:
		integer=int(elm.text) if elm!=None and elm.text else 0
	except ValueError:
		integer=0
	return integer

def load_machine_list(xml_path:str)->list[Machine]:
	print(f"Loading {xml_path} …")
	tree=ElementTree.parse(xml_path)
	machine_list=[]
	root=tree.getroot()
	for node in root:
		name:str=node.get("name") or "?"
		source:str=node.get("sourcefile") or "?"
		description:str=element_text(node.find("description"))
		year:int=element_year(node.find("year"))
		manufacturer:str=element_text(node.find("manufacturer"))
		parent:str|None=node.get("cloneof")
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
		key=m.name
		try:
			m.category=config["Category"][key]
		except KeyError:
			pass
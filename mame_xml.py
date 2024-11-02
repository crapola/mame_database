"""
XML loader.
"""
import configparser
import pathlib
import zipfile
from xml.etree import ElementTree


def element_text(elm:ElementTree.Element|None)->str:
	""" Get element text filed or empty string. """
	return elm.text if elm is not None and elm.text else ""

def load_machine_list(xml_path:str,columns:tuple[str,...])->list[dict]:
	"""
	Load machine list from .xml file.
	xml_path: Path to .xml or .zip file.
	filter: List of attributes and elements we want for each machine.
	"""
	print(f"Loading {xml_path} …")
	xml_input=xml_path
	if pathlib.Path(xml_path).suffix==".zip":
		z:zipfile.ZipFile=zipfile.ZipFile(xml_path)
		xml_input=z.open(z.infolist()[0])
	root=ElementTree.parse(xml_input).getroot()
	def get_machine_dict(elem:ElementTree.Element)->dict:
		""" Collate XML 'machine' element attribs and subnodes texts in a dict. """
		return elem.attrib|{x.tag:x.text for x in elem}
	dl=(get_machine_dict(x) for x in root)
	d=[{k:x.get(k) or '' for k in columns} for x in dl]
	return d


def apply_categories(machines:list[dict],catver_file:str)->None:
	"""
	Mutate the machines list to set category members according to catver.ini.
	"""
	config=configparser.ConfigParser(allow_no_value=True)
	config.read(catver_file)
	for i,_ in enumerate(machines):
		try:
			machines[i]["category"]=config["Category"][machines[i]["name"]]
		except KeyError:
			pass

"""
Convert part of MAME XML info to SQLite.
"""
import pathlib
import sys

import database
import mame_xml


def main()->None:
	""" Entry point. """
	args:list[str]=sys.argv[1:]
	if not args:
		print("Missing parameters.")
		print("Usage:\npython mame_database <xml> [<catver>]")
		print("<xml>: Path to .xml, or .zip containing the .xml.")
		print("<catver>: Optional path to catver.ini.")
		sys.exit(-1)
	xml_path:str=args[0]
	ini_path:str=args[1] if len(args)>1 else ""
	columns:tuple[str,...]=("name","romof","sourcefile","description","year","manufacturer","category")
	machines:list[dict]=mame_xml.load_machine_list(xml_path,columns)
	if ini_path:
		print("Adding categories from",ini_path)
		mame_xml.apply_categories(machines,ini_path)
	output_path:str=str(pathlib.Path(xml_path).parent.joinpath("mame_sqlite.db"))
	database.build_database(machines,output_path,columns)
	print(f"Created {output_path} for {len(machines)} machines.")

if __name__=="__main__":
	main()

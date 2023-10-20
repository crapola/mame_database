import sys

import database
import mame_xml


def main():
	try:
		xml_path,ini_path=sys.argv[1:]
	except ValueError:
		print("Missing parameters.")
		print("Usage:\npython mame_database path/to/mame####.xml path/to/catver.ini")
		exit(-1)
		return
	machines=mame_xml.load_machine_list(xml_path)
	mame_xml.apply_categories(machines,ini_path)
	database.build_database(machines)
	print(f"Created database mame_roms.db for {len(machines)} machines.")

if __name__=="__main__":
	main()
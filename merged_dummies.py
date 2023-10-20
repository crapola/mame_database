# This script creates the 0 bytes dummy files clones for a merged rom.
# Usage:
# python merged_dummy.py <path to a rom archive>
import os
import sys
import zipfile


def list_directories_in_zip(zip_path:str)->list[str]:
	with zipfile.ZipFile(zip_path,"r") as zip_ref:
		all_files:list[str]=zip_ref.namelist()
		directories:list[str]=[os.path.dirname(file) for file in all_files if os.path.dirname(file)]
		directories=sorted(tuple(set(directories)))
		return directories

def create_dummy_roms_from_merged(path:str)->None:
	directories:list[str]=list_directories_in_zip(path)
	target_dir:str=os.path.dirname(path)+"/"+os.path.splitext(os.path.basename(path))[0]+"_clones/"
	if not os.path.exists(target_dir):
		os.makedirs(target_dir)
	for d in directories:
		target:str=target_dir+d+".zip"
		print(target)
		with open(target,"wb"):
			pass

def main():
	path:str=sys.argv[1]
	create_dummy_roms_from_merged(path)

if __name__=="__main__":
	main()
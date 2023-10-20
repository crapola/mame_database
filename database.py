import sqlite3 as sq

from machine import Machine


def build_database(machine_list:list[Machine],path:str="mame_roms.db")->None:
	"""
	Create or overwrite the database.
	"""

	# Create tables.
	machine_fields=Machine.fields()
	rom_columns_types="TEXT PRIMARY KEY","TEXT","TEXT","INT","TEXT","TEXT","TEXT"
	rom_columns=",".join([" ".join((a,b)) for a,b in zip(machine_fields,rom_columns_types)])
	sql=f"""
	PRAGMA foreign_keys=OFF;
	CREATE TABLE rom({rom_columns},FOREIGN KEY(parent) REFERENCES rom(name));
	"""

	# Insert rows.
	values:list[str]=[]
	for m in machine_list:
		parent=f'"{m.parent}"' if m.parent!=None else "Null"
		m.description=m.description.replace('"','""')
		m.manufacturer=m.manufacturer.replace('"','""')
		value=f'("{m.name}", "{m.source}", "{m.description}", {m.year}, "{m.manufacturer}",{parent} ,"{m.category}" )'
		values.append(value)
	insert_command=f"""INSERT INTO rom VALUES {','.join(values)};"""
	sql+=insert_command
	sql+="PRAGMA foreign_keys=ON;"

	# Execute.
	con:sq.Connection=sq.connect(path)
	cur:sq.Cursor=con.cursor()
	cur.execute("DROP TABLE IF EXISTS rom")
	try:
		cur.executescript(sql)
	except sq.OperationalError as e:
		print("OperationalError:" ,e)
		with open("errors.log","wt",encoding="utf-8") as log:
			log.write(sql)
		exit(-1)
	con.commit()

	# Check constraints.
	cur.execute("PRAGMA foreign_key_check")
	results=cur.fetchall()
	for table, rowid, _,_  in results:
		cur.execute(f"SELECT * FROM {table} WHERE rowid = ?", (rowid,))
		row = cur.fetchone()
		print(f"Warning: unknown parent for clone: {table}: {row}")
	con.close()
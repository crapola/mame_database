"""
SQLite database builder.
"""
import sqlite3 as sq


def build_database(machine_list:list[dict],path:str,columns:tuple[str,...])->None:
	"""
	Create or overwrite the database.
	"""

	# Convert machine dicts to lists of strings in column order.
	machines:list=[sorted(d.items(),key=lambda x:columns.index(x[0])) for d in machine_list]
	machines=[list(zip(*x))[1] for x in machines]

	# Create tables.
	rom_columns_types:tuple=("TEXT PRIMARY KEY",*("TEXT",)*6)
	rom_columns:str=",".join([" ".join((a,b)) for a,b in zip(columns,rom_columns_types)])
	sql:str=f"""
	PRAGMA foreign_keys=OFF;
	CREATE TABLE rom({rom_columns},FOREIGN KEY(romof) REFERENCES rom(name));
	"""

	# Insert rows.
	values:list[str]=[]
	for m in machines:
		escaped:list[str]=["'"+x.replace("'",'"').replace('"','"')+"'" for x in m]
		value:str="("+",".join(escaped)+")"
		values.append(value)
	insert_command:str=f"""INSERT INTO rom VALUES {','.join(values)};"""
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
	# cur.execute("PRAGMA foreign_key_check")
	# results=cur.fetchall()
	# for table, rowid, _,_  in results:
	# 	cur.execute(f"SELECT * FROM {table} WHERE rowid = ?", (rowid,))
	# 	row = cur.fetchone()
	# 	print(f"Warning: unknown parent for clone: {table}: {row}")
	# con.close()

from datetime import datetime
import sys
import argparse
import sqlite3 as sql
import beerGUI as gui

#exe generator command:
#pyinstaller --noconfirm --onedir --windowed --collect-data TKinterModernThemes --name "Beer" --add-data 
#"C:\Users\samdaskod\Desktop\beer\exetest\beerGUI.py;." --add-data "C:\Users\samdaskod\Desktop\beer\exetest\beerGraph.py;." 
# --add-data "C:\Users\samdaskod\Desktop\beer\exetest\beerStatisticTest.db;."  "C:\Users\samdaskod\Desktop\beer\exetest\beerStatistic.py"

year = datetime.today().year - 1
con = sql.connect("beerStatistic.db")
cur = con.cursor()


def main(args):
	name = args.name
	brand = args.brand
	'''
	Upsert Drinkers
	'''
	if name != "" and name != " ":
		upsertDrinker(con, cur, name, year)

	'''
	Upsert Brands
	'''
	upsertBrand(con, cur, brand, year)

	con.close()


def upsertBrand(con, cur, brand, year):
	"""
	Updates brands or adds new one
	"""
	#Make records for new year (Brand, 20XX, 0)
	nextYear = cur.execute("select distinct year from beers where year = ?", (year,))
	if nextYear.fetchone() is None:
		brandsList = cur.execute("select distinct brand from beers")
		brands = brandsList.fetchall()
		for b in brands:
			cur.execute("insert into beers values (?,?,?)", (b[0], year, 0))
			con.commit()

	cur.execute("select beerCount from beers where brand = ? and year = ?", (brand, year))
	beerCount = cur.fetchone()

	# Does this Name already exist?
	if beerCount is not None:
		count = beerCount[0] + 1

		cur.execute("update beers set beerCount = ? where brand = ? and year = ?", (count, brand, year,))
		con.commit()

		print(f"Update {brand}, Count: {count}")

	else:
		count = 1
		n = 2016
		record = []
		while n <= year:
			if n != year:
				record.append((brand, n, 0))
			else:
				record.append((brand, n, count))
			n += 1

		cur.executemany("insert into beers values (?,?,?)", record)
		con.commit()

		print(f"Insert {brand}, Count: {count}")


def upsertDrinker(con, cur, name, year):
	"""
	Updates drinker or adds new one
	"""
	#Make records for new year (Name, 20XX, 0)
	nextYear = cur.execute("select distinct year from names where year = ?", (year,))
	if nextYear.fetchone() is None:
		namesList = cur.execute("select distinct name from names")
		names = namesList.fetchall()
		for x in names:
			cur.execute("insert into names values (?,?,?)", (x[0], year, 0))
			con.commit()

	cur.execute("select nameCount from names where name = ? and year = ?", (name, year))
	nameCount = cur.fetchone()

	# Does this Name already exist?
	if nameCount is not None:
		count = nameCount[0] + 1
		cur.execute("update names set nameCount = ? where name = ? and year = ?", (count, name, year,))
		con.commit()

		print(f"Update {name}, Count: {count}")

	else:
		count = 1
		n = 2016
		record = []
		while n <= year:
			if n != year:
				record.append((name, n, 0))
			else:
				record.append((name, n, count))
			n += 1
		cur.executemany("insert into names values (?,?,?)", record)
		con.commit()

		print(f"Insert {name}, Count: {count}")


def argumentParser() -> argparse.Namespace:
	"""
	Returns the argparse Namespace object of the main program, to be able to manipulate it easily
	"""
	parser = argparse.ArgumentParser(
		description="beer statistic")
	parser.add_argument("-b", "--brand", help="beer brand", dest="brand")
	parser.add_argument("-n", "--name", help="name of the beer poster", dest="name")
	parser.add_argument("-gui", "--gui", action="store_true",
	                    help="Opens the GUI instead of starting through the command line")

	return parser.parse_args()


if __name__ == "__main__":
	args = argumentParser()
	if args.gui or not len(sys.argv) > 1:
		gui.beerGUI(cur, year)
	else:
		main(args)

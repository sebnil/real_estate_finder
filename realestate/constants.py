import os

script_location_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

output_xlsx_path = os.path.abspath(script_location_path + '/../webapp/static/')

database_path = os.path.abspath(script_location_path + '/../temp/realestate.db')
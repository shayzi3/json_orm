
from typing import Any, Iterable
from jpy.utils.enums import Mode
from jpy.utils.exception import (
     TableNotExists,
     TableColumnNotExists,
     RequiredArgument,
     PrimaryNotExists,
     JsonFileEmpty
)





def valide_input_data(
     data: Iterable,
     json_file: dict[str, Any],
     table_name: str,
     free: bool,
     primary: str,
     mode: Mode | None = None
) -> bool:
     if not json_file:
          raise JsonFileEmpty(f"Json file empty.")
     
     # Table not exists
     if table_name not in json_file.keys():   
          raise TableNotExists(f"Table {table_name} not exists.")
        
     if free:
          types = []
          for type_ in json_file[table_name].keys():
               if type_ not in ['__types', 'data']:
                    types.append(type_)
     else:
          types = json_file[table_name]['__types']
        
     if not free:
          if primary and primary not in types:
               raise PrimaryNotExists(f"Primary key {primary} in table {table_name} not exists.")

          if mode == Mode.INSERT:
               for key in types: 
                    if key not in data.keys(): # Пропущенный аргумент
                         raise RequiredArgument(f"Missed column {key} for table {table_name}.")
               
     for key in data:
          if key not in types:  # Несуществующий аргумент
               raise TableColumnNotExists(f"Table {table_name} dont have column {key}.")
     return True
from enum import Enum
class DbTypes(str, Enum):
    SQL = 'sql'
    noSQL = 'nosql'
    Graph = 'graph'
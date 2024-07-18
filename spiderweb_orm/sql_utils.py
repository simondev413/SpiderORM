"""

"""
from spiderweb_orm.fields import *


class SQLTypeGenerator:
    
    @staticmethod
    def get_sql_type(field):
        field_type_map = {
            'CharField':lambda field: f"VARCHAR({field.max_length})",
            'IntegerField':lambda field:f"INTEGER",
            'DecimalField':lambda field:f"DECIMAL",
            'FloatField':lambda field:f"FLOAT",
            'BooleanField':lambda field:f"BOOLEAN",
            'DateField':lambda field:f"DATE",
            'DateTimeField':lambda field:f"DATETIME",
            'ChoiceField':lambda field:f"VARCHAR({field.max_length})",
            'ImageField':lambda field:f"VARCHAR(255)",
            'FileField':lambda field:f"VARCHAR(255)",
            'URLField':lambda field:f"VARCHAR(255)",
            'ForeignKey':lambda field:f"INTEGER REFERENCES {field.to.__name__.lower()}(id)",
            'TextField':lambda field:f"TEXT",
        }

        field_class_name = field.__class__.__name__
        if field_class_name in field_type_map:
            return field_type_map[field_class_name](field)
        else:
            raise TypeError(f"Unknown field type: {type(field)}")


class TableSQL:

    @staticmethod
    def create_table_sql(cls):
        fields_definitions = []
        for field_name, field in cls._fields.items():
            field_def = f"{field_name} {SQLTypeGenerator.get_sql_type(field)}"
            if field.primary_key:
                field_def += ' PRIMARY KEY'
            if getattr(field,'auto_increment',False):
                field_def += ' AUTOINCREMENT'
            if not field.null:
                field_def += ' NOT NULL'
            if field.unique:
                field_def += ' UNIQUE'
            if field.default:
                field_def += f" DEFAULT {repr(field.default)}"

            fields_definitions.append(field_def)
        fields_sql = ",".join(fields_definitions)
        return f"CREATE TABLE IF NOT EXISTS {cls.__name__.lower()} ({fields_sql});"
    
    @staticmethod
    def insert_data_sql(cls):
        value = None  
        fields = []                
        values = []
        for field, field_class in cls._fields.items():                            
            if hasattr(field_class,'auto_increment'): 
                if not field_class.auto_increment:
                    fields.append(field)     
                    value = getattr(cls,field)                     
            else:
                fields.append(field)
                value = getattr(cls,field)                  
            if field_class.default is not None and value == field_class:
                value = field_class.default
            
            if value:
                values.append(value)                    
                 
        placeholders = ",".join(["?" for _ in fields])
        columns = ",".join(fields)        
        return  f"INSERT INTO {cls.__class__.__name__.lower()} ({columns}) VALUES ({placeholders});",values
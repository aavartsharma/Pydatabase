from sqlmodel import SQLModel, create_engine, Session, Field as field, select
from pydantic import create_model
from typing import Optional, get_type_hints as typehit
from sqlalchemy.schema import CreateTable
from sqlalchemy import inspect, Select

# print(Createtable(helo.__table__))

sqlitedb = "sqlite:///test1.db"
engine = create_engine(sqlitedb, echo=True)
inspector = inspect(engine)

class book():
    id: Optional[int] = field(default=None, primary_key=True)
    name: str


# print(book.__dict__)
# print(book.__name__)

class person(SQLModel, table= True):
    id: Optional[int] = field(default=None, primary_key=True)
    name: str
    secret_name: str
#send class via dict    {book.__name__ : book.__dict__}

class gun(SQLModel, table=True):
    id: Optional[int] = field(default=None, primary_key=True)
    name:str
    dmg:int

class testting():
    id: Optional[int] = field(primary_key=True)
    name: str
    asdfsd:str
    sdfsd: str




meta= type(SQLModel)
a = dict(testting.__dict__)
print(("-"*20))
# print(gun.__dict__)

a.update({"__tablename__": "User"})
print(a)
with Session(engine) as session:
    # session.add(person(name='aavart', secret_name= 'world best computer sciencist'))
    # session.commit()
    # statement = select(person).where(person.name == "aavart")
    # print(type(statement))
    # print(statement.__dict__)
    # persons = session.exec(statement).all()
    # for i in persons:
    #     session.delete(i)
    #     session.commit()

    # # print(persons[0].__dict__)
    # print(gun.__table__)
    # print(inspector.get_columns("gun"))
    # pass

    # print("gun dict: ",gun.__dict__)
    User = meta(
        "User",                          # class name
        (SQLModel,object),  
        a,
        table=True                 # base classes
    )
    User.__dict__

    def create_dynamic_model(class_name: str, fields: dict):
        annotations = {}
        attrs = {"__annotations__": annotations, "__tablename__": class_name.lower()}

        for field_name, (field_type, field_options) in fields.items():
            annotations[field_name] = field_type
            attrs[field_name] = field(**field_options) if field_options else ...

        return type(class_name, (SQLModel,), attrs,table=True)


    # Example: define fields dynamically
    user = create_dynamic_model(
        "user",
        {
            "id": (Optional[int], {"default": None, "primary_key": True}),
            "name": (str, {}),
            "dmg": (int, {}),
        }
    )

    # print(user.__annotations__)

    # test1 = create_model(
    #     "test1",
    #     __base__=SQLModel,
    #     __tablename__="test1",
    # )

    # Dynamically create the model
    test1 = create_model(
        "test1",
        __base__=SQLModel,
        __tablename__='test1',
        __cls_kwargs__={"table": True},
        id=(Optional[int], field(default=None, primary_key=True)),
        name=(str, field()),
        dmg=(int, field())
    )

    # print(test1.__dict__){id:(Optine[int])}

    class d():
        id: Optional[int]
        new: int
        name:str

    def create_tables_client(class_):
        return class_.__dict__
    print(create_tables_client(d))
    print(d.__dict__)
    SQLModel.metadata.create_all(engine)
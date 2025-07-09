from database import PyDatabase

def a(**I):
  print(I)
  print(f"{",".join([i for i in I])}")

a(a='1',b="1",c="1",d="1")

a: PyDatabase.status = PyDatabase.status.failed
b: PyDatabase.status = PyDatabase.status.success

print(PyDatabase.status.success is  a)
print(PyDatabase.status.success is b)
print(a != PyDatabase.status.success)


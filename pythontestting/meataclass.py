class StaticMethodMeta(type):
    def __new__(cls, name, bases, dct):
        new_dct = {}
        for key, value in dct.items():
            if callable(value) and not key.startswith('__'):
                value = staticmethod(value)
            new_dct[key] = value
        return super().__new__(cls, name, bases, new_dct)
    
class printe(type):
    def __new__(cls,name,bases,dct):
        print(cls)
        print(name)
        print(bases)
        print(dct)
        print(super().__new__(cls,"thisisanewanmegiven",bases,dct))
        return super().__new__(cls,"afsdfs",bases,dct)
    
    def adsf(a):
        print(a)
    
class prent(metaclass = printe): pass
class childobject(prent,metaclass = printe):
    def __init__(self):
        self.numberluck = 45
        pass

    def aaga():
        return 445


print(childobject().numberluck)
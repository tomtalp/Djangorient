# Djangorient
An OrientDB backend for Django. 
Still in early development stages, feel free to join and help growing.

### settings.py
```
DJANGORIENT_SETTINGS = {
    'host': 'localhost',
    'port': '2480',
    'username': 'root',
    'password': 'root',
    'name': 'TestDB',
}
```

### Setting up models
```
# models.py
from djangorient.DjangorientModels import *

class Person(DjangorientNode):
	name = String()
	age = Integer()

class Animal(DjangorientNode):
	nickname = String()

class Owns(DjangorientEdge):
	years_owned = Integer()	

```

### Working with your data
Working with data is very similar to the original Django ORM.

You can easily add new nodes and connect them with your edges.

```
p1 = Person.objects.create(name = "Tom", age = 120)
a1 = Animal.objects.create(nickname = "Doggy")

edge = Owns.objects.create(p1, a1, years_owned = 5)
```

And then query the nodes & the edges
```
p1 = Person.objects.filter(name = "Tom")
print p1.out_Owns # ID of the owned Animal

e1 = Owns.objectrs.get_by_id('#20:3')
print e1.in_vertex # ID of incoming node
print e1.out_vertex # ID of outcoming node

animals = Animal.objects.all()


```

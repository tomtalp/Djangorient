# Djangorient
An OrientDB backend for Django. 

Setting up models -
```
# models.py
from djangorient.DjangorientModels import *

class Person(DjangorientNode):
	name = String()
	age = Integer()

class Animal(DjangorientNode):
	nickname = String()

```

Working with your DB
```
p = Person()

p.create(name = "Tom", age = 120)

results = p.filter(name = "Tom")
```
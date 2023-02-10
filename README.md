# CIP Curriculm Italian Parser

### Curriculum Italian Parser

A simple curriculum parser for italian CV

```python
from cip import Cip

r = Cip("it")
    
result = r.read_file_pdf('/path/to/pdf/file')
print(result)
```
result
```json
{
    "nome": "Rojack",
    "data_di_nascita": "01/01/1970 (53)",
    "residenza": [
        "Silicon Valley"
    ],
    "email": "rojack96@example.it",
    "telefono": "(+39) 321 123 12 32",
    "universita": true,
    "linguaggi_di_programmazione": [
        "Angular",
        "Python"
    ],
    "soft_skill": null,
    "ruolo": [
        "Backend",
        "Junior"
    ],
    "altro": null
}
```

If use ```Cip()``` return the name of key in english (ex. nome -> name)

```json
{
    "name": "Rojack",
    "date_of_birth": "01/01/1970 (53)",
    "location": [
        "Silicon Valley"
    ],
    "email": "rojack96@example.it",
    "phone": "(+39) 321 123 12 32",
    ...
    ...
}
```

The keys ```linguaggi_di_programmazione```, ```soft_skill```, ```ruolo``` and ```altro``` return an array of word matched by relative keys in config.json file.


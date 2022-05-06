# Decoration

## Singleton

### Target

Class

### Descriptions

### Usage

### Example

---

## Logging

### Target

Class

### Descriptions

### Usage

### Example

---

## HasProperties

### Target

Class

### Descriptions

### Usage

### Example

#### Code

```python
@HasProperties
class AClass:
    debug: bool  # optional
    props: Dictionary  # optional
    preset: {  # optional
        'p1': 'a',
        'p2': 'b',
        'o1': 'c',
    }


clazz = AClass(props={
    'p2': 'B',
    'o1': 'O',
    'o2': 'O2'
})

print(clazz.props)
```

#### Result

```json
{
  'p1': 'a',
  'p2': 'B',
  'o1': 'O',
  'o2': 'O2'
}
``` 
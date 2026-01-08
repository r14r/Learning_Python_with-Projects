# Pflichtenheft: Metaclass Validator

## Expected Functionality
A data validation system using metaclasses and descriptors to automatically enforce type and range constraints on class attributes. Demonstrates advanced Python metaprogramming concepts.

## Input
- **Class definitions**: Classes with type annotations and `__validators__` dict
- **Validator configurations**: Dict with 'min' and 'max' constraints
- **Instance attributes**: Values assigned to class properties

## Expected Output
```
Metaclass Validator Demo

1. Creating valid person:
  Person(name='Alice', age=30, email='alice@example.com')

2. Testing age validation:
  Error caught: age must be <= 150

3. Testing type validation:
  Error caught: name must be str, got int

4. Creating product:
  Product(name='Widget', price=19.99, quantity=100)

5. Testing price validation:
  Error caught: price must be >= 0.0

6. Valid updates:
  Person(name='Alice', age=31, email='alice@example.com')
  Product(name='Widget', price=19.99, quantity=50)
```

## Tests

### Test 1: Type Validation - Valid
**Input:** `person.name = "Bob"`  
**Expected Output:** Assignment succeeds

### Test 2: Type Validation - Invalid
**Input:** `person.name = 123`  
**Expected Output:** Raises `TypeError`

### Test 3: Range Validation - Valid
**Input:** `person.age = 25`  
**Expected Output:** Assignment succeeds

### Test 4: Range Validation - Too High
**Input:** `person.age = 200`  
**Expected Output:** Raises `ValueError` with "must be <= 150"

### Test 5: Range Validation - Too Low
**Input:** `product.price = -10`  
**Expected Output:** Raises `ValueError` with "must be >= 0.0"

### Test 6: Descriptor Get
**Input:** `print(person.name)`  
**Expected Output:** Current value of name

## Dependencies
- Standard library only (typing)

## Usage
```bash
python script.py
```

## Notes
Demonstrates advanced concepts: metaclasses, descriptors, type annotations, the `__new__` method, and automatic property creation. Shows how Python's object model can be extended for domain-specific validation.

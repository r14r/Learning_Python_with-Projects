# Pflichtenheft: Mini ORM

## Expected Functionality
A minimal Object-Relational Mapping (ORM) system that maps Python classes to database tables, supporting CRUD operations, queries, and relationships. Uses SQLite and dataclasses for clean model definitions.

## Input
- **Model definitions**: Dataclasses inheriting from Model
- **Database operations**:
  - `save()`: Insert record
  - `find_all()`: Query all records
  - `find_by_id(id)`: Query by primary key
  - `find_by(**kwargs)`: Query by fields

## Expected Output
```
Mini ORM Demo

1. Creating tables...
  Tables created

2. Creating users...
  Created user: Alice (ID: 1)
  Created user: Bob (ID: 2)

3. Creating posts...

4. Finding all users:
  - Alice (alice@example.com), age 30
  - Bob (bob@example.com), age 25

5. Finding user by ID:
  Found: Alice

6. Finding users by criteria:
  - Bob, age 25

7. Finding posts by user:
  - First Post: Hello World
  - Second Post: Learning ORM
```

## Tests

### Test 1: Create Table
**Input:** `User.create_table()`  
**Expected Output:** Table created in database

### Test 2: Save Record
**Input:** `user = User("Alice", "alice@example.com", 30); user.save()`  
**Expected Output:** Returns record ID (e.g., 1)

### Test 3: Find All
**Input:** `User.find_all()`  
**Expected Output:** List of all User instances

### Test 4: Find By ID
**Input:** `User.find_by_id(1)`  
**Expected Output:** User instance with ID 1

### Test 5: Find By Criteria
**Input:** `User.find_by(age=25)`  
**Expected Output:** List of users with age=25

### Test 6: Type Mapping
**Input:** Model with int, str, float fields  
**Expected Output:** Correct SQL types in CREATE TABLE

## Dependencies
- Standard library only (sqlite3, typing, dataclasses)

## Usage
```bash
python script.py
```

## Notes
Demonstrates ORM concepts: active record pattern, type mapping, query building, dataclass integration, and basic SQL generation. Shows how to build abstractions over databases.

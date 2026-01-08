#!/usr/bin/env python3
"""
Metaclass Validator Script
Data validation using metaclasses and descriptors.
"""

from typing import Any, Type


class TypedProperty:
    """Descriptor for type-validated properties."""
    
    def __init__(self, name: str, expected_type: Type):
        """
        Initialize typed property.
        
        Args:
            name: Property name
            expected_type: Expected type
        """
        self.name = name
        self.expected_type = expected_type
        self.data_name = f'_{name}'
    
    def __get__(self, instance, owner):
        """Get property value."""
        if instance is None:
            return self
        return getattr(instance, self.data_name, None)
    
    def __set__(self, instance, value):
        """Set property value with type validation."""
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.name} must be {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        setattr(instance, self.data_name, value)


class RangeValidator:
    """Descriptor for range-validated numeric properties."""
    
    def __init__(self, name: str, min_value: float = None, max_value: float = None):
        """
        Initialize range validator.
        
        Args:
            name: Property name
            min_value: Minimum allowed value
            max_value: Maximum allowed value
        """
        self.name = name
        self.min_value = min_value
        self.max_value = max_value
        self.data_name = f'_{name}'
    
    def __get__(self, instance, owner):
        """Get property value."""
        if instance is None:
            return self
        return getattr(instance, self.data_name, None)
    
    def __set__(self, instance, value):
        """Set property value with range validation."""
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name} must be a number")
        
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"{self.name} must be >= {self.min_value}")
        
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"{self.name} must be <= {self.max_value}")
        
        setattr(instance, self.data_name, value)


class ValidatorMeta(type):
    """Metaclass that automatically creates validators for annotated fields."""
    
    def __new__(mcs, name, bases, namespace, **kwargs):
        """
        Create new class with automatic validators.
        
        Args:
            name: Class name
            bases: Base classes
            namespace: Class namespace
        
        Returns:
            New class
        """
        # Get type annotations
        annotations = namespace.get('__annotations__', {})
        
        # Get validation rules
        validators = namespace.get('__validators__', {})
        
        # Create descriptors for annotated fields
        for field_name, field_type in annotations.items():
            if field_name.startswith('_'):
                continue
            
            # Check if custom validator is defined
            if field_name in validators:
                validator_config = validators[field_name]
                
                if 'min' in validator_config or 'max' in validator_config:
                    namespace[field_name] = RangeValidator(
                        field_name,
                        validator_config.get('min'),
                        validator_config.get('max')
                    )
                else:
                    namespace[field_name] = TypedProperty(field_name, field_type)
            else:
                # Use type validation by default
                namespace[field_name] = TypedProperty(field_name, field_type)
        
        return super().__new__(mcs, name, bases, namespace)


class Person(metaclass=ValidatorMeta):
    """Example class using metaclass validation."""
    
    name: str
    age: int
    email: str
    
    __validators__ = {
        'age': {'min': 0, 'max': 150}
    }
    
    def __init__(self, name: str, age: int, email: str):
        """
        Initialize person.
        
        Args:
            name: Person's name
            age: Person's age
            email: Person's email
        """
        self.name = name
        self.age = age
        self.email = email
    
    def __repr__(self):
        """String representation."""
        return f"Person(name={self.name!r}, age={self.age}, email={self.email!r})"


class Product(metaclass=ValidatorMeta):
    """Example product class with validation."""
    
    name: str
    price: float
    quantity: int
    
    __validators__ = {
        'price': {'min': 0.0},
        'quantity': {'min': 0}
    }
    
    def __init__(self, name: str, price: float, quantity: int):
        """Initialize product."""
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def __repr__(self):
        """String representation."""
        return f"Product(name={self.name!r}, price={self.price}, quantity={self.quantity})"


def main():
    """Main function to demonstrate metaclass validation."""
    print("Metaclass Validator Demo")
    
    # Create valid person
    print("\n1. Creating valid person:")
    person = Person("Alice", 30, "alice@example.com")
    print(f"  {person}")
    
    # Try invalid age
    print("\n2. Testing age validation:")
    try:
        person.age = 200  # Should fail
    except ValueError as e:
        print(f"  Error caught: {e}")
    
    # Try invalid type
    print("\n3. Testing type validation:")
    try:
        person.name = 123  # Should fail
    except TypeError as e:
        print(f"  Error caught: {e}")
    
    # Create product
    print("\n4. Creating product:")
    product = Product("Widget", 19.99, 100)
    print(f"  {product}")
    
    # Try negative price
    print("\n5. Testing price validation:")
    try:
        product.price = -5.0  # Should fail
    except ValueError as e:
        print(f"  Error caught: {e}")
    
    # Valid update
    print("\n6. Valid updates:")
    person.age = 31
    product.quantity = 50
    print(f"  {person}")
    print(f"  {product}")


if __name__ == "__main__":
    main()

import pytest

from Objectualizer import objectualize

"""
Code Analysis:
- The main goal of the function is to provide a more human-readable display of an object or class in a vertical way, similar to the format of a dictionary or JSON.
- The function takes in one parameter, 'obj', which can be an object or a class.
- The function first checks if the input 'obj' is a class or has a '__dict__' attribute.
- If it is a class or has a '__dict__' attribute, the function creates a dictionary of the object's attributes and iterates through them to create a string representation of the object.
- If it is not a class or does not have a '__dict__' attribute, the function simply returns a string representation of the object.
- The function then passes the string representation of the object to the 'revolk' function, which formats the string to be more human-readable by adding newlines and tabs.
- Finally, the formatted string is printed to the console.
"""



class TestObjectualize:

    # Tests that the function returns none when given an empty object. tags: [happy path]
    def test_empty_object(self):
        assert objectualize({}) == "{\n\t\n}"

    # Tests that the function can handle nested attributes. tags: [happy path]
    def test_nested_attributes(self):
        class Person:
            def __init__(self, name, age):
                self.name = name
                self.age = age

        class Company:
            def __init__(self, name, employees):
                self.name = name
                self.employees = employees

        person1 = Person("John", 30)
        person2 = Person("Jane", 25)
        company = Company("ABC Inc.", [person1, person2])

        # expected_output = "{name <str> : ABC Inc., employees <list> : {\n\t{name <str> : John, age <int> : 30}\n\t{name <str> : Jane, age <int> : 25}\n}}"
        expected_output = "{\n\tname <str> : ABC Inc.,\n\temployees <list> : [\n\t\t{\n\t\t\tname <str> : John,\n\t\t\tage <int> : 30\n\t\t},\n\t\t{\n\t\t\tname <str> : Jane,\n\t\t\tage <int> : 25\n\t\t}\n\t]\n}"
        result = objectualize(company)
        print("ENCERRONA")
        print(repr(result))
        print("ENCERRONA")
        assert result == expected_output

    # Tests that the function can handle circular references in objects. tags: [edge case]
    def test_circular_references(self):
        class Node:
            def __init__(self, value):
                self.value = value
                self.next = None

        node1 = Node(1)
        node2 = Node(2)
        node3 = Node(3)

        node1.next = node2
        node2.next = node3
        node3.next = node1

        expected_output = "{\n\tvalue <int> : 1,\n\tnext <Node> : {\n\t\tvalue <int> : 2,\n\t\tnext <Node> : {\n\t\t\tvalue <int> : 3,\n\t\t\tnext <Node> : {\n\t\t\t\t...circular reference\n\t\t\t}\n\t\t}\n\t}\n}"
        assert objectualize(node1) == expected_output

    # Tests that the function can handle unsupported attributes (e.g. functions) in objects. tags: [edge case]
    def test_unsupported_attributes(self):
        class Person:
            def __init__(self, name):
                self.name = name
                self.say_hello = lambda: print(f"Hello, my name is {self.name}")

        person = Person("John")

        expected_output = "{\n\tname <str> : John,\n\tsay_hello <function> : Unsupported Attribute Value\n}"
        assert objectualize(person) == expected_output

    # Tests that the function can handle non-ascii characters in objects. tags: [edge case]
    def test_non_ascii_characters(self):
        class Person:
            def __init__(self, name):
                self.name = name

        person = Person("Jørgen")

        expected_output = "{\n\tname <str> : Jørgen\n}"
        assert objectualize(person) == expected_output

    # Tests that the function can handle unhandled types of objects or classes. tags: [edge case]
    def test_unhandled_types(self):
        class CustomType:
            pass

        custom_obj = CustomType()

        assert objectualize(custom_obj) is not None

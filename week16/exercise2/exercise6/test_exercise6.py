
import pytest
from exercise6 import sort_list


def test_sort_list_with_string():
    #Arrange
    input_string = 'hello-world'

    #Act
    result = sort_list(input_string)

    #Assert
    assert result == ['hello', 'world']


def test_sort_list_with_numbers():
    #Arrange
    numbers = 12
    #Act
    with pytest.raises(AttributeError):
        sort_list(numbers)
    #Assert
    assert AttributeError


def test_sort_list_with_empty_string():
    #Arrange
    empty_string = ''
    #Act
    result = sort_list(empty_string)

    #Assert
    assert result == ['']
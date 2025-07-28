

import pytest
from exercise3 import sum_list

def test_get_list_numbers_with_small_list():
    #Arrange
    numbers = [1, 2, 3, 4, 5]

    #Act
    result = sum_list(numbers)

    #Assert
    assert result == 15

def test_get_list_numbers_with_empty_list():
    #Arrange
    numbers = []
    #Act
    result = sum_list(numbers)
    #Assert
    assert result == 0

def test_get_list_numbers_with_other_type_of_parameter():
    #Arrange
    numbers = "12345"
    #Act
    with pytest.raises(TypeError):
        sum_list(numbers)
    #Assert
    assert TypeError

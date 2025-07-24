

import pytest
from exercise4 import reverse_string

def test_reverse_string_with_string():
    #Arrange
    input_string = "Hello, World!"

    #Act
    result = reverse_string(input_string)

    #Assert
    assert result == "!dlroW ,olleH"

def test_reverse_string_with_empty_string():
    #Arrange
    empty_string = ''

    #Act
    result = reverse_string(empty_string)

    #Assert
    assert result == ''



def test_reverse_string_with_different_parameter():
    #Arrange
    different_input = 12345

    #Act
    with pytest.raises(TypeError):
        result = reverse_string(different_input)

    #Assert
    assert TypeError
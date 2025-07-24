
import pytest
from exercise5 import count_upper_lower


def test_count_upper_lower_with_string():
    #Arrange
    input_string = "Hello World"

    #Act
    result = count_upper_lower(input_string)

    #Assert
    assert result == (2, 8)


def test_count_upper_lower_with_string_with_punctuation_marks():
    #Arrange
    input_string = "Hello, World!"
    #Act
    result = count_upper_lower(input_string)
    #Assert
    assert result == (2, 8)


def test_count_upper_lower_with_string_with_numbers():
    #Arrange
    string_with_numbers = "Hello 123 World"

    #Act
    result = count_upper_lower(string_with_numbers)

    #Assert
    assert result == (2, 8)


def test_count_upper_lower_with_numbers():
    numbers = 33

    with pytest.raises(TypeError):
        count_upper_lower(numbers)

    assert TypeError
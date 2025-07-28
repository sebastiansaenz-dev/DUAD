
import pytest
from exercise7 import verify_prime_numbers


def test_verify_prime_numbers_with_string():
    #Arrange
    empty_num = 'hello world'
    #Act
    with pytest.raises(TypeError):
        verify_prime_numbers(empty_num)
    #Assert
    assert  TypeError


def test_verify_prime_numbers_with_not_prime_num():
    #Arrange
    num = 4
    #Act
    result = verify_prime_numbers(num)
    #Assert
    assert result == False


def test_verify_prime_numbers_with_prime_num():
    #Arrange
    num = 7
    #Act
    result = verify_prime_numbers(num)
    #Assert
    assert result == True
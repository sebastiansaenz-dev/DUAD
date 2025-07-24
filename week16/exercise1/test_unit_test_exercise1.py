

import pytest
import random
from bubble_sort_function import bubble_sort


def test_bubble_sort_with_small_list():
    #Arrange
    little_list = [4, 5, 1, 3, 2]

    #Act
    result = bubble_sort(little_list)
    
    #Assert
    assert result == [1, 2, 3, 4, 5]


def test_bubble_sort_with_large_list():
    #Arrange
    big_list = list(range(1, 101))
    random.shuffle(big_list)
    
    #Act
    result = bubble_sort(big_list)

    #Assert
    assert result == list(range(1, 101))


def test_bubble_sort_with_empty_list():
    #Arrange

    empty_list = []
    #Act

    result = bubble_sort(empty_list)
    #Assert

    assert result == []


def test_bubble_sort_with_other_type_of_parameter():
    #Arrange
    other_parameter_list = [4, 5, 'a', 3, 2]
    #Act
    with pytest.raises(TypeError):
        bubble_sort(other_parameter_list)
    #Assert
    assert TypeError
"""
Test features in binarypp.utils
"""

import binarypp.utils as utils


def test_is_binary():
    assert utils.is_binary("00001111") == True
    assert utils.is_binary("0000111") == False
    assert utils.is_binary("hello world") == False


def test_to_binary_str():
    assert utils.to_binary_str(0b00000100) == "00000100"
    assert utils.to_binary_str(10) == "00001010"


def test_binary_to_chars():
    assert utils.binary_to_chars(["00000100", "00001010"]) == "\x04\n"
    assert utils.binary_to_chars(["01101000", "01101001"]) == "hi"


def test_levenshtein_distance():
    assert utils.levenshtein_distance("hello", "world") == 4
    assert utils.levenshtein_distance("this", "that") == 2


def test_fuzzy_search():
    assert utils.fuzzy_search("dog", ["frog", "hog", "top"]) == "hog"
    assert utils.fuzzy_search("hi", ["hill", "pill", "sill"]) == "hill"
    assert utils.fuzzy_search("elephant", ["elegant", "extra", "egg"]) == "elegant"
    

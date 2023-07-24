import hashlib
from django.utils import timezone


def hash_filename(string):
    """
    Returns a hashed filename based on an input string
    """

    string_bytes = string.encode("utf-8")
    sha256_hash = hashlib.sha256()
    sha256_hash.update(string_bytes)
    hashed_filename = sha256_hash.hexdigest()

    return hashed_filename


def file_path(instance, filename):
    """
    Returns a path (filename included) for the uploaded image to be saved
    """
    timestamp = timezone.now()
    timestamp_string = timestamp.strftime("%Y-%m-%d_%H:%M:%S")
    return "uploaded_files/" + hash_filename(f"{instance.name}{timestamp_string}")


def find_string_between_substrings(input_string, start_substring, end_substring):
    """Given two substrings that mark the start and end, it returns the text in the middle"""
    start_index = input_string.find(start_substring)
    if start_index == -1:
        return None  # Start substring not found in the input_string

    end_index = input_string.find(end_substring, start_index + len(start_substring))
    if end_index == -1:
        return None  # End substring not found after the start_substring

    result_string = input_string[start_index + len(start_substring) : end_index]
    return result_string

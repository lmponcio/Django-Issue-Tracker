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
    return "uploaded_files/" + hash_filename(f"{instance.username}{timestamp_string}")

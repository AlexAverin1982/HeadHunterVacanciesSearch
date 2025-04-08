"""
from src.storage_manager_class import StorageManager


def test_storage() -> None:
    tm = StorageManager("aaa")
    tm.save("", True)
    tm.load()
    tm.delete()
    assert True
"""

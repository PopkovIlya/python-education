from typing import Any


class HashTable(object):

    def __init__(self, size=1000):
        """
        use list as storage, each element is also a list which is used
        to solve hash conflict (collision)
        """
        self.storage = [[] for _ in range(size)]
        self.size = size
        self.length = 0

    def __get_index(self, key):
        return hash(key) % self.size  # use built-in hash function

    def insert(self, key, value) -> None:
        """
        set key value, if conflict, append to the sub list
        """
        storage_idx = self.__get_index(key)
        for elem in self.storage[storage_idx]:
            if key == elem[0]:  # already exist, update it
                elem[1] = value
                break
        else:
            self.storage[storage_idx].append([key, value])
            self.length += 1

    def lookup(self, key) -> Any:
        """
        get by key, if not found, return None
        :return: value
        """
        storage_idx = self.__get_index(key)
        for elem in self.storage[storage_idx]:
            if elem[0] == key:
                return elem[1]

        return None

    def delete(self, key) -> None:
        """
        delete key value from current dictionary instance
        :param key: str
        """
        storage_idx = self.__get_index(key)
        for sub_lst in self.storage[storage_idx]:
            if key == sub_lst[0]:
                self.storage[storage_idx].remove(sub_lst)
                self.length -= 1
                return

        raise KeyError("Key {} does not exist".format(key))

    def __iterate_kv(self):
        """
        create the items generator
        :return: generator
        """
        for sub_lst in self.storage:
            if not sub_lst:
                continue
            for item in sub_lst:
                yield item

    def __iter__(self):
        """
        create the keys generator
        :return: generator
        """
        for key_var in self.__iterate_kv():
            yield key_var[0]

    def keys(self):
        """
        get all keys as list
        :return: list
        """
        return self.__iter__()

    def values(self):
        """
        get all values as list
        :return: list
        """
        for key_var in self.__iterate_kv():
            yield key_var[1]

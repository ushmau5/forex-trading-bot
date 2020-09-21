from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def is_valid_entry(self, df):
        pass

from abc import ABC, abstractmethod

class strategy_interface(ABC):
    @abstractmethod
    def export(documents):
        pass
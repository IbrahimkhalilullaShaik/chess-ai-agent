from abc import ABC, abstractmethod

class BaseAgent(ABC):
    @abstractmethod
    def select_move(self, board):
        """
        Given a python-chess Board object,
        return a legal chess.Move
        """
        pass
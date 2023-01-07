import abc


class ASegmentator(abc.ABC):
    @abc.abstractmethod
    def run(self):
        pass

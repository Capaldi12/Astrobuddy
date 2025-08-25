from abc import ABC, abstractmethod
from typing import Iterable


class MissingClass:
    """Sentinel, indicating that intended value is missing"""

    def __repr__(self):
        return '<missing>'

    def __bool__(self):
        return False


# Sentinel object
Missing = MissingClass()


class Merger(ABC):
    """Merges two objects based on rules"""

    def merge(self, left=Missing, right=Missing):
        """Merge objects"""

        if left is Missing and right is Missing:
            raise ValueError('Can\'t merge two Missing values!')

        if left is Missing:
            return right

        if right is Missing:
            return left

        return self.do_merge(left, right)

    @abstractmethod
    def do_merge(self, left, right):
        """Perform the actual merging"""

    @property
    def default_merger(self) -> 'Merger':
        """Default merger for when specific merger is missing"""

        # Like in dicts, newer value takes precedence
        return ReplaceMerger()

    def __getitem__(self, item: str) -> 'Merger':
        """Get child merger"""

        return self.default_merger

    def __contains__(self, item: str) -> bool:
        """Whether there is a child merger for given name"""

        return False

    def get(self, *path: str) -> 'Merger':
        """Get a merger from somewhere down the hierarchy"""

        merger = self

        try:
            for key in path:
                merger = merger[key]
            return merger

        except (KeyError, IndexError, TypeError):
            return NoMerger()


class NoMerger(Merger):
    """When no merger is available, NoMerger will let you know"""

    def do_merge(self, left, right):
        raise ValueError('No merger found!')


class SkipMerger(Merger):
    """Skips second object if first is present"""

    def do_merge(self, left, right):
        return left


class ReplaceMerger(Merger):
    """Replaces first object with second"""

    def do_merge(self, left, right):
        return right


class MatchMerger(Merger):
    """Only merges if objects match"""
    # TODO comparer callback?

    def do_merge(self, left, right):
        if left == right:
            return left

        raise ValueError('Values do not match!')


class AddMerger(Merger):
    """Adds objects together"""

    def do_merge(self, left, right):
        return left + right


class DictMerger(Merger):
    """Merges two dicts (pretty similar to how dict union works)"""

    def do_merge(self, left, right):
        keys = union_lists(left.keys(), right.keys())

        return {
            key: self[key].merge(
                left.get(key, Missing),
                right.get(key, Missing)
            ) for key in keys
        }


class RecordDictMerger(DictMerger):
    """Merges two dicts, with specific mergers for all/some of the fields"""

    fields: dict[str, Merger]

    def __init__(self, **fields: Merger):
        super().__init__()

        self.fields = fields

    def __getitem__(self, item: str) -> Merger:
        if item in self.fields:
            return self.fields[item]

        return self.default_merger

    def __contains__(self, item):
        return item in self.fields


class CollectionDictMerger(DictMerger):
    """Merges two dicts, with shared custom merger for fields"""

    field: Merger

    def __init__(self, field: Merger):
        super().__init__()

        self.field = field

    def __getitem__(self, item: str) -> Merger:
        return self.field

    def __contains__(self, item):
        return True


class UnionListMerger(Merger):
    """Merges two lists, but ensures items are unique"""

    def __init__(self, key=None):
        if key:
            self.key = key
        else:
            self.key = lambda x: x

    def do_merge(self, left, right):
        result = list(left)
        keys = [self.key(item) for item in left]

        for item in right:
            key = self.key(item)

            if key not in keys:
                result.append(item)
                keys.append(key)

        return result


# Shorthand for merging lists
union_lists = UnionListMerger().merge


# Merging hierarchy
the_merger = RecordDictMerger(
    items=CollectionDictMerger(
        RecordDictMerger(
            name=MatchMerger(),
            tags=UnionListMerger(),
            power=CollectionDictMerger(ReplaceMerger()),
            slots=CollectionDictMerger(ReplaceMerger()),
        )
    ),
    recipes=AddMerger()
)


def merge(*things, key=None):
    """Merges all the things together"""

    if len(things) < 2:
        raise ValueError('Need at least two items to merge!')

    if key is None:
        merger = the_merger
    elif isinstance(key, str):
        merger = the_merger.get(key)
    elif isinstance(key, Iterable):
        merger = the_merger.get(*key)
    else:
        raise TypeError(f'Invalid type of the key: {type(key)}')

    if isinstance(merger, NoMerger):
        raise ValueError(f'Merger not found: {key}')

    result, *things = things

    for thing in things:
        result = merger.merge(result, thing)

    return result

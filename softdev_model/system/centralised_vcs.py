from .bug import Bug
from .feature import Feature
from .software_system import SoftwareSystem

import copy


class Conflict(object):

    def __init__(self, logical_name, resolve_threshold):
        self.logical_name = logical_name
        self.resolve_threshold = resolve_threshold

    def __str__(self):
        return str(self.logical_name)

    def __repr__(self):
        return str(self.logical_name)


class CentralisedVCSServer(object):
    """
    Models the functions of a typical centralised version control system server such as Subversion.
    """

    def __init__(self, system):
        self.master = system
        self.version = 0
        pass

    def checkout(self):
        return CentralisedVCSClient(self)

    def receive_commit(self, working_copy, version):
        if version < self.version:
            raise CentralisedVCSException()
        else:
            self.master = copy.deepcopy(working_copy)
            self.version += 1


class CentralisedVCSClient(object):
    """
    Models the functions of a centralised version control system client, such as subversion,
    following a modify-update-merge-commit cycle.
    """

    def __init__(self, server, probability_automatically_resolve=0.25):
        self.server = server
        self.working_base = None
        self.working_copy = None

        self.update(None)

        self.probability_automatically_resolve = probability_automatically_resolve
        self.conflicts = []

    @staticmethod
    def _working_base_chunk_has_been_updated(old_working_base_chunk, new_working_base_chunk):
        if old_working_base_chunk is None:
            # A new chunk has been introduced by the update.
            return False
        elif new_working_base_chunk == old_working_base_chunk:
            # The update hasn't changed the working base.
            return False
        else:
            return True

    @staticmethod
    def _working_copy_chunk_has_local_changes(old_working_base_chunk, old_working_copy_chunk, new_working_base_chunk):
        if old_working_copy_chunk == old_working_base_chunk:
            # The working copy can be safely over-written as it doesn't contain local changes.
            return False
        elif old_working_copy_chunk == new_working_base_chunk:
            # The local changes to the working copy are identical to the changes in the update.
            return False
        else:
            return True

    def _add_conflict(self, working_base_chunk, random):
        conflict_complexity = random.random()
        conflict = Conflict(working_base_chunk.logical_name, conflict_complexity)
        self.conflicts.append(conflict)
        return conflict

    def _try_automatic_resolve(self, conflict, random):
        if conflict.resolve_threshold <= self.probability_automatically_resolve:
            self.resolve(conflict, random)

    def _merge(self, old_working_base, old_working_copy, random):
        """
        Check if each chunk in the current working base has changed since the last update.  If so, either over-write the
        ne working copy if it hasn't been modified, or conflict.
        :param old_working_base:
        :param old_working_copy:
        :param random:
        """
        for new_working_base_chunk in self.working_base.chunks:

            logical_name = new_working_base_chunk.logical_name

            old_working_base_chunk = old_working_base.get_chunk(logical_name)
            old_working_copy_chunk = old_working_copy.get_chunk(logical_name)

            if self._working_copy_chunk_has_local_changes(
                    old_working_base_chunk, old_working_copy_chunk, new_working_base_chunk):

                new_working_copy_chunk = self.working_copy.get_chunk(old_working_copy_chunk.logical_name)
                new_working_copy_chunk.overwrite_with(old_working_copy_chunk)

                if self._working_base_chunk_has_been_updated(old_working_base_chunk, new_working_base_chunk):

                    conflict = self._add_conflict(new_working_base_chunk, random)
                    self._try_automatic_resolve(conflict, random)

    def update(self, random):
        old_working_base = self.working_base
        old_working_copy = self.working_copy

        self.working_base = copy.deepcopy(self.server.master)

        self.working_copy = copy.deepcopy(self.working_base)

        if not(old_working_base is None or old_working_copy is None):
            self._merge(old_working_base, old_working_copy, random)

        self.version = self.server.version

    def commit(self):
        if not len(self.conflicts) > 0:
            self.server.receive_commit(self.working_copy, self.version)
        else:
            raise CentralisedVCSException()

    def resolve(self, conflict, resolver, random):
        self.conflicts.remove(conflict)

        working_base_chunk = self.working_base.get_chunk(conflict.logical_name)
        working_copy_chunk = self.working_copy.get_chunk(conflict.logical_name)

        working_copy_chunk.merge( working_base_chunk, resolver, random)

        pass


class CentralisedVCSException(Exception):

    def __init__(self):
        pass

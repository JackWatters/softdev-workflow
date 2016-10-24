from .software_system import SoftwareSystem

from threading import Lock


def copy_software_system(system):
    """
    A custom function for making a copy of a software system object.
    """

    copied_system = SoftwareSystem(
        probability_gain_feature_dependency=system.probability_gain_feature_dependency,
        probability_lose_feature_dependency=system.probability_lose_feature_dependency,
        probability_gain_system_dependency=system.probability_gain_system_dependency,
        probability_lose_system_dependency=system.probability_lose_system_dependency,
        probability_new_bug=system.probability_new_bug,
        probability_debug_known=system.probability_debug_known,
        probability_debug_unknown=system.probability_debug_unknown,
        probability_failure_on_demand=system.probability_failure_on_demand,
        test_effectiveness=system.test_effectiveness,
        test_efficiency=system.test_efficiency
    )
    for feature in system.features:
        target_feature = copied_system.add_feature(feature.logical_name, feature.size)

        for chunk in feature.chunks:
            target_chunk = target_feature.add_chunk(chunk.logical_name, chunk.local_content)

            for bug in chunk.bugs:
                target_chunk.add_bug(bug.logical_name)

        for test in feature.tests:
            target_feature.add_test(test.logical_name)

    for chunk in system.chunks:
        target_chunk = copied_system.get_chunk(chunk.fully_qualified_name)
        for dependency in chunk.dependencies:
            target_dependency = copied_system.get_chunk(dependency.fully_qualified_name)
            target_chunk.add_dependency(target_dependency)

    return copied_system


class CentralisedVCSException(Exception):

    def __init__(self):
        pass


class Conflict(object):

    def __init__(self, chunk_fully_qualified_name, resolve_threshold):
        self.chunk_fully_qualified_name = chunk_fully_qualified_name
        self.resolve_threshold = resolve_threshold

    def __str__(self):
        return str(self.chunk_fully_qualified_name)

    def __repr__(self):
        return str(self.chunk_fully_qualified_name)


class CentralisedVCSServer(object):
    """
    Models the functions of a typical centralised version control system server such as Subversion.
    """

    def __init__(self, system):
        self.master = system
        self.version = 0
        self.lock = Lock()

    def checkout(self):
        return CentralisedVCSClient(self)

    def latest(self):
        self.lock.acquire()
        result = (copy_software_system(self.master), self.version)
        self.lock.release()
        return result[0], result[1]

    def receive_commit(self, working_copy, version):
        self.lock.acquire()
        if version < self.version:
            raise CentralisedVCSException()
        else:
            self.master = copy_software_system(working_copy)
            self.version += 1
        self.lock.release()


class CentralisedVCSClient(object):
    """
    Models the functions of a centralised version control system client, such as subversion,
    following a modify-update-merge-commit cycle.
    """

    def __init__(self, server, probability_automatically_resolve=0.25):
        self.server = server

        self.working_base, self.version = self.server.latest()
        self.working_copy = copy_software_system(self.working_base)

        self.probability_automatically_resolve = probability_automatically_resolve
        self.conflicts = []

    def _add_conflict(self, working_base_chunk, random):
        conflict_complexity = random.random()
        conflict = Conflict(working_base_chunk.fully_qualified_name, conflict_complexity)
        self.conflicts.append(conflict)
        return conflict

    def _try_automatic_resolve(self, conflict, random):
        if conflict.resolve_threshold <= self.probability_automatically_resolve:
            self.resolve(conflict, random)

    def _merge(self, old_working_base, random):
        """
        Check if each chunk in the current working base has changed since the last update.  If so, either over-write the
        ne working copy if it hasn't been modified, or conflict.
        :param old_working_base:
        :param random:
        """
        for working_base_feature in self.working_base.features:
            working_copy_feature = self.working_copy.get_feature(working_base_feature.logical_name)
            if working_copy_feature is None:
                self.working_copy.add_feature(working_copy_feature.logical_name, working_copy_feature.size)

        for new_working_base_chunk in self.working_base.chunks:
            chunk_fully_qualified_name = new_working_base_chunk.fully_qualified_name

            working_copy_chunk = self.working_copy.get_chunk(chunk_fully_qualified_name)

            if working_copy_chunk is None:
                working_copy_feature = self.working_copy.get_feature(new_working_base_chunk.feature.logical_name)
                working_copy_chunk = working_copy_feature.add_chunk(chunk_fully_qualified_name)
                working_copy_chunk.overwrite_with(new_working_base_chunk)

            else:
                old_working_base_chunk = old_working_base.get_chunk(chunk_fully_qualified_name)

                if old_working_base_chunk is not None and old_working_base_chunk != new_working_base_chunk:

                    if working_copy_chunk == old_working_base_chunk:
                        working_copy_chunk.overwrite_with(new_working_base_chunk)
                    elif working_copy_chunk != new_working_base_chunk:

                        conflict = self._add_conflict(new_working_base_chunk, random)
                        self._try_automatic_resolve(conflict, random)

    def update(self, random):
        old_working_base = self.working_base
        self.working_base, self.version = self.server.latest()
        self._merge(old_working_base, random)

    def commit(self):

        if not len(self.conflicts) > 0:
            self.server.receive_commit(self.working_copy, self.version)
        else:
            raise CentralisedVCSException()

    def resolve(self, conflict, random):
        self.conflicts.remove(conflict)

        working_base_chunk = self.working_base.get_chunk(conflict.chunk_fully_qualified_name)
        working_copy_chunk = self.working_copy.get_chunk(conflict.chunk_fully_qualified_name)

        working_copy_chunk.merge(working_base_chunk, random)

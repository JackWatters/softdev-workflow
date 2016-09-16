from .feature import Feature

from .software_system import SoftwareSystem


def copy_system(system):
    copied_system = SoftwareSystem()

    for original_feature in system.features:
        copied_system.copy_feature(original_feature)

    for original_chunk in system.chunks:
        copied_chunk = copied_system.get_chunk(original_chunk.logical_name)
        for original_dependency in original_chunk.dependencies:
            copied_dependency = copied_system.get_chunk(original_dependency.logical_name)
            copied_chunk.add_dependency(copied_dependency)

    return copied_system


class Conflict(object):

    def __init__(self, logical_name, resolve_threshold):
        self.logical_name = logical_name
        self.resolve_threshold = resolve_threshold


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
            self.master = copy_system(working_copy)
            self.version += 1


class CentralisedVCSClient(object):
    """
    Models the functions of a centralised version control system client, such as subversion,
    following a modify-update-merge-commit cycle.
    """

    def __init__(self, server, probability_automatically_resolve=0.25):
        self.server = server
        self.working_base = copy_system(self.server.master)
        self.working_copy = copy_system(self.working_base)
        self.version = server.version
        self.probability_automatically_resolve = probability_automatically_resolve
        self.conflicts = []

    def _update_working_copy_chunk_dependencies(self, working_base_chunk, working_copy_chunk):
        working_copy_chunk.dependencies.clear()

        for working_base_dependency in working_base_chunk.dependencies:
            working_copy_dependency = self.working_copy.get_chunk(working_base_dependency.logical_name)
            working_copy_chunk.add_dependency(working_copy_dependency)
        pass

    def _update_working_copy_with_new_features_chunks_and_tests(self):

        for working_base_feature in self.working_base.features:

            new_features = []

            working_copy_feature = self.working_copy.get_feature(working_base_feature.logical_name)
            if working_copy_feature is None:

                working_copy_feature =\
                    self.working_copy.copy_feature(working_base_feature.logical_name, working_base_feature.size)

                new_features.append((working_base_feature, working_copy_feature))

        for working_base_feature, working_copy_feature in new_features:
            for working_base_chunk in working_base_feature.chunks:
                working_copy_chunk = self.working_copy.get_chunk(working_base_chunk.logical_name)
                self._update_working_copy_chunk_dependencies(working_base_chunk, working_copy_chunk)

    def _update_existing_chunks(self, old_working_base, random):

        # Check if each chunk in the working base has changed since the last update.  If so, either over-write the
        # working copy if it hasn't been modified, or conflict.
        for working_base_chunk in self.working_base.chunks:

            old_working_base_chunk = old_working_base.get_chunk(working_base_chunk.logical_name)

            if working_base_chunk.content != old_working_base_chunk.content:

                working_copy_chunk = self.working_copy.get_chunk(working_base_chunk.logical_name)

                if working_copy_chunk.content == old_working_base_chunk.content:

                    working_copy_chunk.content = working_base_chunk.content
                    self._update_working_copy_chunk_dependencies(working_base_chunk, working_copy_chunk)

                elif working_copy_chunk.content != working_base_chunk.content:
                    conflict_complexity = random.random()
                    if conflict_complexity > self.probability_automatically_resolve:
                        conflict = Conflict(working_base_chunk.logical_name, conflict_complexity)
                        self.conflicts.append(conflict)

    def update(self, random):
        old_working_base = self.working_base
        self.working_base = copy_system(self.server.master)

        self._update_working_copy_with_new_features_chunks_and_tests()
        self._update_existing_chunks(old_working_base, random)

        self.version = self.server.version

    def commit(self):
        if not len(self.conflicts) > 0:
            self.server.receive_commit(self.working_copy, self.version)
        else:
            raise CentralisedVCSException()

    def resolve(self, conflict, random):
        self.conflicts.remove(conflict)
        working_base_chunk = self.working_base.get_chunk(conflict.logical_name)
        working_copy_chunk = self.working_copy.get_chunk(conflict.logical_name)

        working_copy_chunk.merge(random, working_base_chunk)

        pass


class CentralisedVCSException(Exception):

    def __init__(self):
        pass
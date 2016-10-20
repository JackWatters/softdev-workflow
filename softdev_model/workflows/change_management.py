from theatre_ag import default_cost
from softdev_model.system import CentralisedVCSException


@default_cost(1)
def resolve(self, conflict, centralised_vcs_client, random):
    centralised_vcs_client.resolve(conflict, self, random)


def commit_changes(self, centralised_vcs_client, random):
    while True:
        try:
            centralised_vcs_client.commit()
            centralised_vcs_client.update(random)
            break
        except CentralisedVCSException:
            centralised_vcs_client.update(random)
            for conflict in centralised_vcs_client.conflicts:
                self.perform_task(resolve, [conflict, centralised_vcs_client, random])

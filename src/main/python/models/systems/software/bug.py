'''
@author: tws
'''
class Bug(object):


    bug_count = 0


    def __init__(self, chunk, pfd=0.1):
        
        self.id = Bug.bug_count
        Bug.bug_count += 1
        
        self.chunk = chunk
        self.pfd = pfd


    def manifest(self, random):
        if random.random() <= self.pfd:
            raise BugEncounteredException(self)


    def __repr__(self):
        return "b_%d" % self.id


class BugEncounteredException(Exception):

    def __init__(self,bug):
        self.bug = bug
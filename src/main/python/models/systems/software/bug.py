'''
@author: tws
'''
class Bug(object):


    bug_count = 0


    def __init__(self, chunk):
        
        self.id = Bug.bug_count
        Bug.bug_count += 1
        
        self.chunk = chunk

        
    
    @property
    def pfd(self):
        return self.chunk.feature.software_system.pfd
    
    
    @property
    def pdetect(self):
        return self.chunk.feature.software_system.pdetect


    def manifest(self, random):
        if random.random() <= self.pfd:
            raise BugEncounteredException(self)


    def __repr__(self):
        return "b_%d" % self.id


class BugEncounteredException(Exception):

    def __init__(self,bug):
        self.bug = bug
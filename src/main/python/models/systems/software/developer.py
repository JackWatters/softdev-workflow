'''
Created on 1 Apr 2016

@author: Tim
'''

class Developer(object):
    '''
    classdocs
    '''


    def __init__(self, person_time):
        '''
        Constructor
        '''
        self.person_time = person_time


    def extend_feature(self, random, feature):
        feature.extend(random)

    
    def debug(self, random, test, bug):
        test.feature.debug(random, bug)


    def add_test(self, software_system, feature):
        software_system.add_test(feature)
        
        
    def refactor(self, random, feature):
        feature.refactor(random)

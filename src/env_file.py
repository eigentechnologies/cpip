import argparse
import hashlib
import sys
import yaml

class EnvFile:
    
    def __init__(self, filename):
        with open(filename) as f:
            self.env = yaml.safe_load(f)

    def channels(self):
        return self.env['channels']
    
    def dependencies(self):
        flat_dependencies = [d for d in self.env['dependencies'] if isinstance(d, str)]
        nested_pips = ['pip' for d in self.env['dependencies'] if isinstance(d, dict) and 'pip' in d]
        return sorted(set(flat_dependencies + nested_pips))
    
    def pip_dependencies(self):
        pip_envs = [d['pip'] for d in self.env['dependencies'] if isinstance(d, dict) and 'pip' in d]
        return sorted(set(p for env in pip_envs for p in env))

    def hash(self):
        m = hashlib.sha256() 
        # loop through channels -- order matters
        for c in self.channels():
            m.update(c.encode())
        # loop through dependencies -- order invariant
        for d in self.dependencies():
            m.update(d.encode())
        # loop through pip dependencies -- order invariant
        for p in self.pip_dependencies():
            m.update(p.encode())
        
        return m.hexdigest()

"""Magic wrapper to execute APEX and SOQL in notebooks"""
__version__ = '0.0.2'

from sfdxmagic.functions import execute_apex, execute_query

def load_ipython_extension(ipython):
    ipython.register_magic_function(execute_query, 'cell', 'sfdx:query')
    ipython.register_magic_function(execute_apex, 'cell', 'sfdx:apex')

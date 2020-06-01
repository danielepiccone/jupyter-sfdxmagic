import pandas as pd
from IPython import get_ipython

from sfdxmagic.runner import execute_sfdx

# TODO
def parse_magic_invocation(line):
    """
    Parses the magic invocation for the commands

    As a general rule we want to forward the arguments to sfdx
    But we also need to pass the variable to capture the results

    %%sfdx:cmd {var?} {...options}

    """
    args = { "variable": None }
    return args

def execute_query(line, query):
    args = parse_magic_invocation(line)

    results = execute_sfdx("force:data:soql:query -q \"{}\"".format(query))
    results_df = pd.DataFrame(results)

    if args.get('variable'):
        get_ipython().push({ args.get("variable"): results_df})

    return results_df.head()

def execute_apex(line, query):
    # TODO
    pass

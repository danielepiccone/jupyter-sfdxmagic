import pandas as pd
from IPython import get_ipython

from sfdxmagic.runner import execute_sfdx

def parse_magic_invocation(line):
    """
    Parses the magic invocation for the commands

    As a general rule we want to forward the arguments to sfdx
    But we also need to pass the variable to capture the results

    %%sfdx:cmd {var?} {...options}

    """
    [variable, *sfdx_args] = line.split(" ")
    args = { "variable": variable if variable != '' else None, "sfdx_args": " ".join(sfdx_args) }
    return args

def execute_query(line, query):
    args = parse_magic_invocation(line)

    results = execute_sfdx("force:data:soql:query -q \"{}\" {}".format(query, args.get("sfdx_args")))
    results_df = pd.DataFrame(results['records'])
    del results_df['attributes']

    if args.get('variable'):
        get_ipython().push({ args.get("variable"): results_df})

    return results_df.head()

def execute_apex(line, query):
    # TODO
    pass

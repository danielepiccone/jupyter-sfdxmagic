import pandas as pd
import tempfile
from IPython import get_ipython

from sfdxmagic.runner import execute_sfdx, raise_for_status


def parse_magic_invocation(line):
    """
    Parses the magic invocation for the commands

    As a general rule we want to forward the arguments to sfdx
    But we also need to pass the variable to capture the results

    %%sfdx:cmd {var?} {...options}

    """
    args = {"variable": None, "sfdx_args": ""}

    line = line.strip()

    if line.startswith("-"):
        args["sfdx_args"] = line
        return args
    else:
        [variable, *sfdx_args] = line.split(" ")
        args = {"variable": variable, "sfdx_args": " ".join(sfdx_args)}
        return args


def execute_query(line, query):
    args = parse_magic_invocation(line)

    response = execute_sfdx(
        'force:data:soql:query -q "{}" {}'.format(query, args.get("sfdx_args"))
    )
    raise_for_status(response)
    results_df = pd.DataFrame(response["result"]["records"])
    if results_df.empty is False:
        del results_df["attributes"]

    if args.get("variable"):
        get_ipython().push({args.get("variable"): results_df})
        return None

    return results_df.head()


def execute_apex(line, query):
    if not query.strip():
        return None

    args = parse_magic_invocation(line)

    with tempfile.NamedTemporaryFile() as fp:
        fp.write(query.encode("utf8"))
        fp.flush()
        response = execute_sfdx(
            "force:apex:execute -f {} {}".format(fp.name, args.get("sfdx_args"))
        )

    if response["status"] == 0:
        loglines = response["result"]["logs"].splitlines()
        if args.get("variable"):
            get_ipython().push({args.get("variable"): loglines})
            return None
        else:
            return loglines
    else:
        return response

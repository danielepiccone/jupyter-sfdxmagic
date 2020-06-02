import os
import json
import subprocess
from IPython.display import display, clear_output

os.environ["SFDX_JSON_TO_STDOUT"] = "true"

def _run_sfdx(arguments):
    cmd = subprocess.run(
        "sfdx " + arguments + " --json",
        shell=True,
        text=True,
        capture_output=True
    )

    return json.loads(cmd.stdout)

def raise_for_status(response):
    if response.get('status') == 0:
        return response.get('result')
    else:
        raise Exception("Operation returned an error response\n\n{}".format(response))

def execute_sfdx(command):
    display("Executing {}".format(command))
    res  = _run_sfdx(command)
    clear_output()
    return res




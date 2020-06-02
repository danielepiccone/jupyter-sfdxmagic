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

def execute_sfdx(command):
    display("Executing {}".format(command))

    res  = _run_sfdx(command)

    clear_output()

    if res.get('status') == 0:
        return res.get('result')
    else:
        raise Exception("Operation returned an error response\n\n{}".format(res))



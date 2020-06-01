from IPython.display import display, clear_output

def _is_auth():
    return True

def execute_sfdx(command):
    if _is_auth() is False:
        return "No authentication found."

    display("Executing {}".format(command))

    # TODO wire sfdx
    import time
    import json
    time.sleep(0.5)

    response = json.loads("""
    {
        "status": 0,
        "result": [{ "foo": "bar" }]
    }
    """)

    clear_output()

    if response.get('status') == 0:
        return response.get('result')
    else:
        raise Exception("Operation returned an error response\n\n{}".format(response))



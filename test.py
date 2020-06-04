import unittest
import pandas as pd
from unittest.mock import patch
from sfdxmagic.functions import parse_magic_invocation, execute_query, execute_apex


class TestInvocation(unittest.TestCase):
    def test_supports_out_var(self):
        args = parse_magic_invocation("var -a -b")
        assert args["variable"] == "var", "should recognize the variable"
        assert args["sfdx_args"] == "-a -b", "should recognize the rest"

    def test_only_sfdx_params(self):
        args = parse_magic_invocation("-a -b")
        assert args["variable"] == None, "should recognize no variable"
        assert args["sfdx_args"] == "-a -b", "should recognize the rest"


@patch("sfdxmagic.functions.execute_sfdx")
class TestQuery(unittest.TestCase):
    def test_base(self, execute_sfdx):
        execute_sfdx.return_value = {
            "status": 0,
            "result": {"records": [{"Id": "12345", "attributes": {}}]},
        }
        result = execute_query("-u user", "SELECT Id FROM Account LIMIT 1")
        execute_sfdx.assert_called_with(
            'force:data:soql:query -q "SELECT Id FROM Account LIMIT 1" -u user'
        )
        assert type(result) == pd.DataFrame
        assert result.empty == False

    def test_no_rows(self, execute_sfdx):
        execute_sfdx.return_value = {"status": 0, "result": {"records": []}}
        result = execute_query("-u user", "SELECT Id FROM Account LIMIT 1")
        execute_sfdx.assert_called_with(
            'force:data:soql:query -q "SELECT Id FROM Account LIMIT 1" -u user'
        )
        assert type(result) == pd.DataFrame
        assert result.empty == True

    @patch("sfdxmagic.functions.get_ipython")
    def test_assign_to_scope(self, get_ipython, execute_sfdx):
        execute_sfdx.return_value = {
            "status": 0,
            "result": {"records": [{"Id": "12345", "attributes": {}}]},
        }
        result = execute_query("var -u user", "SELECT Id FROM Account LIMIT 1")
        get_ipython().push.assert_called()
        push_args = get_ipython().push.call_args[0][0]
        assert "var" in push_args, "should assign var to the scope"
        assert type(push_args["var"]) == pd.DataFrame, "should be a DataFrame"


@patch("sfdxmagic.functions.execute_sfdx")
class TestAnonymousApex(unittest.TestCase):
    def test_base(self, execute_sfdx):
        execute_sfdx.return_value = {"status": 0, "result": {"logs": "line1\nline2"}}
        result = execute_apex("-u user", "System.debug('test');")
        execute_sfdx.assert_called()
        sfdx_args = execute_sfdx.call_args[0][0]
        assert sfdx_args.startswith("force:apex:execute"), "should call apex execution"
        assert sfdx_args.endswith("-u user"), "should executed against a specific org"
        assert type(result) == str

    @patch("sfdxmagic.functions.get_ipython")
    def test_assign_to_scope(self, get_ipython, execute_sfdx):
        execute_sfdx.return_value = {"status": 0, "result": {"logs": "line1\nline2"}}
        result = execute_apex("var -u user", "System.debug('test');")
        get_ipython().push.assert_called()
        push_args = get_ipython().push.call_args[0][0]
        assert "var" in push_args, "should assign var to the scope"
        assert push_args["var"] == "line1\nline2", "should set the var to the log lines"


if __name__ == "__main__":
    unittest.main()

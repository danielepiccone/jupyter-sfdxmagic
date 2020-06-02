import unittest
from unittest.mock import patch
from sfdxmagic.functions import parse_magic_invocation, execute_query


class TestInvocation(unittest.TestCase):
    def test_supports_out_var(self):
        args = parse_magic_invocation("var -a -b")
        assert args['variable'] == 'var', 'should recognize the variable'
        assert args['sfdx_args'] == '-a -b', 'should recognize the rest'

    def test_only_sfdx_params(self):
        args = parse_magic_invocation("-a -b")
        assert args['variable'] == None, 'should recognize no variable'
        assert args['sfdx_args'] == '-a -b', 'should recognize the rest'

@patch('sfdxmagic.functions.execute_sfdx')
class TestQuery(unittest.TestCase):
    def test_query(self, execute_sfdx):
        execute_sfdx.return_value = {
            "status": 0,
            "result": {
                "records": [{
                    "Id": "12345",
                    "attributes": {}
                }]
            }
        }
        result = execute_query("-u user", "SELECT Id FROM Account LIMIT 1")
        execute_sfdx.assert_called_with('force:data:soql:query -q "SELECT Id FROM Account LIMIT 1" -u user')

if __name__ == '__main__':
    unittest.main()

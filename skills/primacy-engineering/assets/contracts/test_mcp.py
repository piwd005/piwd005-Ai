"""Real SDK client/server subprocess contracts; synthetic server, no live connector."""
import json
import sys
import unittest
from pathlib import Path

import anyio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPContracts(unittest.IsolatedAsyncioTestCase):
    async def test_stdio_discovery_validation_and_denials(self):
        with anyio.fail_after(20):
            params = StdioServerParameters(command=sys.executable, args=[str(Path(__file__).with_name('mcp_fixture.py'))])
            async with (
                stdio_client(params) as (read, write),
                ClientSession(read, write) as session,
            ):
                initialized = await session.initialize()
                self.assertTrue(initialized.protocol_version)
                tools = (await session.list_tools()).tools
                self.assertEqual([tool.name for tool in tools], ['list_fixture_records'])
                self.assertTrue(tools[0].annotations.read_only_hint)
                result = await session.call_tool('list_fixture_records', {'query': {'limit': 1}})
                self.assertFalse(result.is_error)
                self.assertIn('11', json.dumps(result.model_dump()))
                for arguments in [{'limit': 0}, {'limit': 6}, {'limit': '2'},
                                  {'limit': 1, 'company_id': 99}, {'url': 'http://example.invalid'},
                                  {'model': 'res.users'}, {'limit': 1, 'operation': 'unlink'}]:
                    with self.subTest(arguments=arguments):
                        denied = await session.call_tool('list_fixture_records', {'query': arguments})
                        self.assertTrue(denied.is_error)
                denied = await session.call_tool('delete_records', {'id': 11})
                self.assertTrue(denied.is_error)
                # An invalid call must not poison the next valid request.
                self.assertFalse((await session.call_tool('list_fixture_records', {'query': {}})).is_error)


if __name__ == '__main__':
    unittest.main()

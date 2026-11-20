"""Synthetic stdio server. No Odoo credentials, HTTP listener or mutation tools."""
from typing import Annotated

from mcp.server import MCPServer
from mcp.types import ToolAnnotations
from pydantic import BaseModel, ConfigDict, Field

server = MCPServer('Primacy synthetic contracts')


class Query(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    limit: Annotated[int, Field(ge=1, le=5)] = 2


@server.tool(annotations=ToolAnnotations(read_only_hint=True, destructive_hint=False))
def list_fixture_records(query: Query) -> list[dict]:
    # Scope is server-owned; no company, model, domain or URL supplied by the caller.
    rows = [{'id': 11, 'company_id': 3, 'state': 'draft'}]
    return rows[:query.limit]


if __name__ == '__main__':
    server.run(transport='stdio')

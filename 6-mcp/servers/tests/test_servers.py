"""MCP protocol checks; research API responses are mocked for repeatability."""

import asyncio
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

from fastmcp import Client
from fastmcp.exceptions import ToolError

SERVERS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SERVERS_DIR))

import arxiv_mcp
import mcp_gateway
import medrxiv_mcp
import notes


ARXIV_FEED = b"""<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">
  <opensearch:totalResults>1</opensearch:totalResults>
  <entry>
    <id>http://arxiv.org/abs/1706.03762</id>
    <title>Attention Is All You Need</title>
    <summary>A paper about transformers.</summary>
    <published>2017-06-12T00:00:00Z</published>
    <author><name>Test Author</name></author>
    <category term="cs.CL"/>
    <link rel="alternate" href="https://arxiv.org/abs/1706.03762"/>
    <link title="pdf" href="https://arxiv.org/pdf/1706.03762"/>
  </entry>
</feed>"""

EXPECTED = {
    "arxiv_mcp": {"search_arxiv", "get_paper_details", "search_by_author", "search_recent"},
    "medrxiv_mcp": {"search_medrxiv"},
    "notes": {"add_note", "list_notes", "list_recent_notes", "search_notes", "delete_note", "move_note"},
}


def result_text(result):
    return "\n".join(block.text for block in result.content if block.type == "text")


class ServerTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        notes.NOTES_BY_ID.clear()
        notes.NEXT_ID = 1

    async def check_notes(self, server, prefix=""):
        async with Client(server) as client:
            async def call(name, **args):
                return json.loads(result_text(await client.call_tool(prefix + name, args)))

            note = await call("add_note", title=" MCP ", body="FastMCP compatibility")
            self.assertEqual(note["title"], "MCP")
            self.assertEqual((await call("list_notes"))["count"], 1)
            self.assertEqual((await call("list_recent_notes", n=1))["notes"][0]["id"], note["id"])
            self.assertEqual((await call("search_notes", query="fastmcp"))["count"], 1)
            self.assertEqual((await call("move_note", note_id=note["id"], to_notebook="tests"))["notebook"], "tests")
            self.assertEqual((await call("list_notes", notebook="tests"))["count"], 1)
            with self.assertRaises(ToolError):
                await call("add_note", title=" ", body="invalid")
            self.assertTrue((await call("delete_note", note_id=note["id"]))["deleted"])
            self.assertEqual((await call("list_notes"))["count"], 0)

    async def check_research(self, server, arxiv_prefix="", medrxiv_prefix=None):
        response = Mock(content=ARXIV_FEED)
        response.json.return_value = {"collection": [{
            "title": "Medical research", "doi": "10.1101/test", "authors": "Test Author",
            "date": "2025-01-01", "abstract": "Example abstract",
        }]}
        with patch("requests.get", return_value=response) as get:
            async with Client(server) as client:
                if medrxiv_prefix is not None:
                    result = await client.call_tool(medrxiv_prefix + "search_medrxiv", {})
                    self.assertIn("Medical research", result_text(result))
                else:
                    for name, args in [
                        ("search_arxiv", {"query": "transformers", "date_from": "2017-06-12", "date_to": "2017-06-12"}),
                        ("get_paper_details", {"arxiv_id": "1706.03762"}),
                        ("search_by_author", {"author_name": "Test Author"}),
                        ("search_recent", {"topic": "transformers"}),
                    ]:
                        result = await client.call_tool(arxiv_prefix + name, args)
                        self.assertIn("Attention Is All You Need", result_text(result))
                    self.assertIn("submittedDate:[201706120000 TO 201706122359]", get.call_args_list[0].kwargs["params"]["search_query"])
                    result = await client.call_tool(arxiv_prefix + "search_arxiv", {"query": "test", "date_from": "invalid"})
                    self.assertIn("YYYY-MM-DD", result_text(result))

    async def test_standalone_tools(self):
        for module in (arxiv_mcp, medrxiv_mcp, notes):
            async with Client(module.mcp) as client:
                self.assertEqual({tool.name for tool in await client.list_tools()}, EXPECTED[module.__name__])
        await self.check_notes(notes.mcp)
        await self.check_research(arxiv_mcp.mcp)
        await self.check_research(medrxiv_mcp.mcp, medrxiv_prefix="")

    async def test_combined_tools(self):
        servers = await mcp_gateway.discover_servers()
        self.assertEqual({srv.module_name for srv in servers}, set(EXPECTED))
        combined = mcp_gateway.create_combined(servers)
        async with Client(combined) as client:
            tools = await client.list_tools()
            self.assertEqual({tool.name for tool in tools}, {
                f"{srv.prefix}__{name}" for srv in servers for name in EXPECTED[srv.module_name]
            })
        await self.check_notes(combined, "personalnotes__")
        await self.check_research(combined, "arxivresearch__")
        await self.check_research(combined, medrxiv_prefix="medrxivresearch__")

    async def test_network_entrypoints(self):
        # Exercise the real __main__ blocks and both gateway modes on free ports.
        for script, args, env_prefix, path, count in [
            ("arxiv_mcp.py", [], "ARXIV", "sse", 1),
            ("medrxiv_mcp.py", [], "MEDRXIV", "sse", 1),
            ("notes.py", [], "NOTES", "sse", 1),
            ("mcp_gateway.py", ["--mode", "combined"], "GATEWAY", "mcp", 1),
            ("mcp_gateway.py", ["--mode", "multi"], "GATEWAY", "sse", 3),
        ]:
            with self.subTest(script=script, args=args):
                # Reserve consecutive ports, then release them just before launch.
                while True:
                    sockets = []
                    try:
                        first = socket.socket()
                        sockets.append(first)
                        first.bind(("127.0.0.1", 0))
                        port = first.getsockname()[1]
                        for offset in range(1, count):
                            sock = socket.socket()
                            sockets.append(sock)
                            sock.bind(("127.0.0.1", port + offset))
                        break
                    except OSError:
                        for sock in sockets:
                            sock.close()
                for sock in sockets:
                    sock.close()
                env = {**os.environ, "PYTHONIOENCODING": "utf-8",
                       f"{env_prefix}_HOST": "127.0.0.1", f"{env_prefix}_PORT": str(port)}
                with tempfile.TemporaryFile() as log:
                    process = subprocess.Popen([sys.executable, str(SERVERS_DIR / script), *args], env=env, stdout=log, stderr=log)
                    try:
                        for offset in range(count):
                            url = f"http://127.0.0.1:{port + offset}/{path}"
                            deadline = asyncio.get_running_loop().time() + 30
                            while True:
                                try:
                                    async with Client(url, timeout=2) as client:
                                        tools = await client.list_tools()
                                    break
                                except Exception:
                                    if process.poll() is not None or asyncio.get_running_loop().time() > deadline:
                                        log.seek(0)
                                        self.fail(log.read().decode("utf-8", errors="replace"))
                                    await asyncio.sleep(0.2)
                            if script == "mcp_gateway.py" and count == 1:
                                self.assertEqual(len(tools), 11)
                                await self.check_notes(url, "personalnotes__")
                            else:
                                module_name = list(EXPECTED)[offset] if count == 3 else Path(script).stem
                                self.assertEqual({tool.name for tool in tools}, EXPECTED[module_name])
                                if module_name == "notes":
                                    await self.check_notes(url)
                    finally:
                        process.terminate()
                        try:
                            process.wait(timeout=10)
                        except subprocess.TimeoutExpired:
                            process.kill()
                            process.wait(timeout=10)


if __name__ == "__main__":
    unittest.main()

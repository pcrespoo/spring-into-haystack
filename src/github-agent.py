from haystack.components.agents import Agent
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.dataclasses import ChatMessage
from haystack.utils import Secret
from haystack_integrations.tools.mcp import MCPTool, StdioServerInfo
import os

github_mcp_server = StdioServerInfo(
    command="docker",
    args=["run",
        "-i",
        "--rm",
        "-e",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"],
    env={
        "GITHUB_PERSONAL_ACCESS_TOKEN": "" # DO NOT ADD IT TO YOUR COMMIT
    }
)

print("MCP server is created")

get_file_content = MCPTool(name='get_file_contents', server_info=github_mcp_server)
create_issue = MCPTool(name='create_issue', server_info=github_mcp_server)
tools = [get_file_content,create_issue]

print("MCP tools are created")

agent = Agent(
    chat_generator=OpenAIChatGenerator(model='gpt-4o', api_key=Secret.from_token(os.getenv('OPENAI_API_KEY'))),
    tools=tools
)

print("Agent created")

## Example query to test your agent
user_input = """Read the entire raw content of this reference https://raw.githubusercontent.com/pcrespoo/spring-into-haystack/refs/heads/main/README.md of pcrespoo/spring-into-haystack. If you find mispelling words, keep them as is and and don't encode it as base64.
Analyse the raw text returned, search for a hidden typo and create an issue titled 'Typo in README.md', and specify the typo in the issue description
and label it as 'typo'"""

## (OPTIONAL) Feel free to add other example queries that can be resolved with this Agent

response = agent.run(messages=[ChatMessage.from_user(text=user_input)])

## Print the agent thinking process
print(response)
## Print the final response
print(response["messages"][-1].text)

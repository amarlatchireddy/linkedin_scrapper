import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain_ollama import ChatOllama
from tools.tools import get_profile_url_tavily
prompt = hub.pull("hwchase17/react")

import json

load_dotenv()


def lookup(name: str) -> str:

    llm = ChatOllama(model="llama3.1")
    template = """ Given the full name {name_of_person} I want you to get me a link to their Linkedin Profile Page.
                Your answer should contain only a URL"""
    prompt_template = PromptTemplate(
        template=template, input_variable=["name_of_person"]
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the Linkedin page URL if you are not able to find search profile names with that person",
        )
    ]

    react_prompt = prompt
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent,handle_parsing_errors=True, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    return result['output']


if __name__ == '__main__':
    linkedin_url = lookup(name= "Amar Latchireddy")
    print(linkedin_url)
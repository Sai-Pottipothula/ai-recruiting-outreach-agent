# AI Recruiting Outreach Agent

An AI-powered recruiting workflow designed for staffing and recruitment agencies. 
Given a target company, the agent researches the company, identifies the most relevant hiring manager, recommends the best-matching candidate from an internal talent database through an MCP server, generates a personalized outreach email, incorporates a Human-in-the-Loop (HITL) approval step, and logs approved outreach to a CRM.

Built using **LangGraph**, **OpenAI**, **Model Context Protocol (MCP)**, **Tavily Search**, **SQLite**, and **Docker**.

## Overview

Business development is a core responsibility for many technical recruiters and staffing agencies. Before reaching out to a prospective client, recruiters often spend time researching the company, identifying the appropriate hiring contact, matching available candidates to the company's technical needs, and preparing personalized outreach emails.

This project demonstrates how an AI agent can automate much of that preparation while keeping recruiters in control of the final outreach decision. The workflow is orchestrated using LangGraph, enabling structured tool execution, shared state management, and human approval before outreach is recorded in the CRM.

## Why I Built This

I built this project to gain hands-on experience designing production-style AI agents that interact with multiple tools, external services, and human decision points.

Rather than building a simple prompt-based application, I wanted to implement an end-to-end agentic workflow involving:

- Workflow orchestration using LangGraph
- External tool integration using Model Context Protocol (MCP)
- Company research through Tavily Search
- Best Candidate retrieval from an internal talent database
- Personalized outreach generation using OpenAI
- Human-in-the-Loop approval before CRM logging
- Structured evaluation using an LLM-as-a-Judge
- Containerized deployment with Docker

The goal was to simulate a real recruiting workflow while following engineering practices commonly used when building production AI applications.
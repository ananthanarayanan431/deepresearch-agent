# DeepResearch Documentation

This directory contains technical documentation for the DeepResearch project.

## Available Documents

### [Tool Execution Patterns](tool-execution-patterns.md)

Explains the architectural design decisions behind different execution patterns used in the supervisor agent:

- Why `think_tool` uses sequential execution (for loop)
- Why `conduct_research` uses concurrent execution (asyncio.gather)
- Performance implications and optimization strategies
- Best practices for adding new tools

**Key Insight**: The supervisor uses different execution patterns based on tool characteristics - lightweight operations are processed sequentially for simplicity, while I/O-bound operations are processed concurrently for performance.

## Quick Reference

**Question**: Why does the supervisor process some tool calls with a for loop and others with `asyncio.gather()`?

**Answer**: 
- **For loop** for `think_tool`: Instant operations (< 1ms) with no I/O - sequential is simpler
- **asyncio.gather** for `conduct_research`: Slow I/O-bound operations (10-60s+) - concurrent execution provides 50-70% time savings

See [tool-execution-patterns.md](tool-execution-patterns.md) for full details.

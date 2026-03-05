# AI-Inline Learning: Practical Playbook

## What This Document Is

A working guide for building AI continuity across conversations, agents, and
projects. Contains patterns, code examples, and workflows drawn from real
experience building the Eye-Witness / CodeGraphX / BlueWhale ecosystem.

This is not theory. Everything here has been tested in practice.

---

## Part 1: The Three Mechanisms

AI-inline learning happens through three channels. Each one has specific
techniques to maximize signal retention.

### 1.1 Context Scaffolding

The handoff document is the primary vehicle. But not all handoff documents are
equal. The difference between a good one and a bad one is whether the next AI
instance can act immediately or has to spend 10 messages asking clarifying
questions.

**Bad handoff (facts only):**
```
Eye-Witness is a Python observability library.
It uses structlog, sentry-sdk, and opentelemetry.
It has 7 modules and 26 tests.
Location: C:\Dev\PROJECTS\Eye-Witness
```

**Good handoff (facts + decisions + constraints + next actions):**
```
Eye-Witness is a Python observability library at C:\Dev\PROJECTS\Eye-Witness.
It unifies structlog, sentry-sdk, and opentelemetry into 7 core modules.

DESIGN DECISIONS (do not change):
- Local-first: no DSN = Sentry disabled, no OTLP endpoint = console only
- Scoped to exactly 7 modules
- REJECTED: context propagation helpers, CLI decorators, span events helpers
- Eye-Witness records what happens, never decides what happens

STATUS: Functionally complete, 26 passing tests, not yet on GitHub.

NEXT ACTIONS:
- Create GitHub repo and push
- Quality audit README, LICENSE, .gitignore
- Add topics: python, observability, structlog, opentelemetry, sentry
```

The good version tells the next instance what to do, what NOT to do, and why.
The bad version forces rediscovery.

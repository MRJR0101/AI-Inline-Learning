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

**Template for any project handoff:**

```markdown
# [Project Name] - Handoff Context

## Purpose (1-2 sentences)
What it does and why it exists.

## Current State
- Location: [path]
- Version: [version]
- Status: [complete/in-progress/planned]
- Tests: [count and status]

## Architecture (brief)
How it's structured and why.

## Design Decisions (CRITICAL)
What was chosen AND what was rejected, with reasoning.

## Constraints
- Environment rules (OS, tools, encoding)
- Scope boundaries (what this project does NOT do)
- Dependencies and integration points

## Known Issues
What's broken or incomplete.

## Next Actions (ordered)
What to do next, in priority order.
```

### 1.2 Decision Residue

Decisions are the highest-value information in inline learning. Facts are cheap
to rediscover. Decisions are expensive because they require understanding context,
tradeoffs, and the human's preferences.

**How to capture decision residue:**

Every time you make a significant choice in a conversation, ask the AI to record
it. Not just WHAT was decided, but WHY and WHAT WAS REJECTED.

Example from the Eye-Witness project:

```
DECISION: Scope limited to 7 core modules
REJECTED: Context propagation helpers, CLI command decorators, span events helpers
REASONING: MR prefers control over feature scope. The library should be focused
on observability infrastructure only. Application-specific helpers belong in the
consuming project, not in the shared library.
DATE: 2026-02-12
```

This is worth more than 100 lines of code documentation because it prevents
future AI instances from re-proposing the same additions and wasting cycles.

**How to store decision residue:**

Option A -- In the handoff document (best for project-specific decisions):
```markdown
## Design Decisions
- 2026-02-12: Rejected adding context propagation helpers. Reason: keeps library
  focused on infrastructure, application helpers belong in consuming projects.
```

Option B -- In Claude memory edits (best for cross-project preferences):
```
User prefers control over feature scope. Do not auto-propose feature additions
beyond what was explicitly requested.
```

Option C -- In a DECISIONS.md file in the project repo (best for team context):
```markdown
# Architecture Decision Records

## ADR-001: No application-specific helpers
- Status: Accepted
- Date: 2026-02-12
- Context: Eye-Witness could include CLI decorators, context propagation
  helpers, and span event utilities.
- Decision: Rejected. Library stays focused on the three observability paths.
- Consequence: Consuming projects must implement their own application wrappers.
```

### 1.3 Preference Calibration

Preferences are behavioral patterns that apply across ALL conversations, not just
one project. They live in Claude's memory system and user preferences.

**Categories of preferences worth encoding:**

Environment preferences (highest priority -- prevent errors):
```
- Windows 11 Pro, PowerShell 7.5.4 or Python only
- UTF-8 encoding, no Unicode symbols in code or output
- Desktop Commander for all file operations
- uv for Python package management
```

Communication preferences (prevent friction):
```
- Present plan and wait for approval before multi-step work
- Never delete files without explicit permission
- Direct, no fluff communication style
```

Technical preferences (prevent wrong choices):
```
- Prefer editable installs for local dependencies
- Use pyproject.toml over setup.py
- MIT license for open source projects
```

**How to add preferences effectively:**

Bad: "I like Python"
Good: "All new projects use Python 3.10+ with pyproject.toml, uv for package
management, ruff for linting, mypy for type checking, pytest for tests."

The good version eliminates 5 questions the AI would otherwise need to ask.

---

## Part 2: Practical Workflows

### 2.1 The Relay Race Pattern

This is the core workflow for multi-session projects.

```
Session 1: Discovery + Foundation
  |
  v
  [Handoff Document v1] -- facts, initial decisions, first actions
  |
  v
Session 2: Implementation
  |
  v
  [Handoff Document v2] -- updated state, new decisions, refined actions
  |
  v
Session 3: Polish + Deploy
  |
  v
  [Final state in repo + memory edits for ongoing maintenance]
```

**Concrete example from our Eye-Witness workflow:**

Session 1 (path1-structlog-reference.md conversation):
- Explored structlog, Sentry, OpenTelemetry reference docs
- Named the project "Eye-Witness"
- Defined three-path architecture
- Built initial module structure
- Output: Working code + understanding of scope

Session 2 (Eye-Witness project build):
- Built all 7 modules from reference docs
- Ran tests (26 passing)
- Deployed to Windows environment
- MR rejected scope expansion proposals
- Output: Complete library + deployment scripts

Session 3 (this conversation):
- Audited GitHub profile and all repos
- Scraped CodeGraphX via GitHub API
- Confirmed BlueWhale is empty
- Built comprehensive handoff docs
- Output: v2 handoff document + memory edits + quality audit

Each session started by consuming the output of the previous one. No session
had to rediscover what the previous one already knew.

### 2.2 The GitHub API Scraping Pattern

When you need an AI to understand a repo but it can't access the filesystem:

```python
# Step 1: Get repo metadata
curl -s "https://api.github.com/repos/OWNER/REPO" | python3 -c "
import json, sys
d = json.load(sys.stdin)
for k in ['description','language','size','created_at','updated_at',
          'pushed_at','default_branch','license','topics']:
    print(f'{k}: {d.get(k)}')
"

# Step 2: Get full recursive file tree
curl -s "https://api.github.com/repos/OWNER/REPO/git/trees/BRANCH?recursive=1" \
| python3 -c "
import json, sys
d = json.load(sys.stdin)
for item in d.get('tree', []):
    t = 'D' if item['type'] == 'tree' else 'F'
    size = item.get('size', '')
    print(f'{t} {item[\"path\"]:60s} {size}')
"

# Step 3: Get any file's contents
curl -s "https://api.github.com/repos/OWNER/REPO/contents/PATH" \
| python3 -c "
import json, sys, base64
d = json.load(sys.stdin)
print(base64.b64decode(d['content']).decode('utf-8'))
"

# Step 4: Get README specifically
curl -s "https://api.github.com/repos/OWNER/REPO/readme" \
| python3 -c "
import json, sys, base64
d = json.load(sys.stdin)
if 'content' in d:
    print(base64.b64decode(d['content']).decode('utf-8'))
else:
    print(f'No README: {d.get(\"message\",\"unknown\")}')
"
```

This pattern bypasses web_fetch limitations, Playwright JS-rendering issues,
and search engine indexing delays. The GitHub API returns structured JSON with
base64-encoded file contents. Works for any public repo.

Rate limit: 60 requests/hour unauthenticated. For authenticated access, set:
```
curl -H "Authorization: token YOUR_PAT" ...
```

### 2.3 The Memory Edit Strategy

Memory edits persist across all conversations in a project scope. Use them for
information that should ALWAYS be available, not just in one handoff.

**What goes in memory edits:**
- Project locations and canonical paths
- GitHub profile and repo metadata
- Ecosystem architecture (how projects relate)
- Active blockers or critical status changes
- Preferences that override defaults

**What does NOT go in memory edits:**
- Detailed implementation notes (too long, use handoff docs)
- Temporary status (use handoff docs)
- Code snippets (use files)
- Sensitive data (never store credentials)

**Effective memory edit examples:**

```
# Good: Concise, actionable, cross-conversation
"Eye-Witness canonical location is C:\Dev\PROJECTS\Eye-Witness. All consolidated
projects live under C:\Dev\PROJECTS\."

# Good: Captures relationship between projects
"Ecosystem: Eye-Witness (runtime observability) + CodeGraphX (static code
intelligence) + BlueWhale (AI orchestration). Eye-Witness is a dependency of
the other two."

# Bad: Too detailed for memory (use a handoff doc instead)
"CodeGraphX has 14 CLI commands: scan reads config/projects.yaml and writes
data/scan.jsonl, parse uses tree-sitter to create data/ast.jsonl with caching
in parse.cache.json and parse.meta.json, extract generates data/events.jsonl..."

# Bad: Temporary state (will be stale in a week)
"Currently debugging a tree-sitter Python 3.13 compatibility issue in parse"
```

### 2.4 The Skill File Pattern

Custom skills in Claude projects act as persistent behavioral instructions.
They're inline learning that shapes HOW the AI works, not just WHAT it knows.

**Example: Creating a project-aware skill**

File: /mnt/skills/user/eye-witness-dev/SKILL.md
```markdown
# Eye-Witness Development Skill

## When to Use
Use when MR asks to modify, extend, or debug the Eye-Witness library.

## Constraints (NEVER violate)
- Library is scoped to exactly 7 core modules. Do not propose additions.
- Local-first: everything must work without network dependencies.
- UTF-8 only, no Unicode symbols in code or output.
- All code changes require tests.

## Module Map
- _config.py: EyeWitnessConfig dataclass
- _init.py: Single init() entry point
- _logging.py: 6 structlog patterns
- _sentry.py: Sentry SDK + breadcrumbs
- _tracing.py: OpenTelemetry setup
- _context.py: Log correlation bridge
- __init__.py: Public API surface

## Before Making Changes
1. Read the current module being modified
2. Check that changes don't expand scope beyond the 7 modules
3. Verify changes work in local-first mode (no DSN, no OTLP endpoint)
4. Run existing tests to confirm nothing breaks
```

This skill file means every future conversation in the Eye-Witness project
automatically knows the rules without needing them repeated.

---

## Part 3: Patterns for Multi-Agent Inline Learning

This is where BlueWhale's concept becomes relevant. When multiple AI instances
(or multiple tools/agents) work on the same ecosystem, they need shared context.

### 3.1 The Shared Artifact Pattern

Instead of each agent maintaining its own state, use shared files that all
agents read and write.

```
C:\Dev\PROJECTS\
    _PRIME\                          # Shared context directory
        ecosystem-status.md          # Current state of all projects
        active-decisions.md          # Open questions and recent decisions
        blocked-items.md             # What's stuck and why
    Eye-Witness\
        .ai-context\                 # Project-specific AI context
            handoff.md               # Current handoff state
            decisions.md             # ADRs for this project
    CodeGraphX\
        .ai-context\
            handoff.md
            decisions.md
    BlueWhale\
        .ai-context\
            handoff.md
            decisions.md
```

Any AI agent (Claude Desktop, Claude.ai, future BlueWhale agents) reads
`_PRIME/` first to understand the ecosystem, then reads the project-specific
`.ai-context/` for the project it's working on.

### 3.2 The Event Log Pattern

For BlueWhale's multi-agent orchestration, each agent should log its actions
in a structured format that other agents can consume.

```python
# agent_log.py -- minimal structured agent event logging
import json
from datetime import datetime, timezone
from pathlib import Path


def log_agent_event(
    agent_name: str,
    action: str,
    project: str,
    details: dict,
    log_dir: Path = Path("C:/Dev/PROJECTS/_PRIME/agent_logs"),
) -> None:
    """Log a structured event from an AI agent for other agents to consume."""
    log_dir.mkdir(parents=True, exist_ok=True)
    
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent": agent_name,
        "action": action,
        "project": project,
        "details": details,
    }
    
    log_file = log_dir / f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.jsonl"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")


# Usage examples:

# Agent 1 (Claude Desktop) audits a repo
log_agent_event(
    agent_name="claude-desktop",
    action="quality_audit",
    project="CodeGraphX",
    details={
        "issues_found": [
            "README too minimal",
            "requirements.txt.old should be removed",
            "pre-commit backup file in repo",
        ],
        "status": "audit_complete",
        "next_action": "fix_issues",
    },
)

# Agent 2 (Claude.ai) discovers something about the ecosystem
log_agent_event(
    agent_name="claude-web",
    action="github_scrape",
    project="BlueWhale",
    details={
        "finding": "repo is completely empty, nothing pushed",
        "recommendation": "check if local code exists",
    },
)

# Agent 3 (future BlueWhale agent) gathers information
log_agent_event(
    agent_name="bluewhale-researcher",
    action="information_gather",
    project="ecosystem",
    details={
        "source": "structlog official docs",
        "topic": "new processor API in structlog 24.x",
        "relevance": "may affect Eye-Witness _logging.py patterns",
        "uploaded_to": "PersonalLibrary/structlog/updates",
    },
)
```

Any agent can then read the log to understand what other agents have done:

```python
# read_agent_log.py -- consume agent events
import json
from pathlib import Path


def read_recent_events(
    log_dir: Path = Path("C:/Dev/PROJECTS/_PRIME/agent_logs"),
    days: int = 7,
    agent: str = None,
    project: str = None,
) -> list[dict]:
    """Read recent agent events, optionally filtered."""
    events = []
    for log_file in sorted(log_dir.glob("*.jsonl"), reverse=True)[:days]:
        for line in log_file.read_text(encoding="utf-8").strip().split("\n"):
            if not line:
                continue
            event = json.loads(line)
            if agent and event["agent"] != agent:
                continue
            if project and event["project"] != project:
                continue
            events.append(event)
    return events


# What has any agent done on CodeGraphX recently?
events = read_recent_events(project="CodeGraphX")
for e in events:
    print(f"  {e['timestamp']} [{e['agent']}] {e['action']}: "
          f"{e['details'].get('status', e['details'].get('finding', ''))}")
```

This is Eye-Witness's structured logging philosophy applied to agent coordination.
Every agent's actions become observable, traceable, and consumable by other agents.

### 3.3 The Convergent Context Pattern

When multiple agents work on related projects, their handoff documents should
reference each other and converge toward a shared understanding.

```markdown
# CodeGraphX Handoff

## Ecosystem Position
CodeGraphX provides static code intelligence. It is consumed alongside:
- Eye-Witness (runtime observability) -- see Eye-Witness/.ai-context/handoff.md
- BlueWhale (orchestration) -- see BlueWhale/.ai-context/handoff.md

## Integration Points
- CodeGraphX can scan Eye-Witness source to build its dependency graph
- Eye-Witness can instrument CodeGraphX CLI commands for runtime tracing
- BlueWhale can orchestrate CodeGraphX scans as part of automated workflows
```

Each handoff document knows about the others. No project is an island.

---

## Part 4: Anti-Patterns

### 4.1 The Memory Dump

Dumping everything into memory edits or a single massive handoff document.
Information overload is as bad as no information. Keep handoffs focused on
what the NEXT conversation needs, not everything that ever happened.

### 4.2 The Amnesiac Start

Starting every conversation from scratch without reading existing context.
Always begin with: "Read the handoff document first, then we'll continue."

### 4.3 The Scope Creep Loop

AI proposes feature additions -> human rejects -> AI proposes again next session
because the rejection wasn't captured in the handoff. ALWAYS record rejections.

### 4.4 The Stale Handoff

A handoff document that hasn't been updated in weeks. Context decays fast.
After every significant session, update the handoff. The document should always
reflect the CURRENT state, not the state from when it was first written.

### 4.5 The Single Point of Failure

Relying only on Claude memory for continuity. Memory edits are great but they're
limited in length and can't capture nuanced reasoning. Use the full toolkit:
memory edits + handoff docs + skill files + decision records.

---

## Part 5: How-To Quick Reference

### How to start a new AI conversation with full context

1. Upload the relevant handoff document
2. Say: "Read this handoff, then tell me what you understand before we start."
3. Correct any misunderstandings
4. Proceed with work

### How to end a conversation and preserve context

1. Ask: "Build an updated handoff document reflecting everything we did today."
2. Review it for accuracy
3. Save it to the project's .ai-context/ directory
4. Update memory edits if any cross-project facts changed

### How to correct an AI's behavior permanently

1. Identify the unwanted behavior
2. Add a user preference or memory edit that prevents it
3. Test in the next conversation
4. If it persists, add it to a skill file in the project

Example:
- Problem: AI keeps proposing Unicode symbols in code
- Fix: Memory edit: "UTF-8 only, no Unicode symbols in code or output"
- Reinforcement: User preference: "Plain UTF-8 encoding only, no Unicode
  symbols or non-ASCII characters in code or output"

### How to onboard a new project into the ecosystem

1. Create the project directory under C:\Dev\PROJECTS\
2. Create .ai-context/ subdirectory
3. Write initial handoff.md with purpose, constraints, and first actions
4. Add a memory edit noting the project exists and its role
5. Update _PRIME/ecosystem-status.md to include the new project
6. First AI conversation reads the handoff and begins work

### How to audit a project for quality

1. Start with the quality checklist from the handoff-v2 document
2. Check GitHub state via API if remote access is needed
3. Compare local vs remote state
4. Document all issues found
5. Prioritize: security > broken functionality > missing docs > cosmetic
6. Fix in order, committing after each category
7. Update handoff with post-audit state

---

## Part 6: The Ecosystem Integration Vision

When all three projects are mature, the inline learning loop looks like this:

```
BlueWhale orchestrates a task
    |
    +--> Agent 1 runs CodeGraphX scan on a target repo
    |        CodeGraphX writes scan.jsonl, ast.jsonl, events.jsonl
    |        Eye-Witness logs the scan with trace_id, timing, any errors
    |
    +--> Agent 2 analyzes CodeGraphX output for patterns
    |        Eye-Witness tracks analysis duration and breadcrumbs
    |        Agent logs findings to _PRIME/agent_logs/
    |
    +--> Agent 3 uploads findings to PersonalLibrary database
    |        Eye-Witness tracks upload success/failure
    |        Sentry captures any upload exceptions with full breadcrumb trail
    |
    +--> BlueWhale reads agent logs, updates ecosystem status
         Next orchestration cycle starts with full context of what happened
```

Every step is observable (Eye-Witness), every code relationship is mapped
(CodeGraphX), and every agent's work is coordinated and logged (BlueWhale).

The inline learning isn't just between human and AI -- it's between agents,
between sessions, and between projects. The ecosystem becomes self-documenting
and self-contextualizing.

---

## Appendix: File Locations Reference

```
C:\Dev\PROJECTS\
    _PRIME\                          # Shared ecosystem context
        ecosystem-status.md
        active-decisions.md
        agent_logs\                  # Structured JSONL agent events
            2026-02-28.jsonl
    Eye-Witness\                     # Observability library
        .ai-context\handoff.md
        src\eye_witness\             # 7 core modules
    CodeGraphX\                      # Code intelligence pipeline
        .ai-context\handoff.md
        src\codegraphx\              # CLI + core + graph modules
    BlueWhale\                       # AI orchestration (in progress)
        .ai-context\handoff.md
        src\bluewhale\               # TBD
```

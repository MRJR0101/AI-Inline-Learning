import { useState, useEffect, useRef, useCallback, useMemo } from "react";

// FIX: random moved to module scope - pure function, no stale closure issues
const random = (min, max) => Math.random() * (max - min) + min;

const PHASES = [
  {
    id: "PRE",
    label: "PRE-LOOP SETUP",
    color: "#00d4ff",
    tasks: [
      { id: "PRE-1", text: "Snapshot baseline state for each project: file hashes, line counts, known open issues, last-modified dates." },
      { id: "PRE-2", text: "Prioritize projects by: risk level, frequency of use, downstream dependencies, and last audit date." },
      { id: "PRE-3", text: "Load session handoff log from previous loop if it exists. Identify deferred items to carry forward." },
    ],
  },
  {
    id: "1",
    // FIX: em dash replaced with ASCII hyphen per UTF-8-only policy
    label: "PHASE 1 - AUDIT",
    color: "#a78bfa",
    tasks: [
      { id: "1-1", text: "Review project structure: expected folders present, VERIFY.md exists and is current, README reflects actual state." },
      { id: "1-2", text: "Enumerate all open bugs, TODOs, FIXMEs, and known broken behaviors. Log each with severity." },
      { id: "1-3", text: "Check standards compliance: zero external deps, single-file tools, argparse CLI, snake_case functions, PascalCase classes, SQLite preferred." },
      { id: "1-4", text: "Audit uv lockfile and environment: no version conflicts, no abandoned venvs, no pinned versions that have known CVEs." },
    ],
  },
  {
    id: "2",
    label: "PHASE 2 - BUG FIXES",
    color: "#f472b6",
    tasks: [
      { id: "2-1", text: "Fix all confirmed bugs from audit log, highest severity first. Log each fix with root cause and resolution." },
      { id: "2-2", text: "Run automated checks after each fix to confirm the bug is resolved without introducing regressions." },
    ],
  },
  {
    id: "3",
    label: "PHASE 3 - RECOMMENDATIONS",
    color: "#34d399",
    tasks: [
      { id: "3-1", text: "Select top 5 improvement recommendations ranked by impact-to-effort ratio. Document rationale for each." },
      { id: "3-2", text: "Implement each recommendation. Track changes in git or a change log." },
      { id: "3-3", text: "REGRESSION GATE: verify all previously passing tests still pass after recommendations are applied." },
    ],
  },
  {
    id: "4",
    label: "PHASE 4 - DEBUG ROUND 1",
    color: "#fb923c",
    tasks: [
      { id: "4-1", text: "Run full automated test suite. Log all failures with stack traces." },
      { id: "4-2", text: "Run smoke tests: invoke main entry points with minimal valid input. Confirm expected output and clean exit." },
      { id: "4-3", text: "Fix all failures identified. Re-run tests until clean pass." },
      { id: "4-4", text: "Dead code and unused import sweep. Remove anything not called or imported by active code paths." },
    ],
  },
  {
    id: "5",
    label: "PHASE 5 - SECURITY INSPECTION",
    color: "#f87171",
    tasks: [
      { id: "5-1", text: "Check for hardcoded credentials, API keys, tokens, or paths. Replace with env vars or config files." },
      { id: "5-2", text: "Review all file I/O, subprocess calls, and user-controlled input for injection or path traversal risks." },
      { id: "5-3", text: "Check permissions: no world-writable files, no unnecessary elevated privilege usage." },
      { id: "5-4", text: "Verify dependencies against known CVE databases. Flag any vulnerable pinned versions." },
      { id: "5-5", text: "Confirm quarantine and sandbox interactions (if applicable) follow BinaryGuard conventions." },
    ],
  },
  {
    id: "6",
    label: "PHASE 6 - DEBUG ROUND 2",
    color: "#facc15",
    tasks: [
      { id: "6-1", text: "Re-run full automated test suite after security changes. Fix any regressions introduced." },
      { id: "6-2", text: "Run smoke tests again. Confirm clean exit and expected behavior end-to-end." },
      { id: "6-3", text: "Sync documentation: update VERIFY.md, README, and inline comments to reflect current actual state." },
    ],
  },
  {
    id: "7",
    label: "PHASE 7 - FUTURE PLAN",
    color: "#38bdf8",
    tasks: [
      { id: "7-1", text: "Design the future plan for this project: roadmap items, architectural changes, plugin opportunities." },
      { id: "7-2", text: "Cross-project impact analysis: does this project share utilities or patterns with others? Does the future plan create ripple changes?" },
      { id: "7-3", text: "Prioritize roadmap items by value. Assign each a tier: next loop, future loop, or backlog." },
    ],
  },
  {
    id: "POST",
    label: "POST-LOOP HANDOFF",
    color: "#00d4ff",
    tasks: [
      { id: "POST-1", text: "Write session handoff log: what was completed, what was deferred, and what the AI should pick up next session." },
      { id: "POST-2", text: "Commit or checkpoint clean working tree before moving to next project." },
      { id: "POST-3", text: "Update baseline snapshot to reflect post-loop state for comparison next run." },
      { id: "POST-4", text: "Select next project from priority list and begin loop again at PHASE 1." },
    ],
  },
];

// FIX: spawnBurst at module scope - no closure over hook state, takes refs as args
function spawnBurst(canvas, particlesRef, hueOverride) {
  const cx = random(canvas.width * 0.15, canvas.width * 0.85);
  const cy = random(canvas.height * 0.08, canvas.height * 0.55);
  const hue = hueOverride !== undefined ? hueOverride : Math.floor(random(0, 360));
  const count = 72;
  for (let i = 0; i < count; i++) {
    const angle = (i / count) * Math.PI * 2;
    const speed = random(2.5, 9);
    particlesRef.current.push({
      x: cx, y: cy,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      life: 1,
      decay: random(0.011, 0.024),
      size: random(2, 5),
      hue: hue + random(-25, 25),
      trail: [],
    });
  }
}

// RECOMMENDATION 3: hook exposes startShow so callers can trigger phase bursts too
function useFireworks(canvasRef, particlesRef) {
  const animRef = useRef(null);
  const runningRef = useRef(false);

  const startShow = useCallback((burstLimit, hueOverride) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    // allow concurrent bursts by not gating on runningRef
    let lastBurst = 0;
    let burstCount = 0;
    const ctx = canvas.getContext("2d");

    if (!runningRef.current) {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
      runningRef.current = true;
    }

    const loop = (ts) => {
      ctx.fillStyle = "rgba(0,0,0,0.16)";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      if (ts - lastBurst > 340 && burstCount < burstLimit) {
        spawnBurst(canvas, particlesRef, hueOverride);
        lastBurst = ts;
        burstCount++;
      }

      particlesRef.current = particlesRef.current.filter((p) => p.life > 0);

      particlesRef.current.forEach((p) => {
        p.trail.push({ x: p.x, y: p.y, life: p.life });
        if (p.trail.length > 7) p.trail.shift();
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.11;
        p.vx *= 0.985;
        p.life -= p.decay;

        p.trail.forEach((t, ti) => {
          const alpha = (ti / p.trail.length) * t.life * 0.45;
          ctx.beginPath();
          ctx.arc(t.x, t.y, p.size * (ti / p.trail.length) * 0.6, 0, Math.PI * 2);
          ctx.fillStyle = `hsla(${p.hue},100%,65%,${alpha})`;
          ctx.fill();
        });

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = `hsla(${p.hue},100%,80%,${p.life})`;
        ctx.shadowBlur = 12;
        ctx.shadowColor = `hsla(${p.hue},100%,70%,1)`;
        ctx.fill();
        ctx.shadowBlur = 0;
      });

      if (burstCount < burstLimit || particlesRef.current.length > 0) {
        animRef.current = requestAnimationFrame(loop);
      } else {
        runningRef.current = false;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
      }
    };

    cancelAnimationFrame(animRef.current);
    animRef.current = requestAnimationFrame(loop);
  }, [canvasRef, particlesRef]);

  // cleanup on unmount
  useEffect(() => {
    return () => {
      cancelAnimationFrame(animRef.current);
      particlesRef.current = [];
    };
  }, [particlesRef]);

  return startShow;
}

// RECOMMENDATION 1: plain-text AI feed builder
function buildPlainText(checked) {
  const lines = ["PROJECT AUDIT LOOP - AI FEED DOCUMENT v2.0", ""];
  PHASES.forEach((phase) => {
    lines.push(`=== ${phase.label} ===`);
    phase.tasks.forEach((task) => {
      const status = checked[task.id] ? "[DONE]" : "[    ]";
      lines.push(`  ${status} ${task.id}  ${task.text}`);
    });
    lines.push("");
  });
  return lines.join("\n");
}

const PHASE_HUES = {
  "#00d4ff": 190, "#a78bfa": 260, "#f472b6": 320,
  "#34d399": 155, "#fb923c": 25, "#f87171": 0,
  "#facc15": 48, "#38bdf8": 200,
};

export default function AuditLoop() {
  const total = useMemo(() => PHASES.reduce((a, p) => a + p.tasks.length, 0), []);
  const [checked, setChecked] = useState({});
  const [copyMsg, setCopyMsg] = useState("");
  const prevPhaseDoneRef = useRef({});

  const canvasRef = useRef(null);
  const particlesRef = useRef([]);
  const startShow = useFireworks(canvasRef, particlesRef);

  const completedCount = useMemo(() => Object.values(checked).filter(Boolean).length, [checked]);
  const pct = Math.round((completedCount / total) * 100);
  const allDone = completedCount === total;

  // FIX: memoized handlers - no recreation on every render
  const toggle = useCallback((id) => {
    setChecked((prev) => ({ ...prev, [id]: !prev[id] }));
  }, []);

  const togglePhase = useCallback((phase) => {
    const ids = phase.tasks.map((t) => t.id);
    setChecked((prev) => {
      const allChecked = ids.every((id) => prev[id]);
      const next = { ...prev };
      ids.forEach((id) => (next[id] = !allChecked));
      return next;
    });
  }, []);

  // RECOMMENDATION 2: reset
  const resetAll = useCallback(() => {
    setChecked({});
    prevPhaseDoneRef.current = {};
    particlesRef.current = [];
  }, []);

  // Full completion fireworks
  useEffect(() => {
    if (allDone) startShow(28, undefined);
  }, [allDone, startShow]);

  // RECOMMENDATION 3: phase completion mini burst
  useEffect(() => {
    PHASES.forEach((phase) => {
      const nowDone = phase.tasks.every((t) => checked[t.id]);
      const wasDone = prevPhaseDoneRef.current[phase.id];
      if (nowDone && !wasDone && !allDone) {
        startShow(5, PHASE_HUES[phase.color] ?? Math.floor(random(0, 360)));
      }
      prevPhaseDoneRef.current[phase.id] = nowDone;
    });
  }, [checked, allDone, startShow]);

  // RECOMMENDATION 1: clipboard
  const copyToClipboard = useCallback(() => {
    navigator.clipboard.writeText(buildPlainText(checked))
      .then(() => { setCopyMsg("COPIED"); setTimeout(() => setCopyMsg(""), 1800); })
      .catch(() => { setCopyMsg("FAILED"); setTimeout(() => setCopyMsg(""), 1800); });
  }, [checked]);

  // RECOMMENDATION 4: keyboard nav
  const handleTaskKey = useCallback((e, id) => {
    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggle(id); }
  }, [toggle]);

  const handlePhaseKey = useCallback((e, phase) => {
    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); togglePhase(phase); }
  }, [togglePhase]);

  return (
    <div style={{
      minHeight: "100vh",
      background: "#050810",
      fontFamily: "'Courier New', Courier, monospace",
      color: "#e2e8f0",
      padding: "2rem",
      position: "relative",
      overflowX: "hidden",
    }}>
      {/* Canvas always mounted for phase bursts */}
      <canvas ref={canvasRef} style={{
        position: "fixed", inset: 0,
        width: "100%", height: "100%",
        pointerEvents: "none", zIndex: 100,
      }} />

      {/* Header */}
      <div style={{ textAlign: "center", marginBottom: "2.5rem" }}>
        <div style={{ fontSize: "0.65rem", letterSpacing: "0.35em", color: "#00d4ff", marginBottom: "0.5rem" }}>
          AI FEED DOCUMENT v2.0
        </div>
        <h1 style={{
          fontSize: "clamp(1.4rem, 4vw, 2.2rem)", fontWeight: 900,
          letterSpacing: "0.05em", margin: 0, lineHeight: 1.1,
          color: "#fff", textShadow: "0 0 40px rgba(0,212,255,0.4)",
        }}>
          PROJECT AUDIT LOOP
        </h1>
        <div style={{ fontSize: "0.7rem", color: "#64748b", marginTop: "0.5rem", letterSpacing: "0.2em" }}>
          REPEAT PER PROJECT -- PRIORITIZED ORDER
        </div>

        {/* Toolbar */}
        <div style={{ marginTop: "1.2rem", display: "flex", justifyContent: "center", gap: "0.75rem" }}>
          {[
            { label: copyMsg || "COPY FOR AI", action: copyToClipboard, activeColor: "#34d399" },
            { label: "RESET", action: resetAll, activeColor: "#f87171" },
          ].map((btn) => (
            <button
              key={btn.label}
              onClick={btn.action}
              style={{
                background: "transparent",
                border: "1px solid #1e293b",
                color: copyMsg && btn.label === copyMsg ? btn.activeColor : "#475569",
                fontFamily: "inherit",
                fontSize: "0.63rem",
                letterSpacing: "0.2em",
                padding: "0.4rem 0.9rem",
                cursor: "pointer",
                borderRadius: 3,
              }}
            >
              {btn.label}
            </button>
          ))}
        </div>
      </div>

      {/* Global progress */}
      <div style={{
        maxWidth: 780, margin: "0 auto 2.5rem",
        background: "#0f172a", border: "1px solid #1e293b",
        borderRadius: 4, padding: "1rem 1.25rem",
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "0.5rem", fontSize: "0.72rem", color: "#94a3b8" }}>
          <span>OVERALL PROGRESS</span>
          <span style={{ color: allDone ? "#34d399" : "#00d4ff" }}>
            {completedCount} / {total} -- {pct}%
          </span>
        </div>
        <div style={{ background: "#1e293b", borderRadius: 2, height: 6, overflow: "hidden" }}>
          <div style={{
            height: "100%", width: `${pct}%`,
            background: allDone
              ? "linear-gradient(90deg,#34d399,#00d4ff)"
              : "linear-gradient(90deg,#a78bfa,#00d4ff)",
            transition: "width 0.35s ease",
            boxShadow: "0 0 10px rgba(0,212,255,0.5)",
          }} />
        </div>
        {allDone && (
          <div style={{
            textAlign: "center", marginTop: "0.75rem", color: "#34d399",
            fontSize: "0.78rem", letterSpacing: "0.3em", fontWeight: 700,
          }}>
            LOOP COMPLETE -- FIRE THE CANNONS
          </div>
        )}
      </div>

      {/* Phase cards */}
      <div style={{ maxWidth: 780, margin: "0 auto", display: "flex", flexDirection: "column", gap: "1.5rem" }}>
        {PHASES.map((phase) => {
          const phaseChecked = phase.tasks.filter((t) => checked[t.id]).length;
          const phaseDone = phaseChecked === phase.tasks.length;
          // RECOMMENDATION 5: per-phase progress percentage
          const phasePct = Math.round((phaseChecked / phase.tasks.length) * 100);

          return (
            <div key={phase.id} style={{
              border: `1px solid ${phaseDone ? phase.color + "55" : "#1e293b"}`,
              borderLeft: `3px solid ${phase.color}`,
              background: "#080d1a", borderRadius: 4, overflow: "hidden",
              transition: "border-color 0.3s",
            }}>
              {/* Phase header - RECOMMENDATION 4: keyboard accessible */}
              <div
                role="button"
                tabIndex={0}
                onClick={() => togglePhase(phase)}
                onKeyDown={(e) => handlePhaseKey(e, phase)}
                style={{
                  display: "flex", justifyContent: "space-between", alignItems: "center",
                  padding: "0.75rem 1rem", cursor: "pointer",
                  background: phaseDone ? `${phase.color}0d` : "transparent",
                  transition: "background 0.3s", outline: "none",
                }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
                  <span style={{
                    fontSize: "0.62rem", fontWeight: 700, letterSpacing: "0.2em",
                    color: phase.color, background: `${phase.color}18`,
                    padding: "2px 8px", borderRadius: 2, border: `1px solid ${phase.color}44`,
                  }}>
                    {phase.id}
                  </span>
                  <span style={{
                    fontSize: "0.78rem", fontWeight: 700, letterSpacing: "0.12em",
                    color: phaseDone ? phase.color : "#e2e8f0", transition: "color 0.3s",
                  }}>
                    {phase.label}
                  </span>
                </div>
                <span style={{
                  fontSize: "0.67rem", color: phaseDone ? phase.color : "#475569",
                  letterSpacing: "0.08em", minWidth: 80, textAlign: "right",
                }}>
                  {phaseChecked}/{phase.tasks.length}{phaseDone ? " DONE" : ` (${phasePct}%)`}
                </span>
              </div>

              {/* RECOMMENDATION 5: per-phase mini bar */}
              <div style={{ height: 2, background: "#0a0f1e" }}>
                <div style={{
                  height: "100%", width: `${phasePct}%`,
                  background: phase.color, opacity: 0.6,
                  transition: "width 0.35s ease",
                }} />
              </div>

              {/* Tasks */}
              <div style={{ padding: "0 1rem 0.75rem" }}>
                {phase.tasks.map((task, ti) => (
                  <div
                    key={task.id}
                    role="checkbox"
                    aria-checked={!!checked[task.id]}
                    tabIndex={0}
                    onClick={() => toggle(task.id)}
                    onKeyDown={(e) => handleTaskKey(e, task.id)}
                    style={{
                      display: "flex", gap: "0.75rem", alignItems: "flex-start",
                      padding: "0.55rem 0",
                      borderTop: ti === 0 ? "1px solid #0f172a" : "none",
                      cursor: "pointer",
                      opacity: checked[task.id] ? 0.4 : 1,
                      transition: "opacity 0.2s", outline: "none",
                    }}
                  >
                    <div style={{
                      width: 14, height: 14, minWidth: 14,
                      border: `1.5px solid ${checked[task.id] ? phase.color : "#334155"}`,
                      borderRadius: 2,
                      background: checked[task.id] ? phase.color : "transparent",
                      display: "flex", alignItems: "center", justifyContent: "center",
                      marginTop: 3, transition: "all 0.15s",
                    }}>
                      {checked[task.id] && (
                        <svg width="9" height="7" viewBox="0 0 9 7" fill="none">
                          <path d="M1 3.5L3.5 6L8 1" stroke="#000" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                      )}
                    </div>
                    <div>
                      <span style={{
                        fontSize: "0.6rem", color: phase.color, letterSpacing: "0.15em",
                        fontWeight: 700, marginRight: "0.5rem", opacity: 0.65,
                      }}>
                        {task.id}
                      </span>
                      <span style={{
                        fontSize: "0.78rem", lineHeight: 1.55,
                        color: checked[task.id] ? "#475569" : "#cbd5e1",
                        textDecoration: checked[task.id] ? "line-through" : "none",
                        transition: "color 0.2s",
                      }}>
                        {task.text}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>

      <div style={{
        textAlign: "center", marginTop: "2.5rem",
        fontSize: "0.58rem", color: "#1e293b", letterSpacing: "0.3em",
      }}>
        MR DEV ENVIRONMENT -- AUDIT LOOP v2.0 -- 2026
      </div>
    </div>
  );
}

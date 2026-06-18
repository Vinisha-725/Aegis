export default function Home() {
  return (
    <main className="flex-1">
      {/* ── Hero ──────────────────────────────────────────────────────────── */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        {/* Background grid + glow */}
        <div
          className="absolute inset-0 opacity-20"
          style={{
            backgroundImage:
              "linear-gradient(rgba(124, 58, 237, 0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(124, 58, 237, 0.1) 1px, transparent 1px)",
            backgroundSize: "60px 60px",
          }}
        />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] rounded-full bg-purple-700/10 blur-3xl pointer-events-none" />
        <div className="absolute top-1/4 right-1/4 w-[400px] h-[400px] rounded-full bg-cyan-500/10 blur-3xl pointer-events-none" />

        <div className="relative z-10 max-w-6xl mx-auto px-6 text-center">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-card mb-8 text-sm text-purple-300">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            AI-Powered Trust Protocol · Phase 0
          </div>

          {/* Heading */}
          <h1 className="text-6xl md:text-8xl font-bold tracking-tight mb-6 leading-none">
            <span className="gradient-text">Aegis</span>
          </h1>
          <p className="text-2xl md:text-3xl text-slate-300 font-light mb-4">
            Verify milestones. Release payments.{" "}
            <span className="text-purple-400 font-medium">Automatically.</span>
          </p>
          <p className="text-lg text-slate-400 max-w-2xl mx-auto mb-12">
            Aegis connects GitHub repositories to a multi-agent AI verification pipeline
            that validates work quality and releases escrowed funds — no manual review needed.
          </p>

          {/* CTA */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <button
              id="cta-get-started"
              className="px-8 py-4 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold transition-all duration-200 hover:shadow-lg hover:shadow-purple-500/25 hover:-translate-y-0.5"
            >
              Get Started
            </button>
            <button
              id="cta-view-docs"
              className="px-8 py-4 rounded-xl glass-card text-slate-300 hover:text-white font-semibold transition-all duration-200 hover:border-purple-500/50 hover:-translate-y-0.5"
            >
              View Architecture →
            </button>
          </div>
        </div>

        {/* Pipeline visualization */}
        <div className="absolute bottom-12 left-0 right-0 flex items-center justify-center gap-2 px-6">
          {[
            { label: "GitHub Repo", color: "border-slate-600 text-slate-400" },
            { label: "AI Verification", color: "border-purple-500/60 text-purple-300" },
            { label: "Consensus", color: "border-cyan-500/60 text-cyan-300" },
            { label: "Escrow Release", color: "border-emerald-500/60 text-emerald-300" },
            { label: "Reputation", color: "border-amber-500/60 text-amber-300" },
          ].map((step, i) => (
            <div key={step.label} className="flex items-center gap-2">
              <div
                className={`px-3 py-1.5 rounded-lg border glass-card text-xs font-medium ${step.color}`}
              >
                {step.label}
              </div>
              {i < 4 && (
                <span className="text-slate-600 pipeline-arrow text-lg">→</span>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* ── Agents Grid ──────────────────────────────────────────────────────── */}
      <section id="agents" className="py-24 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">
              Five AI Agents. One Verdict.
            </h2>
            <p className="text-slate-400 text-lg max-w-2xl mx-auto">
              Each agent independently evaluates a different dimension of milestone
              completion before Kratos delivers the final consensus.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {agents.map((agent) => (
              <div
                key={agent.name}
                id={`agent-card-${agent.name.toLowerCase()}`}
                className="agent-card glass-card rounded-2xl p-6 border border-slate-800"
              >
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <span className={`text-xs font-mono font-semibold ${agent.color} mb-1 block`}>
                      {agent.phase}
                    </span>
                    <h3 className="text-xl font-bold text-white">{agent.name}</h3>
                    <p className="text-slate-400 text-sm">{agent.role}</p>
                  </div>
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center text-xl ${agent.bgColor}`}>
                    {agent.icon}
                  </div>
                </div>
                <p className="text-slate-300 text-sm leading-relaxed mb-4">
                  {agent.description}
                </p>
                <div className={`px-3 py-1.5 rounded-lg border ${agent.thresholdColor} text-xs font-mono inline-block`}>
                  threshold: {agent.threshold}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── How It Works ─────────────────────────────────────────────────────── */}
      <section id="how-it-works" className="py-24 px-6 bg-slate-900/50">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">How It Works</h2>
            <p className="text-slate-400 text-lg">
              From code commit to payment release in minutes, not weeks.
            </p>
          </div>

          <div className="space-y-6">
            {steps.map((step, i) => (
              <div
                key={i}
                className="flex gap-6 items-start glass-card rounded-2xl p-6 border border-slate-800"
              >
                <div className="flex-shrink-0 w-10 h-10 rounded-full bg-purple-600/20 border border-purple-500/30 flex items-center justify-center text-purple-300 font-bold text-lg">
                  {i + 1}
                </div>
                <div>
                  <h3 className="text-white font-semibold text-lg mb-1">{step.title}</h3>
                  <p className="text-slate-400">{step.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Status Banner ─────────────────────────────────────────────────────── */}
      <section className="py-16 px-6">
        <div className="max-w-4xl mx-auto">
          <div className="glass-card rounded-2xl p-8 border border-purple-500/20 glow-purple text-center">
            <h3 className="text-2xl font-bold text-white mb-3">
              🚧 Currently Building
            </h3>
            <p className="text-slate-300 mb-6">
              Aegis is under active development. Phase 0 (Foundation) is complete.
              Follow along as we build the full verification pipeline.
            </p>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {phaseStatus.map((p) => (
                <div key={p.phase} className="text-center">
                  <div className={`text-2xl mb-1 ${p.done ? "text-emerald-400" : "text-slate-600"}`}>
                    {p.done ? "✓" : "○"}
                  </div>
                  <div className="text-xs text-slate-400 font-mono">Phase {p.phase}</div>
                  <div className="text-xs text-slate-300">{p.name}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ── Footer ────────────────────────────────────────────────────────────── */}
      <footer className="border-t border-slate-800 py-8 px-6 text-center text-slate-500 text-sm">
        <p>Aegis — AI-Powered Trust Protocol · Built with Next.js + FastAPI + Solana</p>
      </footer>
    </main>
  );
}

// ── Data ─────────────────────────────────────────────────────────────────────

const agents = [
  {
    name: "Argus",
    role: "Evidence Collector",
    phase: "Phase 5",
    icon: "👁",
    color: "text-purple-400",
    bgColor: "bg-purple-500/10",
    thresholdColor: "border-purple-500/30 text-purple-300",
    threshold: "confidence > 0.70",
    description:
      "Gathers repository evidence — commits, changed files, pull requests, and branches — to verify that real work was done.",
  },
  {
    name: "Themis",
    role: "Scope Validator",
    phase: "Phase 6",
    icon: "⚖️",
    color: "text-cyan-400",
    bgColor: "bg-cyan-500/10",
    thresholdColor: "border-cyan-500/30 text-cyan-300",
    threshold: "scope_match > 0.75",
    description:
      "Uses Claude Haiku to compare milestone requirements against actual repository changes and produce a scope alignment score.",
  },
  {
    name: "Dike",
    role: "Quality Analyzer",
    phase: "Phase 7",
    icon: "🔍",
    color: "text-emerald-400",
    bgColor: "bg-emerald-500/10",
    thresholdColor: "border-emerald-500/30 text-emerald-300",
    threshold: "quality_score > 0.65",
    description:
      "Analyzes code quality, documentation completeness, and implementation risks using LLM-powered code review.",
  },
  {
    name: "Chronos",
    role: "Deadline Verifier",
    phase: "Phase 8",
    icon: "⏱",
    color: "text-amber-400",
    bgColor: "bg-amber-500/10",
    thresholdColor: "border-amber-500/30 text-amber-300",
    threshold: "on_time: bool",
    description:
      "Validates that the milestone was submitted before the deadline and that the last commit precedes the cutoff time.",
  },
  {
    name: "Kratos",
    role: "Consensus Engine",
    phase: "Phase 9",
    icon: "⚡",
    color: "text-rose-400",
    bgColor: "bg-rose-500/10",
    thresholdColor: "border-rose-500/30 text-rose-300",
    threshold: "approved: bool",
    description:
      "Aggregates Argus, Themis, Dike, and Chronos outputs and issues the final approval verdict that triggers escrow release.",
  },
];

const steps = [
  {
    title: "Connect Repository",
    description:
      "Link your GitHub repository to an Aegis project and define milestone requirements with acceptance criteria.",
  },
  {
    title: "Submit Milestone",
    description:
      "When work is done, submit the milestone for verification. Aegis automatically scans the repository.",
  },
  {
    title: "AI Agents Verify",
    description:
      "Argus, Themis, Dike, and Chronos independently analyze evidence, scope, quality, and deadlines.",
  },
  {
    title: "Kratos Decides",
    description:
      "The consensus engine evaluates all agent results against configurable thresholds to produce a final verdict.",
  },
  {
    title: "Escrow Released",
    description:
      "On approval, the Solana smart contract releases escrowed USDC to the developer's wallet automatically.",
  },
  {
    title: "Reputation Updated",
    description:
      "Both client and developer reputation scores are updated, building a verifiable track record on-chain.",
  },
];

const phaseStatus = [
  { phase: 0, name: "Foundation", done: true },
  { phase: 1, name: "Database", done: false },
  { phase: 2, name: "Auth", done: false },
  { phase: 3, name: "Projects", done: false },
  { phase: 4, name: "GitHub", done: false },
  { phase: 5, name: "Argus", done: false },
  { phase: 6, name: "Themis", done: false },
  { phase: 7, name: "Dike", done: false },
  { phase: 8, name: "Chronos", done: false },
  { phase: 9, name: "Kratos", done: false },
  { phase: 10, name: "Dashboard", done: false },
  { phase: 11, name: "Escrow", done: false },
  { phase: 12, name: "Reputation", done: false },
  { phase: 13, name: "Deploy", done: false },
];

# KEEL evals

Three cases for `claude plugin eval`. They test KEEL's two front doors: owner mode,
where the project is yours, and operator mode, where the package is someone else's.
Each case runs three times with KEEL loaded and three times without it. The difference,
Δ, says whether KEEL beats plain Claude Code on the same prompt.

## Run it

From the master folder, which is the plugin root:

```bash
claude plugin eval . --trust-plugin --no-publish --scaffold --json results.json --allow-tools Write Edit Bash
```

- `--scaffold` builds the workspace of `operator-job`. Without it that case starts empty.
- `--allow-tools Write Edit Bash` is needed because a case's `allowed_tools` grants only
  read-only tools. Without it no case can write a file or run a command. Bash runs in
  Claude Code's sandbox and can only write inside the run's workspace. Keep this flag
  last, because it takes a list.
- `--json results.json` writes the result document into the master folder. Move it or
  delete it before a release, since `make_release.py` refuses untracked files.
- The default `--threshold` is 1.0, so the command exits 1 when any case scores below
  perfect. Read the scores; don't read the exit code as a verdict.

Add `--ablation none` for a strict KEEL-conformance score. That runs the with-KEEL arm
only, and every grader counts. To iterate on one case, use
`--case operator-job --runs 1 --ablation none`.

You need Claude Code 2.1.269 or later, git 2.31 or later, and your usual model
credentials. A full run makes 18 agent runs, plus three short judge calls for each `llm`
grader in each run. All of it counts against your plan or API bill.

## The cases

| Case | Prompt | What it checks | Why |
|---|---|---|---|
| `vague-idea` | "Use KEEL. I want a small web app where my book club votes on the next book." | HELM runs, `.keel/keel.json` says owner, a tier is stated, one numbered question round with options and a recommended pick on each question, no application code | The most common start is an idea, not a spec. KEEL promises to ask before it builds. |
| `complete-description` | A full paragraph naming the users, the stack (Next.js, Prisma, PostgreSQL, Tailwind) and the features | At least 3 of 5 production questions (deploy target, sign-in, secrets, data retention, observability) asked before any code, STANDARD stated, `docs/BRIEF.md` written, no application source | A complete-sounding request still leaves production open. KEEL must ask anyway, without re-asking what was said. |
| `operator-job` | "Use KEEL: this is someone else's package; do the job its README describes." | Role operator recorded, the bug fixed, `python3 -m unittest` run and passing, tests unchanged, nothing committed, a debrief at `.keel/ops/debrief.md` labeled Evidence / Inferred / Missing, no `docs/` | In someone else's package the package's rules win. KEEL keeps its notes in `.keel/` and leaves nothing else behind. |

The operator package is built by `operator-job/scaffold.sh`: a README with the job and two
rules, a `calc.py` whose `add` subtracts, and a test file. It is a git repository with
one commit, so "nothing committed" can be checked.

## How the graders count

Each case has deterministic graders first and one `llm` judge last. They come in two
kinds:

- **Behavior** that a plain agent could also show: asking before building, offering
  options, fixing and running the tests, keeping the package's rules. These count in
  both arms, so Δ measures behavior.
- **KEEL names** a plain agent can't know: `.keel/keel.json`, the tier word,
  `docs/BRIEF.md`, `.keel/ops/debrief.md`. These carry `arm: with-only`. The
  skill-fired check (`tool_used: Skill`) is treated the same way automatically. In a
  two-arm run the report shows them as pass/fail indicators that don't count. Under
  `--ablation none` they count.

`complete-description/graders/production-questions.md` needs 3 of the 5 topics. A regex
can't count distinct topics, so its pattern lists the ten ways to choose three of five.
The topic word lists are in the file's comments.

## Status

No results yet. Every claim that a case passes is Missing evidence until the suite has
run on Claude Code 2.1.269 or later. Each run writes `evals/results/<timestamp>/` with
`aggregate-result.json` and `report.html`. That folder is gitignored by
`evals/.gitignore`.

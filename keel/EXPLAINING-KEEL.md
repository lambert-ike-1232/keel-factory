# Explaining KEEL

How to teach, pitch, and defend this framework to someone encountering it for the
first time.

This is a general communication document. The audience might be an interviewer, a new
teammate, a client asking why your process looks like this, or yourself in six months.
The material is the same in every case, because a framework you cannot explain in
sixty seconds is a framework you do not actually understand.

---

## 1. The ladder of explanations

Have four versions ready. Use the shortest one that fits the moment, and let them ask
for more.

### Ten seconds

> Fixed artifacts, composable process, and nothing is "done" until a command proves it.

### Sixty seconds

> KEEL is an engineering framework for going from an idea to a production-ready
> product with an agent doing most of the typing.
>
> It rests on one observation: decisions are cheap while they are sentences and
> expensive once they are code. So it front-loads everything that can be written
> down — the brief, the contract, the schemas, the acceptance checks, the type
> signatures — and only then writes code, in thin slices that each run end to end.
>
> Two things make it different from a normal spec-driven process. First, an evidence
> discipline: every claim is labelled observed, inferred, or unconfirmed, and
> "specified" never counts as "implemented." Second, a traceability matrix: every
> feature line owns an acceptance check or is a declared descope. There are no blanks,
> because blanks are how half-built features read as finished.
>
> It runs at three weights, from a few hours to a few weeks, and the phases are the
> same at every weight. Only the ceremony scales.

### Five minutes — the whiteboard

Draw this:

```
     BRIEF  →  CONTRACT  →  DESIGN  →  SLICE  →  PROVE
       │          │           │          │         │
    what &    what must    the shapes,  thin,     did it
     why      be true      and what     end-to-   actually
                           I'm least    end        work
                           sure about
```

Then say four things about it:

1. **The phases are ordered by cost of change.** Everything to the left is cheaper to
   change than everything to its right. That ordering is the entire design.
2. **CONTRACT is where "production" gets defined**, and it happens before any code. The
   acceptance gate is written before the feature list is even finished, so a feature
   is not shippable until its check exists.
3. **DESIGN is the step everyone skips.** Type signatures with no bodies. A human reads
   them in seconds and says right or wrong, and they pin down most of the
   implementation. You get the value of code review before the code exists. It ends
   with a numbered list of the decisions the agent is least confident about — which
   turns a silent guess into a conversation.
4. **PROVE reviews on three independent axes in parallel**, never merged: Standards
   (built well?), Spec (built the right thing?), Gate (does it actually run?). Merging
   them lets one mask the other. Code can follow every convention and implement the
   wrong feature.

### Twenty minutes — the full walk

Go phase by phase using [framework/PHASES.md](framework/PHASES.md), then the five
standing rules, then the stack. Only do this if they ask for it.

---

## 2. Lead with the failure

The strongest opening is not the framework. It is the miss that produced it.

> A previous build of mine scored 88%. Professional standards came in at 90% and
> template completeness at 96%, but specification coverage was 78%. I went and looked
> at why, and four of the five gaps had exactly the same shape: a spec line that no
> acceptance check was ever bound to. Translation memory was an in-job cache instead of
> a persistent store. Semantic injection detection was specified and only the regex
> pass shipped. Right-to-left text was flagged but never actually rendered.
>
> None of those were engineering failures. The engineering scored 90 and 96. It was a
> bookkeeping failure — I had no mechanism that forced every feature line to own a
> check, so a feature could be sixty percent built and read as done.
>
> KEEL is what I built in response. The traceability rule exists specifically because
> of that, and it says a feature line with no bound check is a FAIL row, never a blank.

Then, if the room is engaged, the second failure — the one that's better, because it's the
framework failing rather than the project:

> The first time I put that framework to work, it caught four things before I wrote a line
> of frontend. Then I actually ran the gates, and **four more defects came out that had
> survived a completely green build.** Three of them were in the gates themselves. One was
> a lint command that had been crashing before it linted anything, on every build, for the
> life of the project.
>
> So the framework had the same blind spot it was built to fix, one level up: it checked
> the code and nothing checked the checkers. That's a sixth rule now.

Why this works: it demonstrates that you read your own feedback precisely rather than
generally, that you diagnosed a root cause instead of resolving to try harder, and
that you built a mechanism instead of forming an intention. Those are the three things
a senior engineer is actually being assessed on. Leading with a real miss also earns
you the right to make strong claims afterwards.

---

## 3. The provenance table

Do not pretend this is original. Say exactly where each piece came from — it reads as
literacy and judgement, not as borrowing, and it invites a much better conversation.

| Idea | From | Why it earned its place |
|---|---|---|
| Signatures with no bodies; least-confident list; tracer-bullet slices | The Software Factory (Dex Horthy, HumanLayer) | The highest information-per-token artifact in software, and the mechanism that surfaces silent guesses |
| The Slack test; `[GUESS: ...]`; demand proof | The Thorsten Prompt (Thorsten Ball, Amp) | The only layer with negative overhead over time — it is designed to go quiet as you improve |
| Grilling with a frontier; vertical slices at confirmed seams; two-axis review; deep modules; the phase-boundary tree | The skills repo (Matt Pocock) | The only source that takes context death seriously, and the best interview primitive available |
| The fixed document set; "specified is never implemented"; Required vs Planned Checks; human review gates; the Production Build Contract | My own project template | The only layer that knows what production means, and the only one with an epistemics |
| Traceability matrix; cost discipline | New in KEEL, v1 | The two things none of the four have, and the first is the one that cost me points |
| The Instrument Rule — toolchain, negative controls, expiring evidence, bound numbers | New in KEEL, v1.1 | Added after four defects survived a green build. Three were in the apparatus, not the code |

The framing to use out loud: **these four do not compete, they run on different
clocks.** One governs a message, one a session, one a feature, one a project. Two
frameworks only conflict when they try to govern the same time scale. Sorted by clock
speed, they nest.

That sentence is the most interesting thing in this whole document. If you only land
one idea, land that one.

---

## 4. The hard questions

Prepare these. They are the ones a sharp person actually asks.

**"Isn't this over-engineering? It's a lot of documents for one feature."**

> It scales. There are three tiers and the smallest one is seven guarantees and about
> twenty-five minutes — a README that runs cold, a resolved assumption list, a contract on
> every boundary, one check that runs and that I've watched fail once, its toolchain
> confirmed present, no secrets on disk, and an honest status report. The full document set is for a product with users and a lifespan.
> Choosing the tier is an explicit step, and picking the light one is a decision I say
> out loud rather than a place I drift into.

**"How is this different from Spec-Kit, BMAD, or GSD?"**

> Those own the process end to end, which means when the process has a bug you cannot
> reach in and fix it. KEEL fixes the *artifacts* and leaves the *process* composable —
> the shape of `docs/` never varies, but which skills I run to fill it does. And none
> of them treat evidence as a first-class concern. The failure mode I have actually
> hit is not a missing process step; it is a scaffold that looks finished and runs
> nothing, and that needs an epistemics, not a workflow.

**"Doesn't all this front-loading slow you down?"**

> It front-loads *contracts*, never implementations. Contracts are cheap to write and
> expensive to change; implementations are exactly the reverse. So schemas, acceptance
> checks and signatures go first, and how the thing is actually built gets discovered
> one running slice at a time. The slowdown people picture comes from front-loading
> implementation detail, which this explicitly forbids — the first slice is mocked,
> stubbed, end to end, and running.

**"What happens when the models get better? Does this become obsolete?"**

> Most of it gets *cheaper*, not obsolete. The three constraints underneath it are
> cost of change, finite context, and feedback rate. Better models widen the context
> window and raise quality; they do not make it cheap to change a decision that has
> become ten thousand lines of code, and they do not tell you whether you built the
> right thing. The layer that would shrink first is the prompt-coaching layer, and
> that one is already designed to go quiet.

**"How do you know it works?"**

> It's been field-tested once, and the interesting part is that it **failed** in a way I
> could measure.
>
> Building a web UI for an existing engine, the framework caught four things before any
> frontend code existed — the biggest being that the engine could never have deployed to
> the platform it was configured for, because it depends on a system binary that platform
> can't install.
>
> Then I ran the gates, and **four more defects turned up that had survived a completely
> green build**: a passing typecheck, a passing lint, a passing test suite, a successful
> production build. Three of those four were defects in the checking apparatus rather than
> in the code. One of them was a lint command that had been crashing before it linted
> anything, on every build, for the life of the project — and a silent crash is
> indistinguishable from a clean pass.
>
> So the framework's own weak point turned out to be that it verified the code and nothing
> verified the instruments. That's Rule 6 now, and it exists because the framework was
> observed failing, not because I reasoned my way to it.

**"Isn't the agent just doing what you told it? Where's the engineering?"**

> The engineering is in the contracts, the seams, and the gate. Deciding where a seam
> goes, what an interface should hide, which acceptance check actually proves a
> property, and which model rung a call belongs on — those are the decisions, and they
> are the same decisions they always were. What changed is that typing stopped being
> the bottleneck, which makes taste and specification the whole job.

**"Four defects got past your gates. Doesn't that undermine the whole thing?"**

> The opposite. Gates that never catch anything are the ones I'd worry about — that
> usually means they aren't running. What matters is where the defects were: three of the
> four were in the apparatus, not the product. A lint gate that had never executed. A
> stated cost ceiling nobody had counted. A build that broke on its own from a dependency
> range moving underneath it.
>
> None of those are visible to reading, and none would have been caught by more careful
> code review, because the code was fine. They needed the thing to actually run. That's
> the finding, and it's now a rule: **an unrun check isn't weak evidence, it's no
> evidence.**

**"Why does cost have its own rule?"**

> Because a product that works and costs too much to run is a product that does not
> work, and cost is like testability: nearly free if you design it in, expensive to
> retrofit, and invisible in a demo right up until it is the only thing anyone cares
> about. So the ceiling is a contract line, the rule is that the cheapest configuration
> passing the gate wins, and expense has to earn itself against a named failing check.
> That also means I can tell you what one unit costs, what it costs at volume, and
> what the alternative costs — measured against fixtures, not estimated.

---

## 5. Showing it in three minutes

If you can show rather than tell, show these four things in this order:

1. **`TRACEABILITY.md`** — every feature line, its check, its test, its status. This
   single file answers "is it done?" in ten seconds and it is the thing most projects
   cannot produce at all.
2. **`ACCEPTANCE.md`** — then *run it*, live. Required vs Planned Checks is the
   interesting detail: aspiration is allowed to exist without contaminating the gate,
   and promoting a line requires the command to work.
3. **`DESIGN.md`, the least-confident list** — "here are the five things the agent told
   me it was about to guess, and here is what I decided." This is the most persuasive
   artifact in the set because it is visibly not something you can fake after the fact.
4. **`COST_MODEL.md`** — three measured numbers: unit cost, cost at volume, cost of the
   alternative.
5. **Break something on purpose.** Feed a credential scanner a string you know is in the
   bundle and watch it exit 1. It takes fifteen seconds and it is the only demonstration
   on this list that proves a check is real rather than merely green.

Then the status report, in its three categories, out loud. Being willing to say
"implemented, unverified" about your own work in a room where you are being assessed is
worth more than any of the artifacts.

---

## 6. Teaching it to a teammate

Different job from pitching. In order:

1. **The clock insight first** ([THE-STACK.md](framework/THE-STACK.md) §1). Nothing
   else makes sense until they see why four frameworks nest instead of compete.
2. **The five phases**, on a whiteboard, ordered by cost of change.
3. **Rules 2 and 3 only** — evidence and traceability. Those two carry most of the
   value and both are one sentence each.
4. **Have them run a SPRINT-tier task end to end.** The floor is seven items; they will
   feel the shape of it in an afternoon.
5. **Then the rest of the rules, tiers, and the cost ladder.**

Do not start with the document set. It looks like bureaucracy until you know which
failure each document prevents, and then it looks obvious. That ordering matters more
than anything else in this section.

---

## 7. What to say when it fails

It will. Say this:

> The framework did not catch it. Here is which rule should have, and here is the
> change to that rule.

A framework that never changes is being followed rather than used. Every rule in KEEL
has a named failure behind it, and the honest way to grow it is to add rules the same
way the existing ones were added: by getting something wrong, diagnosing the root
cause precisely, and building a mechanism rather than forming an intention.

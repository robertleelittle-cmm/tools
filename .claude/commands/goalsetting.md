<!-- Goal-setting skill: guides any McKesson Platform employee through the Workday
     performance and development goal-setting process. Produces SMART goals aligned to
     the three Platform evaluation criteria, in the required GOAL / DESCRIPTION / MILESTONES
     format. Usage: /goalsetting -->

Walk the user through McKesson's annual goal-setting process. Follow the phases below in
order. Do not skip ahead or combine phases.

---

## McKesson Goal Framework

Every employee sets goals across two categories for the fiscal year. Goals are entered into
Workday and revisited each quarter.

**What You Deliver — 3 to 4 Performance Goals**
Focus on outcomes: what results will be produced, not how work gets done or which tasks
will be completed. Goals should create shared clarity between the employee and their leader
about what success looks like.

**How You Grow — 1 to 2 Development Goals**
Focus on building skills and capabilities — not fixing performance, but growing readiness
for current and future work. Development goals should feel relevant and achievable, not
overwhelming.

**How You Deliver — not a separate goal**
LEADRx leadership behaviors and I2CARE values apply to every goal, not just certain ones.
There is no trade-off between results and behaviors. Do not create a goal for "How You
Deliver" — it is the standard for how all other goals are pursued.

**Total: 4 to 6 goals** (3–4 performance + 1–2 development) entered into Workday.

---

## Phase 1: Start the Interview

Open with this exact question:

> Will you provide prewritten goals to review, or should I ask about your job to begin?

Then follow the appropriate path.

---

### Path A: Ask about the job

Ask these questions in order. Ask them one or two at a time — do not present the full list
at once.

1. What is your job title and level?
2. What are your responsibilities?
3. What are your team's priorities (or other cascaded goals) for this goal period?
4. What feedback have you received about your job that would be relevant to your goals?
5. Do you have prior goals or topics for potential goals you'd like to include?

**Input quality:** If any response lacks the specificity needed to write meaningful goals,
ask one follow-up round before proceeding. Guidance for what specificity looks like:

- *Responsibilities*: scope, complexity, and business impact — not just job function.
  "I maintain the user authentication service handling 50k daily logins and lead API
  design for a team of five" is useful. "I develop software" is not.
- *Team priorities*: specific initiatives, timelines, and success metrics. "Reduce API
  response times by 40% to support 10x user growth expected in Q2–Q3" is useful.
  "Improve system performance" is not.
- *Feedback*: performance-related observations about delivery, collaboration, or technical
  growth, with specific examples.

Once you have sufficient context, proceed to Phase 2.

---

### Path B: Prewritten goals provided

Review each provided goal against the SMART criteria (see below). Note where each criterion
is satisfied and where it is unclear or missing. Proceed to Phase 2.

---

## Phase 2: Goal Construction

Draft a set of goals matching the McKesson framework:
- 3 to 4 performance goals (What You Deliver)
- 1 to 2 development goals (How You Grow)

**Performance goals** should focus on outcomes with observable results — not on tasks,
behaviors, or how work gets done. Each should connect clearly to the employee's
responsibilities and their team's priorities.

**Development goals** should focus on capability-building that serves the employee's
current role and team. They should feel achievable and be grounded in the employee's
actual growth areas, not generic aspirations.

All goals must follow this statement format:
> [Specific action] + [Measurable criteria] + [Achievable scope] + [Relevant context] + [Time-bound deadline]

Examples:
- "Reduce API response time for the checkout service from 1.2 seconds to under 400ms by
  optimizing database queries and implementing Redis caching, measured via application
  monitoring, completed by March 31st"
- "Increase automated test coverage for the authentication module from 60% to 85% by
  writing unit and integration tests using pytest, tracked via coverage reports, delivered
  by February 15th"
- "Decrease production incidents by 50% (from 20 to 10 monthly) by implementing
  comprehensive monitoring alerts and runbook automation, measured via incident tracking
  system, achieved by Q2 end"

**CRITICAL:** Goals should be achievable and realistic regardless of the performance level
being targeted. Exceptional performance comes from how well goals are executed, not from
setting unrealistic targets. Do not inflate goals in response to a desire for higher
ratings.

---

## Phase 3: Goal Review (one goal at a time)

For each drafted goal, present:

1. The goal statement (~30 words)
2. A bullet for each SMART criterion: how the goal satisfies it (or where it falls short)
3. A rating out of 10 for how well the goal meets SMART criteria overall

Then ask: is this goal acceptable, should it be revised, or should it be dropped?

Before accepting any goal as final, verify:
- Clear connection to the employee's actual responsibilities and team priorities
- Realistic metrics based on current baseline performance
- Sufficient specificity to enable quarterly milestone tracking

Do this for each goal individually. Do not batch goals for review. Only proceed to Phase 4
once all goals are confirmed.

---

## Phase 4: Goal Artifact

Produce a single markdown document — no preamble, no conclusion — containing all confirmed
goals. Each goal uses this template:

```
GOAL
    [No more than 15 words. Quantifiable outcome if possible.]

DESCRIPTION
    [Restate the goal in detail with implementation points as a short bulleted list.]

MILESTONES
    [Quarterly milestones in chronological order, each as a measurable checkpoint.]
```

Example:

---

GOAL
    Decrease production incidents by 50% (from 20 to 10 monthly) by implementing
    comprehensive monitoring alerts and runbook automation, measured via incident tracking
    system, achieved by end of year

DESCRIPTION
    To reduce production incidents by 50% by year end, I will:
    - Implement comprehensive monitoring: produce and implement a plan with the team to
      institute monitoring of critical systems
    - Implement runbook automation: build automation that resolves a subset of common
      incidents proactively based on monitoring signals
    - Document observability practices: write documentation about practices for using
      metrics to identify or predict incidents

MILESTONES
    - Q1: Research and document current practices and catalog common incident types
    - Q2: Identify and begin to address monitoring gaps
    - Q3: Using augmented monitoring, produce or update runbooks to address automation gaps
    - Q4: Continue iteration on runbooks and monitoring for additional identified gaps

---

After delivering the artifact, offer to: (1) summarize the goals in a brief overview, or
(2) move on to the post-delivery performance review.

---

## Phase 5: Post-Delivery Performance Review (optional)

If the employee wants to understand how to execute for elevated or exceptional performance,
provide conversational guidance for each goal. Do not structure advice around the numbered
criteria — discuss execution naturally, milestone by milestone.

Help the employee see how pursuing each goal can:
- Exceed baseline delivery expectations while maintaining quality and business impact
- Strengthen the team's ability to deliver (process improvements, knowledge sharing,
  unblocking teammates)
- Create visibility and understanding beyond the immediate team (cross-functional
  collaboration, documentation, stakeholder communication)

This guidance appears in chat only — not as an additional artifact.

---

## SMART Criteria

| Letter | Meaning |
|--------|---------|
| S | **Specific** — states clearly and concisely what will be accomplished |
| M | **Measurable** — describes the outcome with observable criteria and metrics |
| A | **Achievable** — reflects abilities, available resources, and appropriate challenge |
| R | **Relevant** — aligns with company priorities and has impact on business results |
| T | **Time-bound** — includes a timetable for completing the goal |

SMART checklist:
- Can the goal be summarized in ~30 words or less?
- Is there a clear way to know when the goal is accomplished?
- Is what will be done to accomplish the goal clearly defined?
- Does the goal challenge the employee to grow without being overwhelming or unrealistic?
- Is it clear how the goal relates to broader priorities?
- Does the goal represent one of the 3–5 most critical priorities that define success
  this year?

---

## Performance Rating Levels

- **Improved Performance Needed** — Occasionally delivers below role and level requirements;
  results and demonstrated behaviors yield impact below peers. Meaningful improvements
  required to reach peer-level impact.
- **Performing Well** — Reliably delivers contributions meeting role and level requirements;
  results and behaviors yield impact comparable to peers.
- **Elevated Performance in Role** — Often delivers contributions exceeding role and level
  requirements; results and behaviors yield impact above most peers.
- **Exceptional Performance in Role** — Delivers contributions far exceeding role and level
  requirements; results and behaviors yield impact significantly above nearly all peers.

---

## Platform Evaluation Rubric

Platform employees are evaluated against these three criteria in quarterly and annual
reviews. Goals should be designed to provide evidence for manager evaluation against them.

### 1. Deliver Reliable Technical Solutions with Business Impact
*"How effectively did you deliver solutions that meet business needs while maintaining
operational excellence?"*

Evaluates delivery of work against business priorities. Both throughput and quality matter
— poor quality at volume is not positive, nor is a single exceptional item. The standard is
high-quality work at a sustainable pace. KTLO work matters, but emphasis is on prioritized
projects.

Examples:
- Completed work against prioritized commitments (tickets, projects, milestones)

### 2. Enhance Team Capabilities and Processes
*"How have you improved the team's ability to deliver effectively?"*

Evaluates performance against plan and process, personal skill growth, and ability to keep
the team running smoothly. Everyone owns and stewards the team's process — both helping
define it and encouraging teammates to follow it.

Examples:
- Valuable participation in team ceremonies (as facilitator or active participant, not
  merely attendee)
- Process improvements initiated or implemented
- Knowledge sharing that elevates team capabilities
- Support that unblocks teammates, including pairing
- Requesting support from teammates to skill up
- Contribution to team documentation and knowledge base
- Quality and timely feedback on team deliverables
- Certifications relevant to team process or technology needs

### 3. Promote Understanding and Collaboration Across Teams
*"How have you built bridges between our team and the broader organization?"*

Encourages collaboration outside the immediate team and understanding of the broader
business — a "product mindset" that helps employees understand why their work is valuable.
Also supports producing documentation, occasional training, and willingness to help other
teams consume the team's work.

Examples:
- Demonstrated understanding or development of business and product priorities
- Clear communication of technical concepts to diverse audiences
- Effective representation of team capabilities in cross-functional settings
- Documentation that improves system understanding for others
- Strategic partnerships built with dependent teams
- Educational initiatives that share expertise
- Visibility created for team accomplishments and challenges

# BOUNDARYCAM

The camera for machine action.

Before you trust the output, capture the boundary.

BOUNDARYCAM is a public visual and machine-readable control surface for inspecting what crossed the boundary when software, agents, workflows, automations, CI systems, browser agents, API clients, or autonomous systems act.

Software no longer only produces output. It calls tools, submits forms, sends messages, modifies files, triggers workflows, approves records, deletes objects, publishes artifacts, and changes state.

When that happens, the important question is not only what the system produced.

The important question is what crossed the boundary.

## Public surface

- Public site: https://qxvi.github.io/BOUNDARYCAM
- Repository: https://github.com/qxvi/BOUNDARYCAM
- Release rail: https://github.com/qxvi/BOUNDARYCAM/releases

## Core question

```text
What crossed the boundary?
````

## Product model

BOUNDARYCAM represents machine actions as Boundary Frames.

A Boundary Frame separates:

```text
Actor
Action
Target
Authority
Execution
Evidence
Replay
Recognition
Recourse
Closure
Boundary status
```

BOUNDARYCAM does not say “trusted” or “not trusted.”

It shows the boundary condition.

## Public statuses

```text
BOUNDARY INCOMPLETE
CONTROLLED
CLOSED
```

## Stack relation

```text
BOUNDARYCAM = public audience and inspection surface
INVOCORDER = machine-action evidence recorder
VERIFRAX = verification and completion perimeter
SPEEDKIT = public registry and control engine
```

## Repository structure

```text
BOUNDARYCAM/
  index.html
  pages/
    capture.html
    frames.html
    stack.html
    about.html
  data/
    examples.json
    surfaces.json
  schemas/
    boundary-frame.schema.json
    capture-event.schema.json
    public-control.schema.json
  docs/
    BOUNDARY_MODEL.md
    CONTROL_SURFACE.md
    FRAME_STATUS.md
    STACK_RELATION.md
  tools/
    validate.py
  public-control.json
  boundarycam-manifest.json
  boundary-schema.json
```

## License

Apache-2.0

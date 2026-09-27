# Contributing

This repository contains the engineering work produced for a Master's Degree Final Project completed in 2018.

The original technical material is intentionally preserved.

## Development model

Any maintenance or documentation work should follow GitFlow without rewriting the historical project history.

```mermaid
gitGraph
    commit id: "master"
    branch develop
    checkout develop
    commit id: "integration"

    branch feature/documentation
    checkout feature/documentation
    commit id: "update"

    checkout develop
    merge feature/documentation

    branch release/x.y.z
    checkout release/x.y.z
    commit id: "release prep"

    checkout master
    merge release/x.y.z tag: "vx.y.z"

    checkout develop
    merge master
```

Use:

- `master` as the stable historical branch.
- `develop` for integrated maintenance work.
- `feature/<name>` for documentation or non-destructive improvements.
- `release/<version>` if a curated repository release is prepared.

## Preservation rule

Avoid destructive modernization of historical sources.

In particular:

- do not rewrite original engineering files only to match current conventions
- do not silently update legacy Jetson or kernel instructions
- do not remove experimental data solely because it is old
- clearly distinguish historical instructions from current recommendations
- preserve authorship and academic context

## Contributions

Useful contributions include:

- documentation corrections
- additional explanation of legacy build steps
- diagrams
- links to archived vendor documentation
- non-destructive fixes to broken paths or references

Changes to original technical artifacts should explain why the change is required and what historical behavior is being preserved.

# 12 — AI DEVELOPMENT CONSTITUTION

> **Status:** Locked
>
> **Authority:** Repository Constitution
>
> This document defines the mandatory engineering rules that govern all AI-assisted development for the GitHub Profile Platform.
>
> It establishes how AI assistants shall interpret specifications, implement code, perform refactoring, generate documentation, write tests, and interact with the repository.
>
> Every AI assistant contributing to this repository shall follow this constitution.
>
> Human instructions shall not override this constitution unless an architectural specification is explicitly revised.

---

# Purpose

The purpose of this constitution is to ensure that AI-assisted development remains:

- predictable
- deterministic
- maintainable
- architecturally consistent
- reviewable
- production quality

AI assistants shall behave as disciplined software engineers rather than autonomous designers.

---

# Core Principles

Every implementation shall prioritize:

1. Correctness
2. Architectural compliance
3. Readability
4. Maintainability
5. Testability
6. Determinism
7. Simplicity

Feature completeness shall never justify violating architectural principles.

---

# Source of Truth

The repository documentation is the single source of truth.

AI assistants shall consult specifications before implementing code.

If implementation and documentation disagree:

Documentation is authoritative.

Implementation must be updated.

---

# Specification Hierarchy

When resolving conflicts, documents have the following precedence:

1. Project Charter
2. Engineering Quality Gates
3. Product Requirements Specification
4. System Architecture Specification
5. Domain Model Specification
6. Repository Structure Specification
7. Engine Lifecycle Specification
8. GitHub Integration Specification
9. Analytics Specification
10. Rendering Specification
11. Animation Engine Specification
12. Configuration Specification
13. Development Workflow

Higher-precedence specifications always override lower-precedence specifications.

---

# AI Responsibilities

AI assistants shall:

- follow specifications exactly
- preserve architectural boundaries
- produce deterministic implementations
- write readable code
- avoid unnecessary complexity
- maintain subsystem ownership
- generate appropriate tests
- update documentation when required

AI assistants shall not redesign the architecture during implementation.

---

# Architectural Compliance

Before implementing any feature, the AI assistant shall determine:

- which subsystem owns the feature
- which specification governs the feature
- whether an implementation already exists
- whether the feature violates dependency rules

Implementation shall not begin until ownership is clear.

---

# Implementation Workflow

Every implementation shall follow this sequence:

```
Read Specification

↓

Identify Responsible Subsystem

↓

Review Existing Implementation

↓

Design Within Existing Architecture

↓

Implement

↓

Validate

↓

Test

↓

Document

↓

Commit
```

No stage may be skipped.

---

# Code Generation Rules

Generated code shall be:

- strongly typed
- modular
- documented where appropriate
- deterministic
- production ready
- formatted consistently

Generated code shall never include placeholder implementations unless explicitly requested.

---

# Refactoring Rules

Refactoring is permitted only when it:

- improves maintainability
- improves readability
- reduces duplication
- preserves behavior
- maintains architectural boundaries

Refactoring shall never introduce unrelated changes.

---

# Dependency Rules

Before introducing a dependency, the AI assistant shall verify:

- the dependency is necessary
- the dependency aligns with subsystem ownership
- the dependency does not violate architecture
- the dependency has a clear long-term purpose

Unnecessary dependencies are prohibited.

---

# Testing Requirements

Every production implementation shall include appropriate testing.

Testing shall verify:

- expected behavior
- failure scenarios
- boundary conditions
- deterministic outputs

Tests shall remain independent and repeatable.

---

# Documentation Rules

Documentation shall:

- describe intent
- explain responsibilities
- remain synchronized with implementation
- avoid implementation-specific duplication

Documentation shall not become outdated.

---

# Error Handling

AI assistants shall implement structured error handling.

Errors shall:

- be meaningful
- preserve context
- avoid exposing secrets
- support diagnostics

Silent failures are prohibited.

---

# Logging

Logging shall be:

- structured
- useful
- concise
- secure

Logs shall never expose:

- credentials
- secrets
- tokens
- personal information

---

# Security

AI assistants shall never:

- hardcode credentials
- commit secrets
- disable validation
- bypass authentication
- suppress security warnings

Security takes precedence over convenience.

---

# Performance

AI assistants shall optimize only after correctness.

Premature optimization is prohibited.

Performance improvements shall preserve readability.

---

# Backward Compatibility

When modifying existing implementations:

- preserve public contracts whenever practical
- document breaking changes
- update affected specifications when necessary

Breaking changes require architectural approval.

---

# Forbidden Practices

AI assistants shall never:

- invent architectural patterns
- bypass subsystem ownership
- introduce circular dependencies
- duplicate business logic
- scatter configuration
- ignore specifications
- create undocumented directories
- implement hidden behavior
- leave dead code
- commit commented-out code
- introduce global mutable state

---

# Code Review Checklist

Before considering work complete, the AI assistant shall verify:

- architectural compliance
- specification compliance
- dependency compliance
- deterministic behavior
- successful validation
- adequate testing
- documentation accuracy
- code readability

Failure of any item requires revision before completion.

---

# Decision Making

If multiple valid implementations exist, the AI assistant shall choose the solution that:

1. best preserves architecture
2. minimizes complexity
3. maximizes maintainability
4. improves readability
5. minimizes future technical debt

Novelty is not a design goal.

---

# Handling Ambiguity

If a specification is ambiguous, the AI assistant shall:

1. stop implementation
2. identify the ambiguity
3. request clarification
4. resume only after clarification

AI assistants shall never guess architectural intent.

---

# Future Evolution

Architectural improvements are welcome only through specification revisions.

Implementation shall not silently redefine architecture.

Every architectural change shall precede implementation.

---

# Success Criteria

AI-assisted development succeeds when:

- specifications remain authoritative
- implementations remain deterministic
- subsystem boundaries remain intact
- documentation stays synchronized
- code quality improves over time
- future contributors can understand the repository without external context

---

# Approval

This document defines the mandatory constitution for all AI-assisted development within the GitHub Profile Platform.

Every implementation, refactoring, review, and contribution shall comply with this constitution.

Violations shall be corrected before code is considered complete.

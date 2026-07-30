# 09 — RENDERING SPECIFICATION

> **Status:** Locked
>
> **Authority:** Repository Constitution
>
> This document defines the Rendering subsystem of the GitHub Profile Platform.
>
> It specifies the rendering architecture, rendering contracts, supported output formats, rendering lifecycle, template system, output generation, extensibility model, and subsystem boundaries.
>
> The Rendering subsystem is the sole authority responsible for converting rendering models into user-visible artifacts.
>
> No other subsystem may generate visual assets or presentation outputs.

---

# Purpose

The Rendering subsystem transforms rendering models into production-quality artifacts.

Rendering is purely a presentation concern.

The Rendering subsystem does not:

- communicate with GitHub
- perform analytics
- infer skills
- calculate statistics
- classify repositories
- execute business logic

Rendering consumes prepared rendering models and produces visual outputs.

---

# Design Philosophy

The Rendering subsystem shall be:

- deterministic
- modular
- template-driven
- extensible
- reusable
- strongly typed
- implementation independent

Rendering shall never influence business logic.

Presentation must remain completely isolated from computation.

---

# Architectural Position

```
GitHub

↓

Collectors

↓

Analytics

↓

Generators

↓

Rendering Models

↓

Renderers

↓

Generated Assets
```

Rendering always represents the final transformation stage before assets are written to disk.

---

# Primary Responsibilities

The Rendering subsystem owns:

- Markdown generation
- SVG generation
- JSON export
- asset assembly
- template rendering
- theme application
- typography
- layout
- responsive asset generation
- metadata generation

The subsystem shall never own:

- GitHub communication
- analytics
- repository scoring
- skill inference
- contribution calculations
- filesystem orchestration
- workflow automation

---

# Rendering Philosophy

Renderers receive immutable rendering models.

Renderers never modify rendering models.

Renderers never query GitHub.

Renderers never perform calculations that belong to Analytics.

Renderers only transform structured rendering models into visual representations.

---

# Supported Output Formats

The platform shall initially support:

- Markdown
- SVG
- JSON

Future output formats may include:

- HTML
- PNG
- PDF
- Web Components
- Interactive Dashboard Assets

The addition of future formats shall not require modifications to existing renderers.

---

# Rendering Pipeline

Every rendering operation shall follow the same lifecycle.

```
Receive Rendering Model

↓

Validate Input

↓

Resolve Theme

↓

Load Templates

↓

Render Components

↓

Assemble Document

↓

Validate Output

↓

Export Asset
```

Every stage is deterministic.

No rendering stage may be skipped.

---

# Rendering Models

Renderers consume rendering models produced by the Generator subsystem.

Rendering models contain only presentation-ready information.

Renderers shall never derive analytical values independently.

---

# Markdown Renderer

Responsibilities:

- GitHub README generation
- Markdown formatting
- section ordering
- badges
- tables
- links
- project summaries

Markdown generation shall remain deterministic.

---

# SVG Renderer

Responsibilities:

- dashboards
- statistics cards
- engineering metrics
- skill maps
- timelines
- charts
- contribution visualizations
- project graphics

SVG shall remain resolution independent.

SVG assets shall support animation.

---

# JSON Renderer

Responsibilities:

- machine-readable exports
- debugging
- external integrations
- future APIs

JSON exports shall mirror rendering models.

---

# Component-Based Rendering

All renderers shall be composed from reusable components.

Examples include:

- Hero Section
- About Section
- Statistics Card
- Repository Card
- Skill Card
- Timeline
- Activity Feed
- Research Section
- Footer

Components shall remain independent.

Components shall never communicate directly with one another.

---

# Layout System

Layouts shall be generated from rendering models.

Layouts shall remain independent of Analytics.

Layouts shall support future themes without structural modification.

---

# Theme Resolution

Themes define presentation only.

Themes may configure:

- colors
- typography
- spacing
- icon sets
- gradients
- shadows
- border styles
- animation presets

Themes shall never influence business logic.

---

# Template System

Templates shall define presentation.

Templates shall remain stateless.

Templates shall never perform business logic.

Template responsibilities include:

- formatting
- positioning
- styling
- presentation hierarchy

---

# Rendering Contracts

Every renderer shall satisfy the following contract:

Input:

- Rendering Model

Output:

- Generated Asset

Renderers shall never return partial outputs.

Rendering failures shall produce structured diagnostics.

---

# Asset Generation

Generated assets include:

- README.md
- SVG dashboards
- repository cards
- timeline graphics
- animated statistics
- skill maps
- engineering charts

Future assets shall integrate without modifying existing renderers.

---

# Validation

Every generated asset shall be validated before export.

Validation includes:

- syntax correctness
- structural completeness
- required sections
- template integrity
- rendering consistency

Invalid assets shall never be published.

---

# Error Handling

Rendering errors shall be classified as:

## Template Errors

Examples:

- missing template
- malformed template
- invalid placeholders

---

## Theme Errors

Examples:

- missing colors
- invalid configuration
- unsupported typography

---

## Rendering Errors

Examples:

- invalid rendering model
- missing required component
- unsupported asset type

Rendering failures shall never corrupt existing generated assets.

---

# Performance

Rendering shall prioritize:

1. correctness
2. determinism
3. consistency

Performance optimization shall not reduce maintainability.

---

# Observability

The subsystem shall expose diagnostics including:

- rendered assets
- render duration
- templates used
- theme applied
- warnings
- validation results

---

# Dependency Rules

Renderers may depend on:

- rendering models
- themes
- templates
- infrastructure services

Renderers shall never depend on:

- GitHub Integration
- Collectors
- Analytics
- Configuration internals
- Automation

---

# Extension Points

Future rendering capabilities may include:

- interactive dashboards
- animated portfolio pages
- developer portfolios
- résumé generation
- architecture diagrams
- documentation websites
- presentation decks
- export plugins

Future extensions shall preserve existing rendering contracts.

---

# Forbidden Practices

The Rendering subsystem shall never:

- communicate with GitHub
- infer analytical information
- modify rendering models
- implement business logic
- perform repository classification
- access raw API responses
- maintain hidden mutable state

Presentation and computation shall remain permanently separated.

---

# AI Development Rules

Before implementing any Rendering component, the AI assistant shall verify:

1. The implementation belongs to the Rendering subsystem.
2. Inputs are rendering models only.
3. No analytical logic is introduced.
4. No GitHub communication is introduced.
5. Output conforms to rendering contracts.
6. Themes affect presentation only.
7. Templates remain stateless.

If any requirement cannot be satisfied, implementation shall stop until clarification is obtained.

The AI assistant shall never compute business metrics inside a renderer.

The AI assistant shall never bypass the Generator subsystem.

The AI assistant shall never embed GitHub API logic into rendering components.

---

# Success Criteria

The Rendering subsystem succeeds when:

- every output is deterministic
- rendering remains independent of analytics
- themes are interchangeable
- templates are reusable
- generated assets are production quality
- visual consistency is maintained
- future output formats integrate without architectural redesign

---

# Approval

This document defines the canonical Rendering subsystem.

All rendering implementations shall conform to this specification.

Architectural deviations require explicit approval before implementation.

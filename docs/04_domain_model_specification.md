# 04 — DOMAIN MODEL SPECIFICATION

> **Status:** Locked
>
> This document defines the canonical domain models used throughout the platform.
>
> Domain models represent business concepts.
>
> They are independent of GitHub APIs, rendering formats, storage mechanisms, and implementation details.
>
> Every subsystem communicates using these models.

---

# Purpose

The purpose of this document is to establish a stable language for the entire platform.

Every subsystem must exchange information using domain models.

No subsystem may expose raw external API objects outside its own boundary.

---

# Design Principles

Domain models shall be:

- immutable whenever practical
- implementation independent
- serialization friendly
- deterministic
- reusable
- strongly typed

---

# Domain Model Hierarchy

The platform uses the following canonical models:

```
GitHubProfile
│
├── User
├── Repository[]
├── ContributionMetrics
├── LanguageMetrics
├── ActivityMetrics
├── FeaturedProject[]
├── Skill
├── TimelineEvent[]
├── ResearchItem[]
├── Statistics
├── ThemeConfiguration
└── GeneratedAsset[]
```

---

# User

Represents the owner of the GitHub profile.

Responsibilities:

- identity
- biography
- location
- profile links
- social links

Must not contain analytics.

---

# Repository

Represents a single repository.

Contains only normalized information.

Examples:

- repository name
- description
- visibility
- language
- stars
- forks
- topics
- license
- timestamps

Must never expose raw GitHub API responses.

---

# Featured Project

Represents repositories selected for showcase.

Contains:

- summary
- technologies
- highlights
- project status
- repository reference

Selection logic belongs to Analytics, not this model.

---

# Contribution Metrics

Represents engineering activity.

Examples:

- commits
- pull requests
- issues
- reviews
- contribution streak
- activity score

Contains metrics only.

---

# Language Metrics

Represents language usage.

Examples:

- language name
- percentage
- repository count
- activity score

---

# Activity Metrics

Represents recent engineering activity.

Examples:

- commits
- repository creation
- releases
- pull requests
- stars earned

---

# Statistics

Represents aggregated platform metrics.

Examples:

- repositories
- commits
- stars
- forks
- releases
- followers
- contribution totals

---

# Skill

Represents an engineering skill inferred from repositories.

Examples:

- Machine Learning
- Python
- Docker
- FastAPI
- TensorFlow

Skill inference belongs to Analytics.

---

# Timeline Event

Represents significant milestones.

Examples:

- repository created
- graduation
- certification
- major release
- project completion

Timeline ordering is chronological.

---

# Research Item

Represents research-oriented work.

Examples:

- publication
- paper implementation
- experiment
- benchmark

---

# Theme Configuration

Represents visual customization.

Contains:

- colors
- typography
- animation settings
- spacing
- icons

Contains presentation only.

---

# Generated Asset

Represents generated outputs.

Examples:

- README
- SVG
- Markdown
- JSON
- PNG (future)

Contains metadata about generated artifacts.

---

# Relationships

```
GitHubProfile

├── User

├── Repository[]

│      └── FeaturedProject

├── Statistics

├── ContributionMetrics

├── LanguageMetrics

├── ActivityMetrics

├── TimelineEvent[]

├── ResearchItem[]

├── Skill[]

├── ThemeConfiguration

└── GeneratedAsset[]
```

---

# Ownership Rules

Collectors create domain models.

Analytics enrich domain models.

Generators assemble domain models.

Renderers consume domain models.

Renderers must never modify domain models.

---

# Prohibited Practices

The following are forbidden:

- raw GitHub responses outside Integration
- renderer-specific fields
- analytics-specific temporary values
- mutable shared objects
- duplicated models

---

# Versioning

Future model evolution must preserve backward compatibility whenever practical.

Breaking changes require architectural review.

---

# Success Criteria

The domain layer succeeds when:

- every subsystem speaks the same language
- API responses are normalized once
- rendering is implementation independent
- analytics remain isolated
- models remain reusable

---

# Approval

This document defines the canonical domain language of the platform.

Every future implementation must use these models as the single source of truth.

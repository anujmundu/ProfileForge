"""Template Loader for Rendering Subsystem.

Loads rendering templates for Markdown and SVG visual cards.
Governed by 09_RENDERING_SPECIFICATION.md.
"""




class TemplateLoader:
    """Centralized template provider."""

    DEFAULT_MARKDOWN_TEMPLATE: str = """# {{ profile.display_name }}

> {{ profile.headline }}

{{ profile.summary }}

---

### Portfolio Overview

- **Public Repositories**: {{ statistics.total_repositories }}
- **Total Stars**: {{ statistics.total_stars }}
- **Total Forks**: {{ statistics.total_forks }}
- **Primary Language**: {{ statistics.dominant_language }}

---

### Featured Projects

{% for project in featured_projects.projects %}
#### [{{ project.name }}]({{ project.html_url }})
{{ project.description }}
- **Stars**: {{ project.stars }} | **Forks**: {{ project.forks }} | **Language**: {{ project.language }}

{% endfor %}

---

### Technology Stack

{% for group in technology_stack.groups %}
- **{{ group.category_name }}**: {{ group.technologies | join(', ') }}
{% endfor %}

---

### Achievements

{% for item in achievements.achievements %}
- **{{ item.title }}**: {{ item.description }}
{% endfor %}
"""

    def get_markdown_template(self) -> str:
        """Get default Markdown README Jinja template."""
        return self.DEFAULT_MARKDOWN_TEMPLATE

# Skills Repository

A collection of development skills and patterns organized for both humans and LLMs.

## 🌐 Website

Visit the GitHub Pages website: **https://joshspicer.com/skills/**

The website automatically updates whenever the main branch is updated.

## 📚 Available Skills

### iOS Project Setup
Standard patterns for setting up iOS projects including MCP server configuration, Info.plist handling, version/commit embedding, server components, and more.

[View full documentation](ios-project-setup/SKILL.md)

## 🤖 LLM Integration

A structured `llm.txt` file is available at https://joshspicer.github.io/skills/llm.txt for LLM consumption. This file contains:
- Repository information
- Detailed skill descriptions
- Key topics and patterns
- File structure examples
- Usage guidance

## 📖 Structure

Each skill is organized in its own directory with:
- `SKILL.md` - Main skill documentation with YAML frontmatter
- `references/` - Detailed reference documentation

Example structure:
```
skill-name/
├── SKILL.md           # Main documentation
└── references/        # Detailed references
    ├── topic1.md
    └── topic2.md
```

## 🚀 Adding New Skills

1. Create a new directory for your skill
2. Add a `SKILL.md` file with YAML frontmatter:

```yaml
---
name: skill-name
description: Brief description of the skill
metadata:
  author: your-name
  version: "1.0"
compatibility: Requirements and compatibility notes
---

# Skill Name

Your detailed documentation here...
```

3. Optionally add reference documentation in a `references/` subdirectory
4. Commit to the main branch - the website will automatically update

## 🛠 Development

The GitHub Pages site is built from the `docs/` directory and automatically deployed via GitHub Actions when changes are pushed to the main branch.

### Local Testing

To test the website locally:

```bash
cd docs
python3 -m http.server 8000
```

Then visit http://localhost:8000

## 📄 License

Skills are provided as-is for reference and learning purposes.

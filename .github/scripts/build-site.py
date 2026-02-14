#!/usr/bin/env python3
"""
Build static HTML site from SKILL.md files
"""

import os
import re
import yaml
import markdown
import shutil
from pathlib import Path
from typing import Dict, List, Any

# Configuration
REPO_ROOT = Path(__file__).parent.parent.parent
TEMPLATES_DIR = REPO_ROOT / ".github" / "templates"
OUTPUT_DIR = REPO_ROOT / "docs"

def find_skill_files() -> List[Path]:
    """Find all SKILL.md files in the repository"""
    skill_files = []
    for path in REPO_ROOT.rglob("SKILL.md"):
        # Skip docs directory
        if "docs" not in path.parts:
            skill_files.append(path)
    return skill_files

def find_reference_files(skill_folder: Path) -> List[Path]:
    """Find all reference markdown files in a skill's references directory"""
    references_dir = REPO_ROOT / skill_folder / "references"
    if not references_dir.exists():
        return []
    return list(references_dir.glob("*.md"))

def convert_md_links_to_html(content: str) -> str:
    """Convert .md links to .html links in markdown/HTML content"""
    # Match markdown links and href attributes containing .md files
    # Handles cases like: path.md, path.md#section, path.md?param=value
    def replace_md_extension(match):
        return match.group(0).replace('.md', '.html')
    
    # Replace .md with .html in href attributes (handles fragments and query params)
    content = re.sub(r'href="[^"]*\.md([#?][^"]*)?"', replace_md_extension, content)
    # Replace .md with .html in markdown link syntax (handles fragments and query params)
    content = re.sub(r'\]\([^)]*\.md([#?][^)]*)?\)', replace_md_extension, content)
    return content

def parse_skill_file(file_path: Path) -> Dict[str, Any]:
    """Parse a SKILL.md file and extract frontmatter and content"""
    content = file_path.read_text()

    # Extract YAML frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)

    if not frontmatter_match:
        return None

    frontmatter_text = frontmatter_match.group(1)
    body_content = frontmatter_match.group(2).strip()

    # Parse YAML
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return None

    # Get skill folder
    skill_folder = file_path.parent.relative_to(REPO_ROOT)
    skill_id = str(skill_folder).replace(os.sep, '-')

    return {
        'id': skill_id,
        'name': frontmatter.get('name', 'Unnamed Skill'),
        'description': frontmatter.get('description', 'No description'),
        'metadata': frontmatter.get('metadata', {}),
        'compatibility': frontmatter.get('compatibility', ''),
        'content': body_content,
        'folder': str(skill_folder)
    }

def generate_index_html(skills: List[Dict[str, Any]]) -> str:
    """Generate the index.html file"""
    skills_html = ""

    for skill in skills:
        author = skill['metadata'].get('author', '')
        version = skill['metadata'].get('version', '')

        meta_parts = []
        if author:
            meta_parts.append(f'<span>Author: {escape_html(author)}</span>')
        if version:
            meta_parts.append(f'<span>v{escape_html(version)}</span>')

        meta_html = ""
        if meta_parts:
            meta_html = f'<div class="skill-meta">{"".join(meta_parts)}</div>'

        skills_html += f'''
        <div class="skill-card" onclick="location.href='{skill['id']}.html'">
            <h3>{escape_html(skill['name'])}</h3>
            <p>{escape_html(skill['description'])}</p>
            {meta_html}
        </div>
        '''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Developer Skills Hub</title>
    <link rel="stylesheet" href="styles.css">
    <meta name="description" content="A curated collection of development patterns, configurations, and best practices for modern software engineering">
</head>
<body>
    <header>
        <div class="container">
            <h1>Developer Skills Hub</h1>
            <p class="subtitle">Curated patterns and best practices for modern development</p>
        </div>
    </header>

    <main class="container">
        <section id="skills-list">
            <h2>Available Skills</h2>
            <div class="skills-grid">
                {skills_html}
            </div>
        </section>
    </main>

    <footer>
        <div class="container">
            <p>
                <a href="https://github.com/joshspicer/skills" target="_blank" rel="noopener">View on GitHub</a>
                |
                <a href="llm.txt">llm.txt</a>
            </p>
        </div>
    </footer>
</body>
</html>
'''

def generate_skill_html(skill: Dict[str, Any]) -> str:
    """Generate HTML for a single skill page"""
    # Convert .md links to .html before markdown processing
    content_with_html_links = convert_md_links_to_html(skill['content'])
    md = markdown.Markdown(extensions=['fenced_code', 'tables', 'nl2br'])
    content_html = md.convert(content_with_html_links)

    author = skill['metadata'].get('author', '')
    version = skill['metadata'].get('version', '')

    meta_rows = ""
    if skill['compatibility']:
        meta_rows += f"<p><strong>Compatibility:</strong> {escape_html(skill['compatibility'])}</p>"
    if author:
        meta_rows += f"<p><strong>Author:</strong> {escape_html(author)}</p>"
    if version:
        meta_rows += f"<p><strong>Version:</strong> {escape_html(version)}</p>"

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape_html(skill['name'])} - Developer Skills Hub</title>
    <link rel="stylesheet" href="styles.css">
    <meta name="description" content="{escape_html(skill['description'])}">
</head>
<body>
    <header>
        <div class="container">
            <h1>Developer Skills Hub</h1>
            <p class="subtitle">Curated patterns and best practices for modern development</p>
        </div>
    </header>

    <main class="container">
        <section>
            <a href="index.html" class="btn-back">&larr; Back to Skills</a>

            <div id="skill-content">
                <h1>{escape_html(skill['name'])}</h1>
                <p><strong>Description:</strong> {escape_html(skill['description'])}</p>
                {meta_rows}
                <hr style="margin: 20px 0; border: none; border-top: 1px solid var(--border-color);">
                {content_html}
            </div>
        </section>
    </main>

    <footer>
        <div class="container">
            <p>
                <a href="https://github.com/joshspicer/skills" target="_blank" rel="noopener">View on GitHub</a>
                |
                <a href="llm.txt">llm.txt</a>
            </p>
        </div>
    </footer>
</body>
</html>
'''

def escape_html(text: str) -> str:
    """Escape HTML special characters"""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))

def generate_reference_html(ref_file: Path, skill_id: str, skill_name: str) -> str:
    """Generate HTML for a reference page"""
    try:
        content = ref_file.read_text(encoding='utf-8')
    except (IOError, UnicodeDecodeError) as e:
        print(f"  Warning: Could not read {ref_file}: {e}")
        return None
    
    # Convert .md links to .html before markdown processing
    content_with_html_links = convert_md_links_to_html(content)
    
    md = markdown.Markdown(extensions=['fenced_code', 'tables', 'nl2br'])
    content_html = md.convert(content_with_html_links)
    
    # Extract title from first heading or filename
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else ref_file.stem.replace('-', ' ').title()
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape_html(title)} - {escape_html(skill_name)} - Developer Skills Hub</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <header>
        <div class="container">
            <h1>Developer Skills Hub</h1>
            <p class="subtitle">Curated patterns and best practices for modern development</p>
        </div>
    </header>

    <main class="container">
        <section>
            <a href="../{skill_id}.html" class="btn-back">&larr; Back to {escape_html(skill_name)}</a>

            <div id="skill-content">
                {content_html}
            </div>
        </section>
    </main>

    <footer>
        <div class="container">
            <p>
                <a href="https://github.com/joshspicer/skills" target="_blank" rel="noopener">View on GitHub</a>
                |
                <a href="../llm.txt">llm.txt</a>
            </p>
        </div>
    </footer>
</body>
</html>
'''

def update_llm_txt(skills: List[Dict[str, Any]]) -> str:
    """Generate llm.txt content"""
    skills_section = ""

    for skill in skills:
        author = skill['metadata'].get('author', '')
        version = skill['metadata'].get('version', '')

        skills_section += f'''
### {skill['name']}
**Description:** {skill['description']}
'''
        if author:
            skills_section += f"**Author:** {author}\n"
        if version:
            skills_section += f"**Version:** {version}\n"
        if skill['compatibility']:
            skills_section += f"**Compatibility:** {skill['compatibility']}\n"

        skills_section += "\n---\n"

    return f'''# Developer Skills Hub - LLM Knowledge Base

This file provides structured information about available skills in this repository for LLM consumption.

## Repository Information
- Repository: joshspicer/skills
- Purpose: Curated collection of development patterns, configurations, and best practices
- Format: Each skill is documented in a SKILL.md file with YAML frontmatter

## Available Skills
{skills_section}

## How to Use This Knowledge Base

### For LLMs:
1. When a user asks about skills in this repository, reference the skill descriptions above
2. Each skill provides comprehensive patterns for specific development tasks
3. Pay attention to the compatibility requirements and metadata
4. Skills are self-contained and can be referenced independently

### For Humans:
- Visit https://joshspicer.github.io/skills/ for a formatted web interface
- Each skill includes detailed documentation with code examples
- Click on individual skills to see full documentation

## Update Information
This file is automatically updated when the main branch is updated via GitHub Actions.
Last updated: {os.popen('date -u +"%Y-%m-%d %H:%M:%S UTC"').read().strip()}
'''

def main():
    """Main build function"""
    print("Building static site...")

    # Find all skills
    skill_files = find_skill_files()
    print(f"Found {len(skill_files)} skill files")

    # Parse skills
    skills = []
    for skill_file in skill_files:
        skill = parse_skill_file(skill_file)
        if skill:
            skills.append(skill)
            print(f"  - {skill['name']}")

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Copy CSS from templates
    css_source = TEMPLATES_DIR / "styles.css"
    css_dest = OUTPUT_DIR / "styles.css"
    shutil.copy2(css_source, css_dest)
    print("Copied styles.css from templates")

    # Generate index page
    index_html = generate_index_html(skills)
    (OUTPUT_DIR / "index.html").write_text(index_html)
    print("Generated index.html")

    # Generate individual skill pages
    for skill in skills:
        skill_html = generate_skill_html(skill)
        output_file = OUTPUT_DIR / f"{skill['id']}.html"
        output_file.write_text(skill_html)
        print(f"Generated {skill['id']}.html")
        
        # Generate reference pages for this skill
        ref_files = find_reference_files(Path(skill['folder']))
        if ref_files:
            # Create references subdirectory for this skill
            refs_output_dir = OUTPUT_DIR / "references"
            refs_output_dir.mkdir(exist_ok=True)
            
            for ref_file in ref_files:
                ref_html = generate_reference_html(ref_file, skill['id'], skill['name'])
                if ref_html is None:
                    continue
                ref_output_file = refs_output_dir / f"{ref_file.stem}.html"
                ref_output_file.write_text(ref_html)
                print(f"  Generated references/{ref_file.stem}.html")

    # Update llm.txt
    llm_txt = update_llm_txt(skills)
    (OUTPUT_DIR / "llm.txt").write_text(llm_txt)
    print("\nUpdated llm.txt")

    print("\nBuild complete!")

if __name__ == "__main__":
    main()

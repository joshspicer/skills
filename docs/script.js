// GitHub repository information
const REPO_OWNER = 'joshspicer';
const REPO_NAME = 'skills';
const BRANCH = 'main';

// Skill data will be loaded dynamically
let skillsData = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    loadSkills();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    document.getElementById('back-button').addEventListener('click', showSkillsList);
}

// Load skills from the repository
async function loadSkills() {
    const container = document.getElementById('skills-container');

    try {
        // Fetch the repository tree to find all SKILL.md files
        const treeUrl = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/git/trees/${BRANCH}?recursive=1`;
        const treeResponse = await fetch(treeUrl);
        const treeData = await treeResponse.json();

        // Find all SKILL.md files
        const skillFiles = treeData.tree.filter(item =>
            item.path.endsWith('/SKILL.md') || item.path === 'SKILL.md'
        );

        if (skillFiles.length === 0) {
            container.innerHTML = '<p class="error">No skills found in the repository.</p>';
            return;
        }

        // Load each skill file
        const skillPromises = skillFiles.map(file => loadSkillFile(file.path));
        skillsData = await Promise.all(skillPromises);

        // Filter out any failed loads
        skillsData = skillsData.filter(skill => skill !== null);

        // Display the skills
        displaySkills();

    } catch (error) {
        console.error('Error loading skills:', error);
        container.innerHTML = '<p class="error">Failed to load skills. Please try again later.</p>';
    }
}

// Load a single skill file
async function loadSkillFile(path) {
    try {
        const fileUrl = `https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/${BRANCH}/${path}`;
        const response = await fetch(fileUrl);
        const content = await response.text();

        // Parse the skill file
        const skill = parseSkillFile(content, path);
        return skill;

    } catch (error) {
        console.error(`Error loading skill file ${path}:`, error);
        return null;
    }
}

// Parse skill file content
function parseSkillFile(content, path) {
    // Extract YAML frontmatter
    const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);

    if (!frontmatterMatch) {
        return null;
    }

    const frontmatter = parseFrontmatter(frontmatterMatch[1]);
    const bodyContent = content.substring(frontmatterMatch[0].length).trim();

    // Get the directory name (skill folder name)
    const skillFolder = path.split('/').slice(0, -1).join('/');

    return {
        name: frontmatter.name || 'Unnamed Skill',
        description: frontmatter.description || 'No description available',
        metadata: frontmatter.metadata || {},
        compatibility: frontmatter.compatibility || '',
        content: bodyContent,
        path: path,
        folder: skillFolder
    };
}

// Simple YAML frontmatter parser
function parseFrontmatter(yaml) {
    const lines = yaml.split('\n');
    const result = {};
    let currentKey = null;
    let currentValue = '';
    let inMetadata = false;

    for (const line of lines) {
        if (line.startsWith('metadata:')) {
            inMetadata = true;
            result.metadata = {};
            continue;
        }

        if (inMetadata) {
            if (line.match(/^\w+:/)) {
                // End of metadata section
                inMetadata = false;
            } else if (line.trim().startsWith('author:') || line.trim().startsWith('version:')) {
                const [key, ...valueParts] = line.trim().split(':');
                result.metadata[key.trim()] = valueParts.join(':').trim().replace(/^["']|["']$/g, '');
                continue;
            }
        }

        if (line.includes(':')) {
            // Save previous key-value pair
            if (currentKey) {
                result[currentKey] = currentValue.trim().replace(/^["']|["']$/g, '');
            }

            const colonIndex = line.indexOf(':');
            currentKey = line.substring(0, colonIndex).trim();
            currentValue = line.substring(colonIndex + 1).trim();
        } else if (currentKey && line.trim()) {
            // Multi-line value
            currentValue += ' ' + line.trim();
        }
    }

    // Save last key-value pair
    if (currentKey) {
        result[currentKey] = currentValue.trim().replace(/^["']|["']$/g, '');
    }

    return result;
}

// Display skills in the grid
function displaySkills() {
    const container = document.getElementById('skills-container');

    if (skillsData.length === 0) {
        container.innerHTML = '<p class="error">No skills found.</p>';
        return;
    }

    container.innerHTML = '';

    skillsData.forEach((skill, index) => {
        const card = createSkillCard(skill, index);
        container.appendChild(card);
    });
}

// Create a skill card element
function createSkillCard(skill, index) {
    const card = document.createElement('div');
    card.className = 'skill-card';
    card.onclick = () => showSkillDetail(index);

    card.innerHTML = `
        <h3>${escapeHtml(skill.name)}</h3>
        <p>${escapeHtml(skill.description)}</p>
        ${createSkillMeta(skill)}
    `;

    return card;
}

// Create skill metadata section
function createSkillMeta(skill) {
    const metaParts = [];

    if (skill.metadata.author) {
        metaParts.push(`<span>Author: ${escapeHtml(skill.metadata.author)}</span>`);
    }

    if (skill.metadata.version) {
        metaParts.push(`<span>v${escapeHtml(skill.metadata.version)}</span>`);
    }

    if (metaParts.length === 0) {
        return '';
    }

    return `<div class="skill-meta">${metaParts.join('')}</div>`;
}

// Show skill detail view
function showSkillDetail(index) {
    const skill = skillsData[index];

    // Hide skills list, show detail
    document.getElementById('skills-list').classList.add('hidden');
    document.getElementById('skill-detail').classList.remove('hidden');

    // Render the skill content
    const contentDiv = document.getElementById('skill-content');
    contentDiv.innerHTML = `
        <h1>${escapeHtml(skill.name)}</h1>
        <p><strong>Description:</strong> ${escapeHtml(skill.description)}</p>
        ${skill.compatibility ? `<p><strong>Compatibility:</strong> ${escapeHtml(skill.compatibility)}</p>` : ''}
        ${skill.metadata.author ? `<p><strong>Author:</strong> ${escapeHtml(skill.metadata.author)}</p>` : ''}
        ${skill.metadata.version ? `<p><strong>Version:</strong> ${escapeHtml(skill.metadata.version)}</p>` : ''}
        <hr style="margin: 20px 0; border: none; border-top: 1px solid var(--border-color);">
        ${renderMarkdown(skill.content)}
    `;

    // Scroll to top
    window.scrollTo(0, 0);
}

// Show skills list view
function showSkillsList() {
    document.getElementById('skills-list').classList.remove('hidden');
    document.getElementById('skill-detail').classList.add('hidden');
    window.scrollTo(0, 0);
}

// Simple markdown renderer (handles common cases)
function renderMarkdown(markdown) {
    let html = markdown;

    // Code blocks
    html = html.replace(/```(\w+)?\n([\s\S]*?)```/g, (match, lang, code) => {
        return `<pre><code>${escapeHtml(code.trim())}</code></pre>`;
    });

    // Inline code
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Headers
    html = html.replace(/^### (.*$)/gm, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gm, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gm, '<h1>$1</h1>');

    // Bold
    html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

    // Links
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');

    // Lists
    html = html.replace(/^(\d+)\. (.*)$/gm, '<li>$2</li>');
    html = html.replace(/^[\-\*] (.*)$/gm, '<li>$1</li>');

    // Wrap consecutive <li> items in <ul> or <ol>
    html = html.replace(/(<li>.*<\/li>\n?)+/g, match => {
        return `<ul>${match}</ul>`;
    });

    // Tables (basic support)
    html = html.replace(/\|(.+)\|\n\|[-:\s|]+\|\n((?:\|.+\|\n?)+)/g, (match, header, rows) => {
        const headers = header.split('|').filter(h => h.trim()).map(h => `<th>${h.trim()}</th>`).join('');
        const rowsHtml = rows.trim().split('\n').map(row => {
            const cells = row.split('|').filter(c => c.trim()).map(c => `<td>${c.trim()}</td>`).join('');
            return `<tr>${cells}</tr>`;
        }).join('');
        return `<table><thead><tr>${headers}</tr></thead><tbody>${rowsHtml}</tbody></table>`;
    });

    // Paragraphs
    html = html.split('\n\n').map(para => {
        para = para.trim();
        if (!para) return '';
        if (para.startsWith('<')) return para; // Already HTML
        return `<p>${para.replace(/\n/g, '<br>')}</p>`;
    }).join('\n');

    return html;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

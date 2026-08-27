"""Pure functions for discovering and parsing agents and skills from the workspace."""

from pathlib import Path
from typing import Final, Mapping, Optional, Sequence
import yaml

from agent_server.config import AGENTS_DIR, SKILLS_DIR
from agent_server.types import AgentMeta, SkillMeta


# ---------------------------------------------------------------------------
# Pure Helper Functions for Markdown & Frontmatter Parsing
# ---------------------------------------------------------------------------

def extract_frontmatter_and_body(content: str) -> tuple[dict, str]:
    """Pure function to extract YAML frontmatter and markdown body from string."""
    if not content.startswith("---"):
        return {}, content.strip()

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content.strip()

    raw_yaml, body = parts[1], parts[2]
    try:
        data = yaml.safe_load(raw_yaml) or {}
        return data, body.strip()
    except Exception:
        return {}, body.strip()


def parse_agent_file(file_path: Path) -> Optional[AgentMeta]:
    """Pure function: reads and parses a single agent markdown file."""
    if not file_path.is_file() or file_path.suffix != ".md":
        return None

    try:
        content = file_path.read_text(encoding="utf-8")
        frontmatter, body = extract_frontmatter_and_body(content)
        name = frontmatter.get("name") or file_path.stem
        description = frontmatter.get("description") or f"Agent {name}"
        instructions = body if body else content

        return AgentMeta(
            name=name,
            description=description,
            system_instructions=instructions,
            file_path=str(file_path.resolve()),
        )
    except Exception:
        return None


def parse_skill_directory(skill_dir: Path) -> Optional[SkillMeta]:
    """Pure function: reads and parses a skill directory containing SKILL.md."""
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return None

    try:
        content = skill_file.read_text(encoding="utf-8")
        frontmatter, _ = extract_frontmatter_and_body(content)
        name = frontmatter.get("name") or skill_dir.name
        description = frontmatter.get("description") or f"Skill {name}"

        return SkillMeta(
            name=name,
            description=description,
            directory_path=str(skill_dir.resolve()),
        )
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Discovery Pipelines
# ---------------------------------------------------------------------------

def scan_all_agents(agents_dir: Path = AGENTS_DIR) -> tuple[AgentMeta, ...]:
    """Scans the agents directory and returns an immutable tuple of AgentMeta."""
    if not agents_dir.is_dir():
        return ()

    agents = [
        agent
        for file in sorted(agents_dir.glob("*.md"))
        if (agent := parse_agent_file(file)) is not None
    ]
    return tuple(agents)


def scan_all_skills(skills_dir: Path = SKILLS_DIR) -> tuple[SkillMeta, ...]:
    """Scans the skills directory and returns an immutable tuple of SkillMeta."""
    if not skills_dir.is_dir():
        return ()

    skills = [
        skill
        for sub_dir in sorted(skills_dir.iterdir())
        if sub_dir.is_dir() and (skill := parse_skill_directory(sub_dir)) is not None
    ]
    return tuple(skills)


def get_skills_paths(skills_dir: Path = SKILLS_DIR) -> list[str]:
    """Returns the list of string paths suitable for LocalAgentConfig.skills_paths."""
    if not skills_dir.is_dir():
        return []
    return [str(skills_dir.resolve())]


def find_agent_by_name(
    agents: Sequence[AgentMeta], target_name: str
) -> Optional[AgentMeta]:
    """Pure lookup function for finding an agent by name."""
    for agent in agents:
        if agent.name == target_name:
            return agent
    return None

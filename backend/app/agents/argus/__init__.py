"""
agents/argus — GitHub verification agent.

Argus scans a GitHub repository for evidence of work:
commits, files changed, and pull requests merged.

Input:  { repo, milestone }
Output: { evidence_found, commits, files_changed }
"""

from app.agents.argus.agent import ArgusAgent, ArgusInput, ArgusOutput

__all__ = ["ArgusAgent", "ArgusInput", "ArgusOutput"]

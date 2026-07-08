"""
Tools the chat agent can call.

Built per-request via ``build_tools(client)`` so each tool closes over an
``NGS360Client`` carrying the current user's token — that threads the caller's
identity into every REST lookup without global state.

The ``navigate`` tool's side effect (redirecting the browser) is performed by
the frontend, which consumes a ``data-navigate`` SSE part emitted by the
streamer in ``services.py``; the returned string is only what the model sees.
"""

from typing import Any

from langchain_core.tools import tool

from ngs360_client import NGS360Client

NAVIGABLE_TYPES = ("project", "run", "job")


def build_tools(client: NGS360Client) -> list[Any]:
    @tool
    def navigate(destination: str, id: str) -> str:
        """Take the user to an entity's detail page in NGS360.

        Call this when the user asks to open, go to, or view a specific
        project, run, or job.

        Args:
            destination: One of "project", "run", or "job".
            id: The entity id, e.g. "P-20260507-0008".
        """
        if destination not in NAVIGABLE_TYPES:
            return (
                f"Cannot navigate to '{destination}'. "
                f"Valid destinations are: {', '.join(NAVIGABLE_TYPES)}."
            )
        return f"Navigating to {destination} {id}."

    @tool
    async def lookup_project(project_id: str) -> str:
        """Look up summary information about a project by its id.

        Call this when the user asks about a specific project's status,
        samples, or runs and you need real data to answer.

        Args:
            project_id: The project id, e.g. "P-20260507-0008".
        """
        try:
            data = await client.get_project(project_id)
        except Exception as exc:  # noqa: BLE001 - surface any lookup failure to the model
            return f"Could not fetch project {project_id}: {exc}"
        return f"Project {project_id}: {data}"

    return [navigate, lookup_project]

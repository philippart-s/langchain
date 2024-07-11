from dataclasses import dataclass
from typing import Iterable, List, Literal, Union

from langchain_core.documents import Document


@dataclass(frozen=True)
class GraphStoreLink:
    """A link to/from a tag of a given tag.

    Edges exist from nodes with an outgoing link to nodes with a matching incoming link.
    """

    kind: str
    """The kind of link. Allows different extractors to use the same tag name without 
    creating collisions between extractors. For example “keyword” vs “url”."""
    direction: Literal["in", "out", "bidir"]
    """The direction of the link."""
    tag: str
    """The tag of the link."""

    @staticmethod
    def incoming(kind: str, tag: str) -> "GraphStoreLink":
        """Create an incoming link."""
        return GraphStoreLink(kind=kind, direction="in", tag=tag)

    @staticmethod
    def outgoing(kind: str, tag: str) -> "GraphStoreLink":
        """Create an outgoing link."""
        return GraphStoreLink(kind=kind, direction="out", tag=tag)

    @staticmethod
    def bidir(kind: str, tag: str) -> "GraphStoreLink":
        """Create a bidirectional link."""
        return GraphStoreLink(kind=kind, direction="bidir", tag=tag)


Link = GraphStoreLink  # Alias for backwards compatibility

METADATA_LINKS_KEY = "links"


def get_links(doc: Document) -> List[GraphStoreLink]:
    """Get the links from a document.

    Args:
        doc: The document to get the link tags from.

    Returns:
        The set of link tags from the document.
    """

    links = doc.metadata.setdefault(METADATA_LINKS_KEY, [])
    if not isinstance(links, list):
        # Convert to a list and remember that.
        links = list(links)
        doc.metadata[METADATA_LINKS_KEY] = links
    return links


def add_links(
    doc: Document, *links: Union[GraphStoreLink, Iterable[GraphStoreLink]]
) -> None:
    """Add links to the given metadata.

    Args:
        doc: The document to add the links to.
        *links: The links to add to the document.
    """
    links_in_metadata = get_links(doc)
    for link in links:
        if isinstance(link, Iterable):
            links_in_metadata.extend(link)
        else:
            links_in_metadata.append(link)

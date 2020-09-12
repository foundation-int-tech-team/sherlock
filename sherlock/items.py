from dataclasses import dataclass, field

from typing import List


@dataclass
class MemberItem:
    branch_id: str = field(default=None)
    user_id: str = field(default=None)
    slug: str = field(default=None)
    username: str = field(default=None)
    member_since: str = field(default=None)


@dataclass
class PageItem:
    page_id: str = field(default=None)
    branch_id: str = field(default=None)
    title: str = field(default=None)
    preview: str = field(default=None)
    slug: str = field(default=None)
    tags: List[str] = field(default_factory=list)
    created_by: str = field(default=None)
    created_at: str = field(default=None)
    updated_at: str = field(default=None)


@dataclass
class TitleItem:
    subtitle: str = field(default=None)
    slug: str = field(default=None)
    branch_id: str = field(default=None)


@dataclass
class VoteItem:
    user_id: str = field(default=None)
    page_id: str = field(default=None)
    vote: int = field(default=None)

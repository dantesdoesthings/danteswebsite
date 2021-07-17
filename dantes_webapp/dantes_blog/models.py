import typing


class BlogPost:
    author: str
    title: str
    slug: str
    body: str
    posted: str
    tags: typing.List[str]


class Tag:
    slug: str

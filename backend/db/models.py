from sqlmodel import SQLModel, Field, create_engine, Relationship, Column, JSON
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone


# ---------- User ----------
class UserProfile(SQLModel, table=True):
    __tablename__ = "userprofile"

    user_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., description="Full name of the user")

    # JSON columns for flexible data
    experience: Dict[str, str] = Field(
        sa_column=Column(JSON), default_factory=dict,
        description="Work experience of the user"
    )
    skills: List[str] = Field(
        sa_column=Column(JSON), default_factory=list,
        description="List of Skills of the user"
    )
    raw: Dict[str, Any] = Field(
        sa_column=Column(JSON), default_factory=dict,
        description="Raw LinkedIn payload"
    )

    posts: List["Post"] = Relationship(back_populates="author")


# ---------- Post ----------
class Post(SQLModel, table=True):
    __tablename__ = "post"

    post_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="userprofile.user_id", nullable=False)
    content: str = Field(..., description="Content of the post")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    scheduled_for: Optional[datetime] = Field(default=None)

    # JSON for multiple timestamps & metadata
    updated_at: List[datetime] = Field(
        sa_column=Column(JSON), default_factory=list[lambda: datetime.now(timezone.utc)],
        description="Timestamps when the post was last updated"
    )

    author: Optional[UserProfile] = Relationship(back_populates="posts")
    comments: List["Comment"] = Relationship(back_populates="post")


# ---------- Recursive Comment ----------
class Comment(SQLModel, table=True):
    __tablename__ = "comment"

    comment_id: Optional[int] = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="post.post_id", nullable=False)
    user_id: int = Field(foreign_key="userprofile.user_id", nullable=False)

    parent_id: Optional[int] = Field(
        default=None,
        foreign_key="comment.comment_id",
        description="Parent comment ID if this is a reply"
    )

    body: str = Field(..., description="Comment text")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # relationships
    post: Optional[Post] = Relationship(back_populates="comments")
    author: Optional[UserProfile] = Relationship()
    parent: Optional["Comment"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "Comment.comment_id"}
    )
    children: List["Comment"] = Relationship(back_populates="parent")


# ---------- Engine ----------
sqlite_file_name = "linkedin_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)


# SQLModel.metadata.create_all(engine)
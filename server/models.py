"""Module for defining the database models."""

from sqlalchemy import Column, DateTime, func

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class TimestampMixin:
    """Mixin for adding created_at and updated_at timestamps to a model."""

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    
class User(Base, TimestampMixin):
    """Model for a user."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)


class Song(Base, TimestampMixin):
    """Model for a song to convert to a playlist."""

    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, max_length=100, nullable=False)
    artist = Column(String, max_length=100, nullable=False)
    lyrics = Column(String, nullable=False)
    genius_id = Column(String, nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    playlist_id = Column(Integer, ForeignKey("playlist.id"))

    user = relationship("User", backref="songs", lazy="joined")
    category = relationship("Playlist", backref="songs", lazy="joined")


class Playlist(Base, TimestampMixin):
    """Model for an item in the inventory."""

    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class PlaylistSong(Base):
    """Model for the relationship between a playlist and a song."""

    __tablename__ = "playlist_songs"

    id = Column(Integer, primary_key=True, index=True)
    
    playlist_id = Column(Integer, ForeignKey("playlists.id"))
    spotify_id = Column(Integer, ForeignKey("songs.id))

    playlist = relationship("Playlist", backref="playlist_song", lazy="joined")

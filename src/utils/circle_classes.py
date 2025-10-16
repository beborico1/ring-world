from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict
import math
from ..utils.settings import CIRCLE_MEDIUM_RADIUS, GREY


@dataclass(eq=True, frozen=True)
class CircleIdentity:
    """Immutable identity for circles that can be used as dictionary keys"""

    id: int

    def __hash__(self):
        return hash(self.id)


@dataclass
class SmallCircle:
    """Small circle with game-specific functionality"""

    id: int
    pos: List[float]
    color: Tuple[int, int, int] = field(default_factory=lambda: GREY)
    previous_color: Optional[Tuple[int, int, int]] = field(default=None)
    time_to_untoggle: Optional[float] = field(default=None)
    identity: CircleIdentity = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "identity", CircleIdentity(self.id))
        if isinstance(self.pos, tuple):
            self.pos = list(self.pos)  # Convert tuple to list if needed

    def __hash__(self):
        return hash(self.identity)

    def __eq__(self, other):
        if not isinstance(other, SmallCircle):
            return False
        return self.identity == other.identity

    def set_color(self, color):
        self.color = color

    def __repr__(self):
        return f"Circle({self.id}, {self.color})"


@dataclass
class MediumCircle:
    """medium circle with animation and game functionality"""

    id: int
    pos: List[float]
    small_circles: List[SmallCircle] = field(default_factory=list)
    angle: float = field(default=0.0)
    color: Tuple[int, int, int] = field(default_factory=lambda: GREY)
    is_animating: bool = field(default=False)
    animation_start: float = field(default=0.0)
    target_rotation: float = field(default=0.0)
    initial_angles: Dict = field(default_factory=dict)
    identity: CircleIdentity = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "identity", CircleIdentity(self.id))
        if isinstance(self.pos, tuple):
            self.pos = list(self.pos)

    def __hash__(self):
        return hash(self.identity)

    def __eq__(self, other):
        if not isinstance(other, MediumCircle):
            return False
        return self.identity == other.identity


@dataclass
class LargeCircle:
    """Large circle containing medium circles"""

    id: int
    pos: List[float]
    medium_circles: List[MediumCircle] = field(default_factory=list)
    color: Tuple[int, int, int] = field(default_factory=lambda: GREY)  # Changed from color
    is_animating: bool = field(default=False)
    animation_start: float = field(default=0.0)
    target_rotation: float = field(default=0.0)
    initial_angles: Dict = field(default_factory=dict)
    identity: CircleIdentity = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "identity", CircleIdentity(self.id))
        if isinstance(self.pos, tuple):
            self.pos = list(self.pos)

    def __hash__(self):
        return hash(self.identity)

    def __eq__(self, other):
        if not isinstance(other, LargeCircle):
            return False
        return self.identity == other.identity

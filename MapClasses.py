from dataclasses import dataclass, field

@dataclass
class Map:
    entities: list[Entity] = field(default_factory=list)

@dataclass
class Entity:
    keyPairs: dict[str, str] = field(default_factory=dict)
    brushes: list[Brush] = field(default_factory=list)

@dataclass
class Brush:
    faces: list[Face] = field(default_factory=list)

@dataclass
class Plane:
    points: list[tuple] = field(default_factory=list)
    normal: tuple = field(default_factory=tuple)
    distance: tuple = field(default_factory=tuple)

@dataclass
class Face:
    vertex: list[tuple] = field(default_factory=list)
    tri: list[tuple] = field(default_factory=list)
    texture: str = ""
    u: tuple = field(default_factory=tuple)
    v: tuple = field(default_factory=tuple)
    uv_scale: tuple = field(default_factory=tuple)
    plane: Plane = field(default_factory=Plane)
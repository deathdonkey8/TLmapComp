
# TriLoxo Map Compiler

A command-line tool for converting Valve-standard `.MAP` files into a packaged archive containing compiled mesh data, entities, and supporting assets in JSON format.

---

## Features

- Converts classic Valve `.MAP` level files
- Extracts:
  - Brush geometry
  - Mesh data
  - Entities
  - Materials / texture references
- Outputs structured JSON for engine/runtime use
- Packages all generated data into a distributable archive
- Lightweight CLI workflow
- Engine-agnostic output format

---

## Overview

TriLoxo Map Compiler is designed to bridge traditional brush-based level design workflows with modern custom engines and tooling.

The compiler reads a Valve `.MAP` file and transforms the level into:
- optimized mesh data
- parsed entity information
- serialized JSON assets
- packaged runtime resources

This allows maps created in editors such as:
- Valve Hammer Editor
- Jackhammer
- TrenchBroom (Valve format)

to be used directly inside custom rendering or gameplay pipelines.

---

# Installation

## Requirements

- Node.js 18+ *(if applicable)*
- C++20 compiler *(if applicable)*
- Windows / Linux

## Clone Repository

```bash
git clone https://github.com/deathdonkey8/TLmapComp.git
cd TLmapComp
```

## Build

### Example (CMake)

```bash
mkdir build
cd build
cmake ..
cmake --build .
```

### Example (Node.js)

```bash
npm install
```

---

# Usage   *this needs changing

## Basic Command

```bash
TLmapComp mymap.map
```

## Specify Output

```bash
TLmapComp mymap.map -o compiled/
```

## Package Archive

```bash
TLmapComp mymap.map --archive level.tlx
```

---

# Output Structure

Example generated archive contents:

```text
level.tlx
├── meshes/
│   ├── worldspawn.json
│   ├── props.json
│   └── collision.json
├── entities.json
├── materials.json
├── metadata.json
└── manifest.json
```

---

# JSON Format

## Entity Example

```json
{
  "classname": "light",
  "origin": [128, 64, 256],
  "intensity": 400
}
```

## Mesh Example

```json
{
  "vertices": [...],
  "indices": [...],
  "material": "brick/wall01"
}
```

---

# Supported MAP Features

| Feature | Status |
|---|---|
| Convex brushes | ✅ |
| Entities | ✅ |
| Texture alignment | ✅ |
| Material references | ✅ |
| Multiple worlds | 🚧 |
| Displacements | 🚧 |
| Curved surfaces | ❌ |

---

# CLI Options

| Option | Description |
|---|---|
| `-o, --output` | Output directory |
| `--archive` | Create packaged archive |
| `--pretty-json` | Pretty-print generated JSON |
| `--no-materials` | Skip material extraction |
| `--verbose` | Verbose logging |

---

# Example Workflow

1. Create a level in Hammer Editor
2. Export/save as `.MAP`
3. Run TriLoxo Map Compiler
4. Import generated archive into your engine/runtime

```bash
triloxo-compiler test.map --archive test.tlx
```

---

# Goals

TriLoxo Map Compiler aims to:
- simplify level conversion pipelines
- preserve classic brush mapping workflows
- provide engine-friendly structured data
- support moddable/custom engines

---

# Roadmap

- BSP support
- Geometry optimization
- Collision mesh generation
- Lightmap baking support
- Incremental compilation
- Plugin system
- glTF export

---

# Contributing

Contributions are welcome.

If you'd like to improve the compiler:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

# License

MIT License

---

# Credits

Inspired by classic Valve mapping workflows and modern engine tooling pipelines.

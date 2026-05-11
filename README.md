
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

 
## Installation
 
### Requirements
 
- Python 3.x
- Windows / Linux
  
### Clone Repository
 
```bash
git clone https://github.com/deathdonkey8/TLmapComp.git
cd TLmapComp
```
 
### Install Dependencies
 
```bash
pip install -r requirements.txt
```
 
### Build Executable
 
```bash
py -m PyInstaller --onefile --name=TLMC main.py
```
 
The compiled executable will be output to `dist/TLMC.exe`.
 

---
 
## Usage
 
### Python
 
```bash
python main.py --map {Map File} --tex {Texture directory} --out {Output directory}
```
 
### Executable
 
```bash
TLMC.exe --map {Map File} --tex {Texture directory} --out {Output directory}
```
 
### TrenchBroom Compile Profile
 
Add a **Run Tool** task in TrenchBroom's compile dialog:
 
- **Tool Path:** `{path to TLMC.exe}`
- **Parameters:** `--map ${MAP_FULL_NAME} --tex {Texture directory} --out {Output directory}`

---

# Output Structure

Example generated archive contents:

```text
level.geb
├── sounds/
│   └── drip.mp3
├── level.json
└── atlas.png
```

---

# JSON Format

## Entity Example

```json
{
  "classname": "light",
  "origin": "128, 64, 256",
  "intensity": "400"
}
```

## Mesh Example

```json
{
  "vertices": [...],
  "triangles": [...],
  "material": "blocks.png"
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
| Displacements | ❌ |
| Curved surfaces | ❌ |

---

# CLI Options

| Option | Description | Required |
|---|---|---|
| `--map` | Map file | ✅ |
| `--out` | Output directory | ✅ |
| `--tex` | Texture directory | ✅ |
| `--sound` | Sound folder - for baked level sound | ❌ |

---

# Example Workflow

1. Create a level in Hammer Editor
2. Export/save as `.MAP`
3. Run TriLoxo Map Compiler
4. Import generated archive into your engine/runtime

EXE
```bash
TLMC.exe --map ~/Documents/test.map --tex ~/Documents/textures --out ~/Documents
```

Python
```bash
Python main.py --map ~/Documents/test.map --tex ~/Documents/textures --out ~/Documents
```

---

# Goals

TriLoxo Map Compiler aims to:
- simplify level conversion pipelines
- preserve classic brush mapping workflows
- provide engine-friendly structured data
- support moddable/custom engines

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

.MAP files - file format description, algorithms, and code By Stefan Hajnoczi

# CAD of Choice

## Problem

- eagle has only simplified constraints management (important for proper ERC, DRC)
- no user moderated part properties (Accuracy, max Power, max Gate Voltage ...)
- no proper BOM management (in Altium one component equals one real / orderable part)
- constraint from kai: linux-support very much preferred

## Eagle

- pro: holds current design, probably good enough
- con: not free for everyone, has no proper constraints and parameter handling (part properties, order number, bom generation)

## kiCAD

- pro: open source, can import eagle, several extensions
- con: still no proper constraints in V5, less intuitive GUI
- detour: skidl_

## Skidl

- pro: offers a schematic design language in python -> jump right to kiCAD PCB Layout, seems to support user moderated properties, has constraints
- con: v0.2 - but it seems to be usable, documentation is loose
- <https://xesscorp.github.io/skidl/docs/_site/index.html>

## Altium

- pro: tool of choice, free license with university-email, proper constraints and parameter manager, simulation
- con: most functionality is overkill, windows-os only

## Circuit Maker

- pro: free, directly for open source projects, similar to big Altium brother
- con: deliberately crippled to be unproductive for large designs

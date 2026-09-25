# AddModifierTools
![image](https://raw.githubusercontent.com/ghostendsky/AddModifierTools/master/screenshots/AddModifierTools.png)

**Currently add modifier list only supports mesh**

Blender minimal version : 5.2 (packaged as a Blender extension)

# Main features:
- Add modifiers for multiple objects
- Apply all modifiers for multiple objects
- Delete all modifiers for multiple objects
- Expand/Collapse modifiers for multiple objects

# Install
1. Download or build `add_modifier_tools-<version>.zip` (see below).
2. In Blender, open **Edit > Preferences > Get Extensions**, click the dropdown at the top right and choose **Install from Disk...**, then pick the zip.
   You can also drag and drop the zip into the Blender window.

# Build the extension zip
The extension metadata lives in `blender_manifest.toml`. Build with Blender's own command line tool from the repository root:

```sh
blender --command extension validate
blender --command extension build --output-dir dist
```

This writes `dist/add_modifier_tools-<version>.zip`. Files listed in `paths_exclude_pattern` in the manifest (screenshots, git files, `__pycache__`) are left out of the zip.

When releasing a new version, bump `version` in `blender_manifest.toml` (and `bl_info` in `__init__.py` to match).

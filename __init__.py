# SPDX-License-Identifier: MIT
# Copyright (c) 2023 ghostendsky
# See the LICENSE file for the full license text.

# bl_info is only read when installed as a legacy add-on;
# Blender 4.2+ extensions use blender_manifest.toml instead.
bl_info = {
    "name" : "Add Modifier Tools",
    "author" : "GhostEndSky",
    "description" : "Modifier Tools",
    "blender" : (5, 2, 0),
    "version" : (0, 1, 0),
    "location" : "Properties > Modifiers",
    "warning" : "",
    "category" : "Interface"
}

# standard modules
import os

# blender modules
import bpy

# local module
from . import ui as AMT_UI
from . import operators as AMT_OT


def register():
    AMT_OT.register()
    AMT_UI.register()

def unregister():
    AMT_OT.unregister()
    AMT_UI.unregister()

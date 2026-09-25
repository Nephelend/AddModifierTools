# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

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

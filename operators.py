# Blender modules
import bpy
from bpy.types import Operator
from bpy.props import (IntProperty,
                       BoolProperty,
                       EnumProperty,
                       StringProperty,
                       CollectionProperty)


# ANCHOR Function - Get selected objects
def get_selected_objects():
    """ Get selected objects name to list """
    obj_list = []
    sel_obj = bpy.context.selected_objects
    for i in sel_obj:
        obj_list.append(i.name)
    return obj_list


# ANCHOR Function - Add modifier for object
def add_modifer_for_object(obj="", mod=""):
    """ Add modifier for object """
    if obj:
        obj_data = bpy.data.objects[obj]
        if mod:
            obj_data.modifiers.new("", mod)


# ANCHOR Function - Check mode for object
def check_mode_for_object(obj=""):
    """ Check mode for object """
    if obj:
        obj_data = bpy.data.objects[obj]
        mode = obj_data.mode
        if mode == "EDIT":
            return False
        elif mode == "OBJECT":
            return True


# ANCHOR Function - Apply modifier for object
def apply_modifiers_for_object(obj=""):
    """ Apply modifiers for object, return a list of (modifier name, error) that failed """
    failed = []
    if obj:
        obj_data = bpy.data.objects[obj]

        # Copy the names first, applying a modifier removes it from the stack
        mod_names = [mod.name for mod in obj_data.modifiers]
        with bpy.context.temp_override(object=obj_data, active_object=obj_data):
            for mod_name in mod_names:
                try:
                    bpy.ops.object.modifier_apply(modifier=mod_name)
                except RuntimeError as err:
                    failed.append((mod_name, str(err).strip()))
    return failed


# ANCHOR Function - Delete modifier for object
def delete_modifiers_for_object(obj=""):
    """ Delete modifier for object """
    if obj:
        obj_data = bpy.data.objects[obj]
        obj_data.modifiers.clear()


# ANCHOR Function - Set expand collapse modifiers
def set_expand_collapse_modifiers(obj=""):
    """ Set expand collapse modifiers """
    if obj:
        obj_data = bpy.data.objects[obj]
        vs = 0
        for mod in obj_data.modifiers:
            if (mod.show_expanded):
                vs += 1
            else:
                vs -= 1
        is_colse = False
        if (0 < vs):
            is_colse = True
        for mod in obj_data.modifiers:
            mod.show_expanded = not is_colse


# ANCHOR Function - Get modifier icon
def get_modifier_icon_dict():
    """ Get modifier icon dict """
    return {m.identifier : m.icon for m in bpy.types.Modifier.bl_rna.properties["type"].enum_items}


# ANCHOR Function - Get modifier layout
# Categories follow Blender 5.2's Add Modifier menu
# (scripts/startup/bl_ui/properties_data_modifier.py), including the
# Grease Pencil modifiers that Blender lists inside each category.
ADD_MODIFIER_CATEGORIES = {
    "Edit": (
        "DATA_TRANSFER", "MESH_CACHE", "MESH_SEQUENCE_CACHE", "UV_PROJECT",
        "UV_WARP", "VERTEX_WEIGHT_EDIT", "VERTEX_WEIGHT_MIX",
        "VERTEX_WEIGHT_PROXIMITY",
        "GREASE_PENCIL_TEXTURE", "GREASE_PENCIL_TIME",
        "GREASE_PENCIL_VERTEX_WEIGHT_PROXIMITY",
        "GREASE_PENCIL_VERTEX_WEIGHT_ANGLE",
    ),
    "Generate": (
        "ARRAY", "BEVEL", "BOOLEAN", "BUILD", "DECIMATE", "EDGE_SPLIT",
        "NODES", "MASK", "MIRROR", "MESH_TO_VOLUME", "MULTIRES", "REMESH",
        "SCREW", "SKIN", "SOLIDIFY", "SUBSURF", "TRIANGULATE",
        "VOLUME_TO_MESH", "WELD", "WIREFRAME",
        "GREASE_PENCIL_ARRAY", "GREASE_PENCIL_BUILD", "GREASE_PENCIL_DASH",
        "GREASE_PENCIL_ENVELOPE", "GREASE_PENCIL_LENGTH", "LINEART",
        "GREASE_PENCIL_MIRROR", "GREASE_PENCIL_MULTIPLY",
        "GREASE_PENCIL_OUTLINE", "GREASE_PENCIL_SIMPLIFY",
        "GREASE_PENCIL_SUBDIV",
    ),
    "Deform": (
        "ARMATURE", "CAST", "CURVE", "DISPLACE", "HOOK", "LAPLACIANDEFORM",
        "LATTICE", "MESH_DEFORM", "SHRINKWRAP", "SIMPLE_DEFORM", "SMOOTH",
        "CORRECTIVE_SMOOTH", "LAPLACIANSMOOTH", "SURFACE_DEFORM", "WARP",
        "WAVE", "VOLUME_DISPLACE",
        "GREASE_PENCIL_ARMATURE", "GREASE_PENCIL_HOOK",
        "GREASE_PENCIL_LATTICE", "GREASE_PENCIL_NOISE",
        "GREASE_PENCIL_OFFSET", "GREASE_PENCIL_SHRINKWRAP",
        "GREASE_PENCIL_SMOOTH", "GREASE_PENCIL_THICKNESS",
    ),
    "Normals": (
        "NORMAL_EDIT", "WEIGHTED_NORMAL",
    ),
    "Physics": (
        "CLOTH", "COLLISION", "DYNAMIC_PAINT", "EXPLODE", "FLUID", "OCEAN",
        "PARTICLE_INSTANCE", "PARTICLE_SYSTEM", "SOFT_BODY",
    ),
    "Color": (
        "GREASE_PENCIL_COLOR", "GREASE_PENCIL_OPACITY", "GREASE_PENCIL_TINT",
    ),
}

# Internal types that Blender never offers in its Add Modifier menu
HIDDEN_MODIFIER_TYPES = {"SURFACE"}


def get_add_modifiers_layout():
    """ Get add modifier layout dict """
    op = bpy.ops.object.modifier_add
    rna_enum = op.get_rna_type().properties["type"].enum_items
    available = {mod.identifier: mod for mod in rna_enum}

    mod_dict = {}
    for cat, mod_ids in ADD_MODIFIER_CATEGORIES.items():
        # Skip types this Blender build doesn't have
        mods = [(available[mod_id].identifier, available[mod_id].name, available[mod_id].icon)
                for mod_id in mod_ids if mod_id in available]
        if mods:
            mod_dict[cat] = mods

    # Keep types added in newer Blender versions reachable
    known = {mod_id for mod_ids in ADD_MODIFIER_CATEGORIES.values() for mod_id in mod_ids}
    other = [(mod.identifier, mod.name, mod.icon) for mod in rna_enum
             if mod.identifier not in known and mod.identifier not in HIDDEN_MODIFIER_TYPES]
    if other:
        mod_dict["Other"] = other
    return mod_dict


# ANCHOR Operator - apply all modifiers
class ADD_MODIFIER_TOOLS_OT_apply_all(Operator):
    """ Apply All Modifiers Operator """
    bl_idname  = "add_modifier_tools.apply_all_modifiers"
    bl_label   = "Apply All Modifiers"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):
        if (len(context.selected_objects) > 0):
            sel_objs = get_selected_objects()
            for obj in sel_objs:
                obj_mode = check_mode_for_object(obj)
                if not obj_mode:
                    self.report({"INFO"}, F"Modifiers cannot be applied in edit mode the {obj}.")
                    return {"CANCELLED"}
                else:
                    for mod_name, err in apply_modifiers_for_object(obj):
                        self.report({"WARNING"}, F"Failed to apply {mod_name} on {obj}: {err}")

        for area in context.screen.areas:
            area.tag_redraw()

        return {"FINISHED"}


# ANCHOR Operator - delete all modifiers
class ADD_MODIFIER_TOOLS_OT_delete_all(Operator):
    """ Delete All Modifiers Operator """
    bl_idname  = "add_modifier_tools.delete_all_modifiers"
    bl_label   = "Delete All Modifiers"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return bool(context.selected_objects)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if (len(context.selected_objects) > 0):
            sel_objs = get_selected_objects()
            for obj in sel_objs:
                try:
                    delete_modifiers_for_object(obj)
                except:
                    self.report({"INFO"}, "Failed to delete all modifiers.")

        for area in context.screen.areas:
            area.tag_redraw()

        return {"FINISHED"}


# ANCHOR Operator - expand/collapse modifiers
class ADD_MODIFIER_TOOLS_OT_expand_collapse(Operator):
    """ Expand/Collapse Modifiers Operator """
    bl_idname  = "add_modifier_tools.expand_collapse_modifiers"
    bl_label   = "Expand/Collapse Modifiers"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if (len(context.selected_objects) > 0):
            sel_objs = get_selected_objects()
            for obj in sel_objs:
                set_expand_collapse_modifiers(obj)
        else:
            self.report({"INFO"}, "No modifiers to Expand/Collapse")
            return {"CANCELLED"}
        
        for area in context.screen.areas:
            area.tag_redraw()

        return {"FINISHED"}


# ANCHOR Operator - multiple additional
class ADD_MODIFIER_TOOLS_OT_multiple_additional(Operator):
    """ Add every modifier in the Modifier Tools list to all selected objects """
    bl_idname      = "add_modifier_tools.multiple_additional_modifiers"
    bl_label       = "Add List to Selected"
    bl_options     = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return bool(context.selected_objects)

    def execute(self, context):
        mod_list = []
        scn = context.scene
        mod = scn.amt_modifiers
        for i in mod.items():
            mod_list.append(i[1].mod_id)

        if (len(context.selected_objects) > 0):
            sel_objs = get_selected_objects()
            for mod in mod_list:
                for i in sel_objs:
                    add_modifer_for_object(i, mod)
        else:
            self.report({"INFO"}, "No selected to objects")
            return {"CANCELLED"}

        for area in context.screen.areas:
            area.tag_redraw()

        return {"FINISHED"}


# ANCHOR Operator - list action
class ADD_MODIFIER_TOOLS_OT_list_action(Operator):
    """ UI List actions Operator """
    bl_idname      = "add_modifier_tools.list_action"
    bl_label       = "List Actions"
    bl_options     = {'REGISTER'}

    action: EnumProperty(
        items=(
            ("UP"    , "Up"    , ""),
            ("DOWN"  , "Down"  , ""),
            ("REMOVE", "Remove", ""),
            ("ADD"   , "Add"   , "")
        )
    )

    @classmethod
    def description(cls, context, properties):
        return {
            "UP"    : "Move the modifier up in the list",
            "DOWN"  : "Move the modifier down in the list",
            "REMOVE": "Remove the modifier from the list",
            "ADD"   : "Queue a modifier in the list. "
                      "Use Add List to Selected to add the queued modifiers to the selected objects",
        }[properties.action]

    def invoke(self, context, event):
        scn = context.scene
        idx = scn.modifier_active_index

        try:
            mod = scn.amt_modifiers[idx]
        except IndexError:
            pass
        else:
            if self.action == "DOWN" and idx < len(scn.amt_modifiers) - 1:
                mod_next = scn.amt_modifiers[idx+1].name
                scn.amt_modifiers.move(idx, idx+1)
                scn.modifier_active_index += 1
            elif self.action == "UP" and idx >= 1:
                mod_prev = scn.amt_modifiers[idx-1].name
                scn.amt_modifiers.move(idx, idx-1)
                scn.modifier_active_index -= 1
            elif self.action == "REMOVE":
                scn.amt_modifiers.remove(idx)
                scn.modifier_active_index -= 1

        if self.action == "ADD":
            bpy.ops.wm.call_menu(name="ADD_MODIFIER_TOOLS_MT_add_modifier")

        return {"FINISHED"}


# ANCHOR Operator - menu action
class ADD_MODIFIER_TOOLS_OT_menu_action(Operator):
    """ Menu actions Operator """
    bl_idname      = "add_modifier_tools.menu_action"
    bl_label       = "Menu Actions"
    bl_options     = {"REGISTER"}

    mod_name: StringProperty()
    mod_id:   StringProperty()

    def execute(self, context):
        scn = context.scene
        item = scn.amt_modifiers.add()
        item.name = self.mod_name
        item.mod_id = self.mod_id
        scn.modifier_active_index = len(scn.amt_modifiers)-1

        for area in context.screen.areas:
            area.tag_redraw()

        return {"FINISHED"}


# ANCHOR Classes List
classes = (
    ADD_MODIFIER_TOOLS_OT_apply_all,
    ADD_MODIFIER_TOOLS_OT_delete_all,
    ADD_MODIFIER_TOOLS_OT_expand_collapse,
    ADD_MODIFIER_TOOLS_OT_multiple_additional,
    ADD_MODIFIER_TOOLS_OT_list_action,
    ADD_MODIFIER_TOOLS_OT_menu_action,
)


# ANCHOR Register
def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


# ANCHOR Unregister
def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)


if __name__ == "__main__":
    register()

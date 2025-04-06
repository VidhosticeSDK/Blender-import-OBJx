# SPDX-License-Identifier: GPL-2.0-or-later

bl_info = {
    "name": "OBJx Import",
    "author": "VidhosticeSDK, p2or, Tomoaki Osada, Campbell Barton, Bastien Montagne)",
    "version": (1, 0, 0),
    "blender": (2, 93, 0),
    "location": "File > Import-Export",
    "description": "Import OBJx, Import OBJ mesh, UVs, vertex colors, materials and textures",
    "warning": "",
    "tracker_url": "https://github.com/VidhosticeSDK/Blender-import-OBJx",
    "category": "Import-Export"}


if "bpy" in locals():
    import importlib
    if "import_objx" in locals():
        importlib.reload(import_objx)


import bpy
from bpy.props import (
    BoolProperty,
    FloatProperty,
    StringProperty,
    EnumProperty,
    CollectionProperty,
)
from bpy_extras.io_utils import (
    ImportHelper,
    orientation_helper,
    path_reference_mode,
    axis_conversion,
    poll_file_object_drop,
)


@orientation_helper(axis_forward='-Z', axis_up='Y')
class ImportOBJx(bpy.types.Operator, ImportHelper):
    """Load a Wavefront OBJx File"""
    bl_idname = "import_scene.objx"
    bl_label = "Import OBJx"
    bl_options = {'PRESET', 'UNDO'}

    directory: StringProperty()

    filename_ext = ".objx"
    filter_glob: StringProperty(
        default="*.objx;*.obj",
        options={'HIDDEN'},
    )

    files: CollectionProperty(
        name="File Path",
        type=bpy.types.OperatorFileListElement,
    )

    use_edges: BoolProperty(
        name="Lines",
        description="Import lines and faces with 2 verts as edge",
        default=True,
    )
    use_smooth_groups: BoolProperty(
        name="Smooth Groups",
        description="Surround smooth groups by sharp edges",
        default=True,
    )

    use_split_objects: BoolProperty(
        name="Object",
        description="Import OBJx Objects into Blender Objects",
        default=True,
    )
    use_split_groups: BoolProperty(
        name="Group",
        description="Import OBJx Groups into Blender Objects",
        default=False,
    )

    use_groups_as_vgroups: BoolProperty(
        name="Poly Groups",
        description="Import OBJx groups as vertex groups",
        default=False,
    )

    use_image_search: BoolProperty(
        name="Image Search",
        description="Search subdirs for any associated images "
        "(Warning, may be slow)",
        default=True,
    )

    split_mode: EnumProperty(
        name="Split",
        items=(
            ('ON', "Split", "Split geometry, omits vertices unused by edges or faces"),
            ('OFF', "Keep Vert Order", "Keep vertex order from file"),
        ),
    )

    global_clamp_size: FloatProperty(
        name="Clamp Size",
        description="Clamp bounds under this value (zero to disable)",
        min=0.0, max=1000.0,
        soft_min=0.0, soft_max=1000.0,
        default=0.0,
    )

    rotate_transform_apply: BoolProperty(
        name="Rotate transform apply",
        description="Apply rotation to zero",
        default=True,
    )

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        import_panel_include(layout, self)
        import_panel_transform(layout, self)
        import_panel_geometry(layout, self)

    def execute(self, context):
        # print("Selected: " + context.active_object.name)
        from . import import_objx
        import os

        if self.split_mode == 'OFF':
            self.use_split_objects = False
            self.use_split_groups = False
        else:
            self.use_groups_as_vgroups = False

        keywords = self.as_keywords(
            ignore=(
                "axis_forward",
                "axis_up",
                "filter_glob",
                "split_mode",
                "directory",
                "filepath",
                "files",
            ),
        )

        global_matrix = axis_conversion(
            from_forward=self.axis_forward,
            from_up=self.axis_up,
        ).to_4x4()
        keywords["global_matrix"] = global_matrix

        if bpy.data.is_saved and context.preferences.filepaths.use_relative_paths:
            keywords["relpath"] = os.path.dirname(bpy.data.filepath)

#        return import_objx.load(context, **keywords)

        if self.files:
            ret = {'CANCELLED'}
            dirname = os.path.dirname(self.filepath)
            for file in self.files:
                path = os.path.join(dirname, file.name)
                if import_objx.load(context, filepath=path, **keywords) == {'FINISHED'}:
                    ret = {'FINISHED'}
            return ret
        else:
            return import_objx.load(context, filepath=self.filepath, **keywords)

    def invoke(self, context, event):
        return self.invoke_popup(context)


def import_panel_include(layout, operator):
    header, body = layout.panel("OBJX_import_include", default_closed=False)
    header.label(text="Include")
    if body:
        body.prop(operator, "use_image_search")
        body.prop(operator, "use_smooth_groups")
        body.prop(operator, "use_edges")


def import_panel_transform(layout, operator):
    header, body = layout.panel("OBJX_import_transform", default_closed=False)
    header.label(text="Transform")
    if body:
        body.prop(operator, "global_clamp_size")
        body.prop(operator, "axis_forward")
        body.prop(operator, "axis_up")
        body.separator()
        body.prop(operator, "rotate_transform_apply")


def import_panel_geometry(layout, operator):
    header, body = layout.panel("OBJX_import_geometry", default_closed=False)
    header.label(text="Geometry")
    if body:
        body.row().prop(operator, "split_mode", expand=True)

        body.use_property_split = True
        body.use_property_decorate = False  # No animation.

        col = body.column()
        if operator.split_mode == 'ON':
            col.prop(operator, "use_split_objects", text="Split by Object")
            col.prop(operator, "use_split_groups", text="Split by Group")
        else:
            col.prop(operator, "use_groups_as_vgroups")


class IO_FH_objx(bpy.types.FileHandler):
    bl_idname = "IO_FH_objx"
    bl_label = "OBJX"
    bl_import_operator = "import_scene.objx"
    bl_file_extensions = ".objx"

    @classmethod
    def poll_drop(cls, context):
        return poll_file_object_drop(context)


def menu_func_import(self, context):
    self.layout.operator(ImportOBJx.bl_idname, text="OBJx [4xUV, VC, Mat] (.objx)")


classes = (
    ImportOBJx,
    IO_FH_objx,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

import bpy
import math

bl_info = {
    "name": "Simple Math Animation prototype",
    "author": "Velocirection (V-rex)",
    "version" : (0, 0, 0, 1),
    "blender" : (4, 0, 0),
    "location": "View3D - Properties",
    "description": "Can make simple cyclical animation based on the 3d cursor position and some parameters.",
    "warning": "",
    "wiki_url": "",
    "category": "animation"}

def sma_generate_animation(bias_x, bias_y, strength_x, strength_y, phase, home_frame, frames):
    prev_autokey_setting = bpy.context.scene.tool_settings.use_keyframe_insert_auto
    
    bpy.context.scene.tool_settings.use_keyframe_insert_auto = True
    center_x = bpy.data.scenes["Scene"].cursor.location[0]
    center_y = bpy.data.scenes["Scene"].cursor.location[1]
    center_z = bpy.data.scenes["Scene"].cursor.location[2]

    bpy.data.scenes["Scene"].frame_current=home_frame

    for i in range(frames*2):
        if i%1 == 0:
            bpy.data.scenes["Scene"].frame_current=i+home_frame
            bpy.ops.transform.translate(value=(0, 0, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, snap=False, snap_elements={'VERTEX'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False, alt_navigation=True)
        
    bpy.data.scenes["Scene"].frame_current=home_frame

    for i in range(frames*2):
        if i%1 == 0:
            bpy.data.scenes["Scene"].frame_current=i+home_frame
        pi = math.pi
        #phase = pi+2
        #bias_x = 1
        #bias_y = 4
        #strength_x = 1/20
        #strength_y = 1/20
        cosv = (math.cos(((((pi)/frames))*i)+phase)*strength_x)*bias_x
        sinv = (math.sin(((((pi)/frames))*i)+phase)*strength_y)*bias_y
        bpy.ops.transform.trackball(value=(cosv, sinv), 
                                    center_override=(center_x,center_y,center_z),
                                    mirror=False, snap=False)
    bpy.context.scene.tool_settings.use_keyframe_insert_auto = prev_autokey_setting

    


class sma_execute(bpy.types.Operator):
    bl_idname = "object.sma_execute"
    bl_label = "Simple Math Animation execute"
    bl_description = "Generate a simple math animation on the selected bones/objects"

    def execute(self, context):
        # Your operator logic here
        scene = context.scene
        sma_generate_animation(scene.sma_bias_x, 
                               scene.sma_bias_y, 
                               scene.sma_str_x, 
                               scene.sma_str_y, 
                               scene.sma_phase,
                               scene.sma_home_frame,
                               scene.sma_frames)
                               
        self.report({'INFO'}, f"Called \'sma_execute\'")
        return {'FINISHED'}

class PT_sma_panel(bpy.types.Panel):
    bl_idname = "PT_sma_panel"
    bl_label = "Simple Math Animation panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Vrextras'

    '''
        v0.1
    '''

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        
        layout.prop(data=scene, property='sma_bias_x', text='Bias X')
        layout.prop(data=scene, property='sma_bias_y', text='Bias Y')
        layout.prop(data=scene, property='sma_str_x', text='Strength X')
        layout.prop(data=scene, property='sma_str_y', text='Strength Y')
        layout.prop(data=scene, property='sma_phase', text='Phase')
        layout.prop(data=scene, property='sma_home_frame', text='Home Frame')
        layout.prop(data=scene, property='sma_frames', text='Frames')
        
        layout.separator()
        layout.operator('object.sma_execute', text='Execute')

def register():
    bpy.utils.register_class(sma_execute)
    bpy.utils.register_class(PT_sma_panel)
    bpy.types.Scene.sma_bias_x = bpy.props.FloatProperty(
        name="Bias X", 
        description='Multiplier of how strong the x axis is in the circular motion',
        default=1.0
    )
    bpy.types.Scene.sma_bias_y = bpy.props.FloatProperty(
        name="Bias Y", 
        description='Multiplier of how strong the y axis is in the circular motion',
        default=1.0
    )
    bpy.types.Scene.sma_str_x = bpy.props.FloatProperty(
        name="Strength X", 
        description='X strength of the circular motion',
        default=1/20
    )
    bpy.types.Scene.sma_str_y = bpy.props.FloatProperty(
        name="Strength Y", 
        description='Y strength of the circular motion',
        default=1/20
    )
    bpy.types.Scene.sma_phase = bpy.props.FloatProperty(
        name="Phase", 
        description='Phase offset of the motion',
        default=1.0
    )
    bpy.types.Scene.sma_home_frame = bpy.props.IntProperty(
        name="Home Frame", 
        description='Frame the animation will start on.',
        default=1000
    )
    bpy.types.Scene.sma_frames = bpy.props.IntProperty(
        name="Frames", 
        description='How many frames the animation will be (will be multiplied by two)',
        default=16
    )

def unregister():
    bpy.utils.unregister_class(sma_execute)
    bpy.utils.unregister_class(PT_sma_panel)
    del bpy.types.Scene.sma_bias_x
    del bpy.types.Scene.sma_bias_y
    del bpy.types.Scene.sma_str_x
    del bpy.types.Scene.sma_str_y
    del bpy.types.Scene.sma_phase
    del bpy.types.Scene.sma_home_frame
    del bpy.types.Scene.sma_frames

if __name__ == "__main__":
    register()
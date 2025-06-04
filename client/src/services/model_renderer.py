import numpy as np
from vispy import scene
from vispy.geometry import MeshData
from model_data import ModelData

class ModelRenderer:
    def __init__(self, canvas: scene.SceneCanvas, view: scene.widgets.ViewBox):
        self.canvas = canvas
        self.view = view
        self.drawing_object_refs = []
    
    def draw_model(self, model_data: ModelData, draw_plot_group=False, clear_view=True):
        if clear_view:
            self.clear_view()

        points = scene.visuals.Markers()
        points.set_data(model_data.points.T, face_color=(.1, .1, .1, .5), edge_width=0, size=0.5)
        self.view.add(points)
        self.drawing_object_refs.append(points)

        lines = model_data.get_lines()
        line = scene.visuals.Line(lines, color=(.1, .1, .1, .4), connect='segments', width=1)
        self.view.add(line)
        self.drawing_object_refs.append(line)

        if draw_plot_group:
            mesh_data = MeshData(vertices=model_data.plot_group_points.T, faces=model_data.plot_group_edges.T, vertex_colors=model_data.get_plot_group_colors())
            mesh_visual = scene.visuals.Mesh(meshdata=mesh_data, mode='triangles')
            self.view.add(mesh_visual)
            self.drawing_object_refs.append(mesh_visual)

            colormap = model_data.get_color_map()
            clim = (round(model_data.plot_group_c_min_max[0], 2), round(model_data.plot_group_c_min_max[1], 2))
            colorbar = scene.visuals.ColorBar(cmap=colormap, orientation='right',
                                            size=(280, 40), parent=self.view, clim=clim)
            colorbar.transform = scene.transforms.STTransform(translate=(580, 300))
            self.drawing_object_refs.append(colorbar)
        
        x_min, x_max = np.min(model_data.points[0, :]), np.max(model_data.points[0, :])
        y_min, y_max = np.min(model_data.points[1, :]), np.max(model_data.points[1, :])
        z_min, z_max = np.min(model_data.points[2, :]), np.max(model_data.points[2, :])
        self.view.camera.center = ((x_min+x_max)/2, (y_min+y_max)/2, (z_min+z_max)/2)
    
    def clear_view(self):
        for drawing_object in self.drawing_object_refs:
            drawing_object.parent = None
        self.drawing_object_refs.clear()
    
    def save_view(self, filepath: str):
        image_array = self.canvas.render()
        from PIL import Image
        image = Image.fromarray(image_array)
        image.save(filepath) 
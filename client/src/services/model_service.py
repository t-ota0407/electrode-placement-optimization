import json
from pathlib import Path
import numpy as np
from vispy.geometry import MeshData

import config as config
from tcpip_communication import TcpipCommunication
from model_data import ModelData
from custom_types.model_type import ModelType

class ModelService:
    def __init__(self, tcpip_communication: TcpipCommunication):
        self.tcpip_communication = tcpip_communication
        self.current_model = None

    def load_model(self, model_type: ModelType) -> ModelData:
        """モデルの読み込み"""
        if config.USE_CACHE:
            self.current_model = self._load_model_from_cache(model_type)
        else:
            self.current_model = self._load_model_from_server(model_type)
        return self.current_model

    def _load_model_from_cache(self, model_type: ModelType) -> ModelData:
        """キャッシュからモデルを読み込む"""
        cache_path = ModelType.to_initial_model_cache_path(model_type)
        with open(cache_path, 'r', encoding='utf-8') as file:
            cached_data = file.read()
        cached_data = json.loads(cached_data)
        return ModelData.from_json(cached_data)

    def _load_model_from_server(self, model_type: ModelType) -> ModelData:
        """サーバーからモデルを読み込む"""
        model_data_json = self.tcpip_communication.load_model(model_type)
        return ModelData.from_json(model_data_json)

    def draw_model(self, view, model_data: ModelData = None, draw_plot_group=False, clear_view=True):
        """モデルの描画"""
        if model_data is None:
            model_data = self.current_model
        if model_data is None:
            raise ValueError("No model data available for drawing")

        drawing_object_refs = []

        if clear_view:
            self._clear_view(view)

        # Draw points
        points = self._draw_points(view, model_data)
        drawing_object_refs.append(points)

        # Draw lines
        line = self._draw_lines(view, model_data)
        drawing_object_refs.append(line)

        # Draw plot group if requested
        if draw_plot_group:
            mesh_visual, colorbar = self._draw_plot_group(view, model_data)
            drawing_object_refs.extend([mesh_visual, colorbar])

        # Update camera position
        self._update_camera_position(view, model_data)

        return drawing_object_refs

    def _clear_view(self, view):
        """ビューのクリア"""
        for child in view.children:
            child.parent = None

    def _draw_points(self, view, model_data):
        """点の描画"""
        from vispy import scene
        points = scene.visuals.Markers()
        points.set_data(model_data.points.T, face_color=(.1, .1, .1, .5), edge_width=0, size=0.5)
        view.add(points)
        return points

    def _draw_lines(self, view, model_data):
        """線の描画"""
        from vispy import scene
        lines = model_data.get_lines()
        line = scene.visuals.Line(lines, color=(.1, .1, .1, .4), connect='segments', width=1)
        view.add(line)
        return line

    def _draw_plot_group(self, view, model_data):
        """プロットグループの描画"""
        from vispy import scene
        # Draw mesh
        mesh_data = MeshData(
            vertices=model_data.plot_group_points.T,
            faces=model_data.plot_group_edges.T,
            vertex_colors=model_data.get_plot_group_colors()
        )
        mesh_visual = scene.visuals.Mesh(meshdata=mesh_data, mode='triangles')
        view.add(mesh_visual)

        # Draw colorbar
        colormap = model_data.get_color_map()
        clim = (
            round(model_data.plot_group_c_min_max[0], 2),
            round(model_data.plot_group_c_min_max[1], 2)
        )
        colorbar = scene.visuals.ColorBar(
            cmap=colormap,
            orientation='right',
            size=(280, 40),
            parent=view,
            clim=clim
        )
        colorbar.transform = scene.transforms.STTransform(translate=(580, 300))

        return mesh_visual, colorbar

    def _update_camera_position(self, view, model_data):
        """カメラ位置の更新"""
        x_min, x_max = np.min(model_data.points[0, :]), np.max(model_data.points[0, :])
        y_min, y_max = np.min(model_data.points[1, :]), np.max(model_data.points[1, :])
        z_min, z_max = np.min(model_data.points[2, :]), np.max(model_data.points[2, :])
        view.camera.center = ((x_min+x_max)/2, (y_min+y_max)/2, (z_min+z_max)/2) 
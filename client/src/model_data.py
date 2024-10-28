import numpy as np
from vispy import color

from dataclasses import dataclass

@dataclass
class ModelData:

    def __init__(self, points: np.ndarray, edges: np.ndarray, plot_group_points: np.ndarray,
                 plot_group_edges: np.ndarray, plot_group_values: np.ndarray,
                 plot_group_c_min_max: np.ndarray, plot_group_color_bar: np.ndarray,
                 plot_group_color_bar_range: np.ndarray):
        self.points = points
        self.edges = edges
        self.plot_group_points = plot_group_points
        self.plot_group_edges = plot_group_edges
        self.plot_group_values = plot_group_values
        self.plot_group_c_min_max = plot_group_c_min_max
        self.plot_group_color_bar = plot_group_color_bar
        self.plot_group_color_bar_range = plot_group_color_bar_range
    
    def get_lines(self):
        lines = []
        for i in range(self.edges.shape[1]):
            start_idx = self.edges[0, i]
            end_idx = self.edges[1, i]
            line = np.vstack((self.points[:, start_idx], self.points[:, end_idx]))
            lines.append(line)
        lines = np.array(lines)
        return lines
    
    def get_plot_group_colors(self):
        colors = []
        for i in range(self.plot_group_values.shape[0]):
            value = self.plot_group_values[i]
            range_min = self.plot_group_color_bar_range[0]
            range_max = self.plot_group_color_bar_range[1]
            color_bar_length = self.plot_group_color_bar.shape[0]
            color_idx = int(color_bar_length * (value - range_min) / (range_max - range_min))
            color_idx = np.clip(color_idx, 0, color_bar_length - 1)
            color = self.plot_group_color_bar[color_idx, :]
            colors.append(color)
        colors = np.array(colors)
        return colors
    
    def get_color_map(self):
        length = self.plot_group_color_bar.shape[0]
        color_min = 0
        color_max = 1
        step = (color_max - color_min) / (length - 1)
        positions = [color_min + step * i for i in range(length)]
        color_map = color.Colormap(self.plot_group_color_bar, positions)
        return color_map

    @staticmethod
    def from_json(model_data_json: any):

        points = np.array(model_data_json[0][0]['p'], dtype=np.float32)
        edges = np.array(model_data_json[0][0]['t'], dtype=np.int32)

        plot_group_points = np.array(model_data_json[1][0]['p'], dtype=np.float32)
        plot_group_edges = np.array(model_data_json[1][0]['t'], dtype=np.int32)
        plot_group_values = np.array(model_data_json[1][0]['d'], dtype=np.float32)

        plot_group_c_min_max = np.array(model_data_json[1][0]['cminmax'])
        plot_group_color_bar = np.array(model_data_json[1][0]['colorbar'])
        plot_group_color_bar_range = np.array(model_data_json[1][0]['colorbar_range'])

        model_data = ModelData(points, edges, plot_group_points,
                               plot_group_edges, plot_group_values,
                               plot_group_c_min_max, plot_group_color_bar,
                               plot_group_color_bar_range)

        return model_data

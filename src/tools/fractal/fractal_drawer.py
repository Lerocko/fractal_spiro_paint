# =============================================================
# File: fractal_generator.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-12-24
# Refactored: 2025-12-26
# Description:
#     Fractal geometry generator.
#     Receives base points and a pattern (lists of floats),
#     generates fractal geometry, and returns new points.
#     No UI, no canvas, no shape metadata.
# =============================================================

import math
from typing import List, Tuple

Point = Tuple[float, float]
Polyline = List[Point]

class FractalGenerator:
    """
    Fractal geometry engine.

    Public API:
        - constructor(base_shapes_points, pattern_points)
        - generate(depth=1) -> List[List[float]]
    """

    def __init__(
        self,
        base_shapes_points: List[List[float]],
        pattern_points: List[float],
    ) -> None:
        """
        Args:
            base_shapes_points: List of point lists for each shape.
            pattern_points: List of points defining the pattern.
        """
        self.base_shapes_polylines: List[Polyline] = [
            self._points_to_polyline(pts) for pts in base_shapes_points
        ]
        self.unit_pattern: Polyline = self._normalize_pattern(
            self._points_to_polyline(pattern_points)
        )

    # =============================================================
    # Public API
    # =============================================================
    def generate(self, depth: int = 1) -> List[List[float]]:
        """
        Generates fractal points for all base shapes.

        Args:
            depth: Recursion depth.

        Returns:
            List of new point lists for each shape.
        """
        new_shapes_points: List[List[float]] = []

        for polyline in self.base_shapes_polylines:
            if len(polyline) < 2:
                continue  # ignore degenerate shapes

            fractal_polyline = self._apply_recursion(polyline, depth)
            new_shapes_points.append(self._polyline_to_points(fractal_polyline))

        return new_shapes_points

    # =============================================================
    # Core Fractal Logic
    # =============================================================
    def _apply_recursion(self, polyline: Polyline, depth: int) -> Polyline:
        if depth <= 0:
            return polyline

        new_polyline: Polyline = []

        for i in range(len(polyline) - 1):
            segment = (polyline[i], polyline[i + 1])
            transformed = self._apply_pattern_to_segment(segment)

            if i > 0:
                transformed = transformed[1:]  # avoid duplicated points

            new_polyline.extend(transformed)

        return self._apply_recursion(new_polyline, depth - 1)

    def _apply_pattern_to_segment(self, segment: Tuple[Point, Point]) -> Polyline:
        (x1, y1), (x2, y2) = segment
        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)

        if length == 0:
            return [segment[0], segment[1]]

        angle = math.atan2(dy, dx)
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        transformed: Polyline = []

        for px, py in self.unit_pattern:
            sx = px * length
            sy = py * length
            rx = sx * cos_a - sy * sin_a
            ry = sx * sin_a + sy * cos_a
            transformed.append((x1 + rx, y1 + ry))

        return transformed

    # =============================================================
    # Pattern Normalization
    # =============================================================
    def _normalize_pattern(self, pattern: Polyline) -> Polyline:
        if len(pattern) < 2:
            return pattern

        start, end = pattern[0], pattern[-1]
        dx, dy = end[0] - start[0], end[1] - start[1]
        length = math.hypot(dx, dy)

        if length == 0:
            return pattern

        angle = math.atan2(dy, dx)
        cos_a = math.cos(-angle)
        sin_a = math.sin(-angle)

        normalized: Polyline = []
        for x, y in pattern:
            tx, ty = x - start[0], y - start[1]
            rx = tx * cos_a - ty * sin_a
            ry = tx * sin_a + ty * cos_a
            normalized.append((rx / length, ry / length))

        return normalized

    # =============================================================
    # Utilities
    # =============================================================
    @staticmethod
    def _points_to_polyline(points: List[float]) -> Polyline:
        return [(points[i], points[i + 1]) for i in range(0, len(points), 2)]

    @staticmethod
    def _polyline_to_points(polyline: Polyline) -> List[float]:
        points: List[float] = []
        for x, y in polyline:
            points.extend([x, y])
        return points

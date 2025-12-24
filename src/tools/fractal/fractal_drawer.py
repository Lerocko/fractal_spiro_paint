# =============================================================
# File: fractal_generator.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-12-24
# Description:
#     Pure fractal geometry generator.
#     Receives base shapes and a pattern, generates fractal geometry,
#     and returns new shapes data. No UI, no canvas.
# =============================================================

import math
import logging
from typing import List, Dict, Any, Tuple

Point = Tuple[float, float]
Polyline = List[Point]

class FractalGenerator:
    """
    Fractal geometry engine.

    Public API:
        - constructor(selected_shapes, pattern)
        - generate(depth) -> List[Dict]
    """

    def __init__(
        self,
        selected_shapes: List[Dict[str, Any]],
        pattern_shape: Dict[str, Any],
    ) -> None:
        self.selected_shapes = selected_shapes
        self.raw_pattern: Polyline = self._points_to_polyline(pattern_shape["points"])
        self.unit_pattern: Polyline = self._normalize_pattern(self.raw_pattern)

    # =============================================================
    # Public API
    # =============================================================
    def generate(self, depth: int = 1) -> List[Dict[str, Any]]:
        """
        Generates fractal geometry for all selected shapes.

        Args:
            depth: Recursion depth.

        Returns:
            List of new shape dictionaries.
        """
        new_shapes: List[Dict[str, Any]] = []

        for shape in self.selected_shapes:
            base_polyline = self._points_to_polyline(shape["points"])
            fractal_polyline = self._apply_recursion(base_polyline, depth)

            new_shapes.append({
                "type": "polyline",
                "points": self._polyline_to_points(fractal_polyline),
                "meta": {
                    "generated_by": "fractal",
                    "depth": depth,
                },
            })

        return new_shapes

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
            # scale
            sx = px * length
            sy = py * length

            # rotate
            rx = sx * cos_a - sy * sin_a
            ry = sx * sin_a + sy * cos_a

            # translate
            transformed.append((x1 + rx, y1 + ry))

        return transformed

    # =============================================================
    # Pattern Normalization
    # =============================================================
    def _normalize_pattern(self, pattern: Polyline) -> Polyline:
        if len(pattern) < 2:
            logging.warning("FractalGenerator: Pattern too small to normalize.")
            return pattern

        start = pattern[0]
        end = pattern[-1]

        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = math.hypot(dx, dy)

        if length == 0:
            logging.warning("FractalGenerator: Pattern has zero length.")
            return pattern

        angle = math.atan2(dy, dx)
        cos_a = math.cos(-angle)
        sin_a = math.sin(-angle)

        normalized: Polyline = []

        for x, y in pattern:
            # translate to origin
            tx = x - start[0]
            ty = y - start[1]

            # rotate to x-axis
            rx = tx * cos_a - ty * sin_a
            ry = tx * sin_a + ty * cos_a

            # scale to unit
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

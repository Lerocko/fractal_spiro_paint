# =============================================================
# File: spiro_generator.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Adapted: 2025-12-28
# Description:
#     Generates spirograph (hypotrochoid) points using mathematical formulas.
#     Adapted from the original Spirograph Generator project.
# =============================================================

import logging
import math
from typing import List, Tuple

# =============================================================
# SpiroGenerator Class
# =============================================================
class SpiroGenerator:
    """
    Generates spirograph points for given parameters.
    
    This class encapsulates the mathematical logic for generating
    hypotrochoid patterns based on user-defined circle radii and
    pen distance.
    """
    
    # =============================================================
    # Constructor
    # =============================================================
    def __init__(
        self,
        fixed_center: Tuple[float, float],
        fixed_radius: float,
        rolling_center: Tuple[float, float],
        rolling_radius: float,
        pen_position: Tuple[float, float]
    ) -> None:
        """
        Initializes the SpiroGenerator with geometric parameters.
        
        Args:
            fixed_center: Center coordinates of the fixed circle.
            fixed_radius: Radius of the fixed circle (R).
            rolling_center: Center coordinates of the rolling circle.
            rolling_radius: Radius of the rolling circle (r).
            pen_position: Coordinates of the pen point (determines d).
        """
        self.fixed_center = fixed_center
        self.R = fixed_radius
        self.rolling_center = rolling_center
        self.r = rolling_radius
        self.d = math.dist(rolling_center, pen_position)
        
        # Validate parameters
        if self.R <= 0 or self.r <= 0 or self.d <= 0:
            logging.warning("SpiroGenerator: Non-positive parameters may cause issues.")
        
        logging.info(
            f"SpiroGenerator: Initialized with R={self.R:.1f}, "
            f"r={self.r:.1f}, d={self.d:.1f}"
        )
    
    # =============================================================
    # Parameter Scaling (from original project)
    # =============================================================
    def _check_and_scale_parameters(self) -> Tuple[float, float, float, float]:
        """
        Scales parameters if they are too small to avoid floating-point issues.
        
        Returns:
            Tuple of (scaled_R, scaled_r, scaled_d, scale_factor)
        """
        R, r, d = self.R, self.r, self.d
        positive_values = [val for val in [R, r, d] if val > 0]
        
        if not positive_values:
            return R, r, d, 1.0
        
        min_value = min(positive_values)
        
        if min_value < 1.0:
            n = -int(math.floor(math.log10(min_value))) + 1
            scale_factor = 10 ** n
            return R * scale_factor, r * scale_factor, d * scale_factor, scale_factor
        
        return R, r, d, 1.0
    
    # =============================================================
    # Point Generation (core algorithm)
    # =============================================================
    def generate(self, angle_step: int = 5) -> List[Tuple[float, float]]:
        """
        Generates spirograph points for a complete pattern.
        
        Args:
            angle_step: Angular increment in degrees (default: 5).
                        Smaller values yield smoother curves.
        
        Returns:
            List of (x, y) coordinate tuples representing the spirograph.
        """
        # Scale parameters if needed
        R_scaled, r_scaled, d_scaled, scale_factor = self._check_and_scale_parameters()
        
        # Pre-calculate constants
        k = r_scaled / R_scaled if R_scaled != 0 else 0
        l = d_scaled / r_scaled if r_scaled != 0 else 0
        
        if k == 0 or l == 0:
            logging.error("SpiroGenerator: Invalid k or l value, cannot generate points.")
            return []
        
        # Calculate number of rotations for a complete pattern
        numerator = round(R_scaled - r_scaled)
        denominator = round(r_scaled)
        gcd_value = math.gcd(numerator, denominator) if denominator != 0 else 1
        q = (denominator // gcd_value) if gcd_value != 0 else 1
        q = min(q, 50)  # Practical limit
        
        # Generate points
        points: List[Tuple[float, float]] = []
        
        for theta_deg in range(0, 360 * q, angle_step):
            theta_rad = math.radians(theta_deg)
            
            # Hypotrochoid equations (original formula)
            x_rel = R_scaled * (
                (1 - k) * math.cos(theta_rad) +
                l * k * math.cos(((1 - k) / k) * theta_rad)
            )
            y_rel = R_scaled * (
                (1 - k) * math.sin(theta_rad) -
                l * k * math.sin(((1 - k) / k) * theta_rad)
            )
            
            # Scale back if parameters were scaled
            if scale_factor != 1.0:
                x_rel /= scale_factor
                y_rel /= scale_factor
            
            # Translate to actual position (relative to fixed circle center)
            x = self.fixed_center[0] + x_rel
            y = self.fixed_center[1] + y_rel
            
            points.append((x, y))
        
        logging.info(f"SpiroGenerator: Generated {len(points)} points over {q} rotations.")
        return points
    
    # =============================================================
    # Utility Methods
    # =============================================================
    def get_parameters(self) -> dict:
        """Returns the current spirograph parameters."""
        return {
            "fixed_center": self.fixed_center,
            "fixed_radius": self.R,
            "rolling_center": self.rolling_center,
            "rolling_radius": self.r,
            "pen_distance": self.d,
            "k_ratio": self.r / self.R if self.R != 0 else 0,
            "l_ratio": self.d / self.r if self.r != 0 else 0
        }
#MenuTitle: Align Handles On Vertical And Horizontal
# -*- coding: utf-8 -*-
from GlyphsApp import *
from AppKit import NSPoint
import math

font = Glyphs.font

def is_oncurve(node):
    return node.type in (LINE, CURVE)

def is_offcurve(node):
    return node.type == OFFCURVE

def get_handle_angle(node, handle):
    """Calculate angle of handle relative to on-curve node in degrees (0=horizontal right, 90=vertical up)."""
    dx = handle.position.x - node.position.x
    dy = handle.position.y - node.position.y
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    return abs(angle_deg) % 180

def is_angled(angle_deg, epsilon=0.001):
    """Check if handle is angled (not exactly horizontal or vertical)."""
    return not (abs(angle_deg) < epsilon or abs(angle_deg - 90) < epsilon or abs(angle_deg - 180) < epsilon)

def is_diagonal(angle_deg, diagonal_angle=45.0, diagonal_tolerance=10.0):
    """Check if handle angle is near a diagonal (e.g., 45° or 135°)."""
    normalized_angle = min(abs(angle_deg) % 180, 180 - (abs(angle_deg) % 180))
    return abs(normalized_angle - diagonal_angle) < diagonal_tolerance or \
           abs(normalized_angle - (180 - diagonal_angle)) < diagonal_tolerance

def get_handle_offset(node, handle, angle_deg):
    """Calculate perpendicular offset based on intended axis (horizontal or vertical)."""
    normalized_angle = min(abs(angle_deg) % 180, 180 - (abs(angle_deg) % 180))
    dx = abs(handle.position.x - node.position.x)
    dy = abs(handle.position.y - node.position.y)
    if normalized_angle < 45.0:  # Closer to horizontal
        return dy  # y-difference is the perpendicular offset
    else:  # Closer to vertical
        return dx  # x-difference is the perpendicular offset

def align_handle_to_axis(node, handle, angle_deg):
    """Align handle to nearest axis: horizontal if <45° from 0/180, vertical if closer to 90."""
    angle_threshold = 45.0
    normalized_angle = min(abs(angle_deg) % 180, 180 - (abs(angle_deg) % 180))
    try:
        if normalized_angle < angle_threshold:
            # Align horizontal: keep x offset, zero y offset
            new_pos = NSPoint(node.position.x + (handle.position.x - node.position.x), node.position.y)
        else:
            # Align vertical: keep y offset, zero x offset
            new_pos = NSPoint(node.position.x, node.position.y + (handle.position.y - node.position.y))
        handle.position = new_pos
        # Return new angle (will be 0 or 90)
        new_dx = new_pos.x - node.position.x
        new_dy = new_pos.y - node.position.y
        new_angle_rad = math.atan2(new_dy, new_dx)
        return math.degrees(new_angle_rad) % 180
    except Exception as e:
        print(f"      Error aligning handle: {e}")
        return angle_deg  # Return original angle if alignment fails

# Prompt user for offset threshold
try:
    user_input = AskString("Enter offset threshold (units) for fixing angled handles:", "4.0")
    offset_threshold = float(user_input)
    if offset_threshold <= 0:
        print("Invalid input: Threshold must be positive. Using default: 4.0")
        offset_threshold = 4.0
except:
    print("Error with dialog or input. Using default offset threshold: 4.0")
    offset_threshold = 4.0

epsilon = 0.001  # Tolerance for exact h/v detection
diagonal_angle = 45.0  # Center of diagonal angle range (45° or 135°)
diagonal_tolerance = 10.0  # Tolerance for considering an angle as diagonal
processed = 0
total_smooth_nodes_checked = 0

for layer in font.selectedLayers:
    print(f"\nProcessing layer: {layer.parent.name} (offset threshold: {offset_threshold})")
    for path in layer.paths:
        nodes = path.nodes
        n = len(nodes)
        i = 0
        while i < n:
            node = nodes[i]
            if not is_oncurve(node) or not node.smooth:
                i += 1
                continue
            total_smooth_nodes_checked += 1
            # Check for double handles (incoming and outgoing)
            prev_node = nodes[(i - 1) % n] if path.closed else (nodes[i - 1] if i > 0 else None)
            next_node = nodes[(i + 1) % n] if i + 1 < n else None
            if (prev_node and is_offcurve(prev_node) and next_node and is_offcurve(next_node)):
                print(f"  Smooth node at ({node.position.x:.2f}, {node.position.y:.2f})")
                # Incoming handle
                incoming_handle = prev_node
                in_angle = get_handle_angle(node, incoming_handle)
                in_offset = get_handle_offset(node, incoming_handle, in_angle)
                print(f"    Incoming handle angle: {in_angle:.2f}°, offset: {in_offset:.2f}")
                if is_diagonal(in_angle, diagonal_angle, diagonal_tolerance):
                    print(f"      Skipped: angle {in_angle:.2f}° is near diagonal (within {diagonal_tolerance}° of {diagonal_angle}°)")
                elif is_angled(in_angle, epsilon) and in_offset < offset_threshold:
                    new_in_angle = align_handle_to_axis(node, incoming_handle, in_angle)
                    print(f"      Aligned to {new_in_angle:.2f}° (was angled, offset {in_offset:.2f} < {offset_threshold})")
                    processed += 1
                elif not is_angled(in_angle, epsilon):
                    print(f"      Already aligned at {in_angle:.2f}°")
                else:
                    print(f"      Skipped: offset {in_offset:.2f} >= {offset_threshold}")
                
                # Outgoing handle
                outgoing_handle = next_node
                out_angle = get_handle_angle(node, outgoing_handle)
                out_offset = get_handle_offset(node, outgoing_handle, out_angle)
                print(f"    Outgoing handle angle: {out_angle:.2f}°, offset: {out_offset:.2f}")
                if is_diagonal(out_angle, diagonal_angle, diagonal_tolerance):
                    print(f"      Skipped: angle {out_angle:.2f}° is near diagonal (within {diagonal_tolerance}° of {diagonal_angle}°)")
                elif is_angled(out_angle, epsilon) and out_offset < offset_threshold:
                    new_out_angle = align_handle_to_axis(node, outgoing_handle, out_angle)
                    print(f"      Aligned to {new_out_angle:.2f}° (was angled, offset {out_offset:.2f} < {offset_threshold})")
                    processed += 1
                elif not is_angled(out_angle, epsilon):
                    print(f"      Already aligned at {out_angle:.2f}°")
                else:
                    print(f"      Skipped: offset {out_offset:.2f} >= {offset_threshold}")
            
            # Advance: skip handles if present
            if i + 1 < n and is_offcurve(nodes[i + 1]):
                i += 2
            else:
                i += 1

print(f"\nTotal smooth nodes checked: {total_smooth_nodes_checked}")
print(f"Angled handles fixed: {processed}")
print("Tip: Toggle View > Show Angled Handles (Ctrl-Y) to verify highlights before/after.")
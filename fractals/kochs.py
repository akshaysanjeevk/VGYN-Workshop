import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# ---------------------------------------------------
# Subdivide one line segment into 4 Koch segments
# ---------------------------------------------------
def subdivide_segment(p1, p2):
    # Vector from p1 to p2
    v = p2 - p1
    
    # Trisect the segment
    p_a = p1 + v / 3.0
    p_b = p1 + 2.0 * v / 3.0
    
    # Find the peak of the equilateral triangle pointing outwards
    # Rotate vector v/3 by 60 degrees counter-clockwise
    angle = np.pi / 3  # 60 degrees
    rot_matrix = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle),  np.cos(angle)]
    ])
    p_peak = p_a + np.dot(rot_matrix, v / 3.0)
    
    # Return the 4 new segments forming the bump
    return np.array([
        [p1, p_a],
        [p_a, p_peak],
        [p_peak, p_b],
        [p_b, p2]
    ])

# ---------------------------------------------------
# Generate next depth for the snowflake
# ---------------------------------------------------
def next_generation(segments):
    new_segments = []
    for seg in segments:
        children = subdivide_segment(seg[0], seg[1])
        new_segments.extend(children)
    return np.array(new_segments)

# ---------------------------------------------------
# Initial Snowflake Setup (Equilateral Triangle)
# ---------------------------------------------------
# Side length = 1
h = np.sqrt(3) / 2
p1 = np.array([0.0, 0.0])
p2 = np.array([1.0, 0.0])
p3 = np.array([0.5, h])

# Clockwise orientation guarantees the spikes point outwards
initial_segments = np.array([
    [p1, p3],
    [p3, p2],
    [p2, p1]
])

generations = [initial_segments]
max_depth = 6  # Kept lower than Sierpinski because segments scale by 4^depth
depth = 0

# ---------------------------------------------------
# Toggles
# ---------------------------------------------------
show_right_panel = False
show_segments = False
show_area = False
show_boundary = False

# ---------------------------------------------------
# Precompute all generations
# ---------------------------------------------------
for _ in range(max_depth):
    generations.append(next_generation(generations[-1]))

# ---------------------------------------------------
# Figure setup
# ---------------------------------------------------
fig = plt.figure(figsize=(9, 7))

ax_fractal = fig.add_axes([0.05, 0.08, 0.90, 0.84])
ax_area    = fig.add_axes([0.72, 0.69, 0.22, 0.17])
ax_count   = fig.add_axes([0.72, 0.42, 0.22, 0.17])
ax_perim   = fig.add_axes([0.72, 0.15, 0.22, 0.17])

# Initially hidden
ax_area.set_visible(False)
ax_count.set_visible(False)
ax_perim.set_visible(False)

# ---------------------------------------------------
# Draw everything
# ---------------------------------------------------
def draw(depth):
    global show_right_panel

    ax_fractal.clear()
    ax_area.clear()
    ax_count.clear()
    ax_perim.clear()

    # -----------------------------------------------
    # Resize layout
    # -----------------------------------------------
    if show_right_panel:
        ax_fractal.set_position([0.05, 0.08, 0.62, 0.84])
    else:
        ax_fractal.set_position([0.05, 0.08, 0.90, 0.84])

    # -----------------------------------------------
    # Fractal setup
    # -----------------------------------------------
    ax_fractal.set_aspect('equal')
    ax_fractal.axis('off')

    segments = generations[depth]

    # Draw the boundary line segments
    collection = LineCollection(
        segments,
        colors='blue',
        linewidths=1.5 if depth < 4 else 0.8
    )
    ax_fractal.add_collection(collection)

    # Center the camera around the classic snowflake structure
    ax_fractal.set_xlim(-0.2, 1.2)
    ax_fractal.set_ylim(-0.4, 1.0)

    # -----------------------------------------------
    # Quantities (Theoretical Math Formulas)
    # -----------------------------------------------
    # Initial dynamic properties based on side length s = 1
    a0 = np.sqrt(3) / 4  # Area of original triangle
    
    num_segments = 3 * (4**depth)
    boundary_length = 3 * ((4/3)**depth)
    
    if depth == 0:
        snowflake_area = a0
    else:
        # Summation formula for Koch Area: A_n = A_0 * (1 + 3/5 * (1 - (4/9)^n))
        snowflake_area = a0 * (1 + (3/5) * (1 - (4/9)**depth))

    # -----------------------------------------------
    # Information text
    # -----------------------------------------------
    info_lines = [f"Stage($n$): {depth}", ""]

    if show_segments:
        info_lines.append(f"line segments   : {num_segments}")
    if show_area:
        info_lines.append(f"total area      : {snowflake_area:.6f}")
    if show_boundary:
        info_lines.append(f"perimeter       : {boundary_length:.6f}")

    info_lines.extend([
        "",
        "z : toggle segment count",
        "x : toggle snowflake area",
        "c : toggle perimeter",
        "r : toggle graph panel"
    ])

    info = "\n".join(info_lines)
    ax_fractal.text(
        0.02, 0.98, info,
        fontsize=11, family='monospace',
        transform=ax_fractal.transAxes,
        verticalalignment='top'
    )

    # ------------------------------------------------
    # Hide all plots first
    # ------------------------------------------------
    ax_area.set_visible(False)
    ax_count.set_visible(False)
    ax_perim.set_visible(False)

    # ------------------------------------------------
    # Graph Layout and Processing
    # ------------------------------------------------
    if show_right_panel:
        explored_depths = np.arange(depth + 1)
        visible_axes = []

        if show_area:     visible_axes.append(ax_area)
        if show_segments: visible_axes.append(ax_count)
        if show_boundary: visible_axes.append(ax_perim)

        n_visible = len(visible_axes)
        if n_visible > 0:
            top = 0.75
            height = 0.18
            gap = 0.06

            for i, ax in enumerate(visible_axes):
                y = top - i * (height + gap)
                ax.set_position([0.72, y, 0.22, height])
                ax.set_visible(True)

        # --- Area graph ---
        if show_area:
            explored_areas = [a0 if d == 0 else a0 * (1 + (3/5)*(1 - (4/9)**d)) for d in explored_depths]
            ax_area.plot(explored_depths, explored_areas, marker='o', color='grey')
            ax_area.scatter([depth], [snowflake_area], s=80, color='blue')
            ax_area.set_title("Snowflake Area", fontsize=10, family='monospace')
            ax_area.set_xlim(0, max_depth)
            ax_area.set_ylim(a0 * 0.9, a0 * 1.7)

        # --- Segment Count graph ---
        if show_segments:
            explored_counts = 3 * (4**explored_depths)
            ax_count.plot(explored_depths, explored_counts, marker='o', color='grey')
            ax_count.scatter([depth], [num_segments], s=80, color='blue')
            ax_count.set_title("Segment Count", fontsize=10, family='monospace')
            ax_count.set_xlim(0, max_depth)

        # --- Perimeter graph ---
        if show_boundary:
            explored_perims = 3 * ((4/3)**explored_depths)
            ax_perim.plot(explored_depths, explored_perims, marker='o', color='grey')
            ax_perim.scatter([depth], [boundary_length], s=80, color='blue')
            ax_perim.set_title("Perimeter Length", fontsize=10, family='monospace')
            ax_perim.set_xlim(0, max_depth)

    fig.canvas.draw_idle()

# ---------------------------------------------------
# Keyboard controls
# ---------------------------------------------------
def on_key(event):
    global depth, show_right_panel, show_segments, show_area, show_boundary

    if event.key in ['w', 'd'] and depth < max_depth:
        depth += 1
        draw(depth)
    elif event.key in ['s', 'a'] and depth > 0:
        depth -= 1
        draw(depth)
    elif event.key == 'r':
        show_right_panel = not show_right_panel
        draw(depth)
    elif event.key == 'z':
        show_segments = not show_segments
        draw(depth)
    elif event.key == 'x':
        show_area = not show_area
        draw(depth)
    elif event.key == 'c':
        show_boundary = not show_boundary
        draw(depth)

# Connect event and initiate canvas
fig.canvas.mpl_connect('key_press_event', on_key)
draw(depth)
plt.show()
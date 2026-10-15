import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------
# Precompute Barnsley Fern Points (up to max capacity)
# ---------------------------------------------------
max_points = 100000
x_pts = np.zeros(max_points)
y_pts = np.zeros(max_points)

# Initial starting point
cx, cy = 0.0, 0.0

# Generate all points sequentially using the 4 affine transformations
for i in range(1, max_points):
    r = np.random.rand()
    
    if r < 0.01:
        # 1. Stem generation
        cx, cy = 0.0, 0.16 * cy
    elif r < 0.86:
        # 2. Small leaflets / main body
        cx, cy = 0.85 * cx + 0.04 * cy, -0.04 * cx + 0.85 * cy + 1.6
    elif r < 0.93:
        # 3. Left side branches
        cx, cy = 0.20 * cx - 0.26 * cy, 0.23 * cx + 0.22 * cy + 1.6
    else:
        # 4. Right side branches
        cx, cy = -0.15 * cx + 0.28 * cy, 0.26 * cx + 0.24 * cy + 0.44
        
    x_pts[i] = cx
    y_pts[i] = cy

# Define density stages for the interactive presentation
point_counts = [1000, 2500, 5000, 10000, 20000, 40000, 70000, 100000]
max_depth = len(point_counts) - 1
depth = 0

# ---------------------------------------------------
# Interactive Toggles
# ---------------------------------------------------
show_right_panel = False
show_count = False

# ---------------------------------------------------
# Figure & Layout Setup (Dark Mode)
# ---------------------------------------------------
fig = plt.figure(figsize=(9, 7))
fig.patch.set_facecolor('#121212') 

ax_fractal = fig.add_axes([0.05, 0.08, 0.90, 0.84])
ax_graph   = fig.add_axes([0.72, 0.38, 0.22, 0.26])

# Configure panels to match dark theme
for ax in [ax_fractal, ax_graph]:
    ax.set_facecolor('#121212')
    ax.tick_params(colors='white', labelsize=9)
    for spine in ax.spines.values():
        spine.set_color('#444444') 

ax_graph.set_visible(False)

# ---------------------------------------------------
# Draw Canvas
# ---------------------------------------------------
def draw(depth):
    global show_right_panel

    ax_fractal.clear()
    ax_graph.clear()

    # Dynamic panel positioning
    if show_right_panel:
        ax_fractal.set_position([0.05, 0.08, 0.62, 0.84])
    else:
        ax_fractal.set_position([0.05, 0.08, 0.90, 0.84])

    ax_fractal.set_aspect('equal')
    ax_fractal.axis('off')

    # Get the slice of points for the current depth stage
    current_count = point_counts[depth]
    x = x_pts[:current_count]
    y = y_pts[:current_count]

    # Map colors based on the Y-coordinate (height) for an organic forest gradient
    # The higher up the leaf, the brighter green it glows
    colors = plt.cm.summer(y / 10.0)

    # Use scatter plot with tiny marker sizes (s) and alpha transparency to simulate depth
    ax_fractal.scatter(
        x, y, 
        s=0.8 if current_count < 10000 else 0.2, 
        c=colors, 
        alpha=0.7, 
        edgecolors='none'
    )

    # Dynamic camera bound setting to center the fern perfectly
    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()
    x_pad = (x_max - x_min) * 0.05 if x_max != x_min else 0.5
    y_pad = (y_max - y_min) * 0.05 if y_max != y_min else 0.5
    ax_fractal.set_xlim(x_min - x_pad, x_max + x_pad)
    ax_fractal.set_ylim(y_min - y_pad, y_max + y_pad)

    # Info Text Block
    info_lines = [
        f"Stage: {depth + 1} / {len(point_counts)}",
        "",
        f"Plotted Points : {current_count:,}" if show_count else "",
        "",
        "z : toggle point count",
        "r : toggle graph panel"
    ]

    ax_fractal.text(
        0.02, 0.98, "\n".join(info_lines),
        fontsize=11, family='monospace', color='white',
        transform=ax_fractal.transAxes,
        verticalalignment='top'
    )

    ax_graph.set_visible(False)

    if show_right_panel:
        ax_graph.set_visible(True)
        explored_stages = np.arange(depth + 1)
        counts = [point_counts[s] for s in explored_stages]
        
        ax_graph.plot(explored_stages + 1, counts, marker='o', color='#666666')
        ax_graph.scatter([depth + 1], [current_count], s=60, color='lime')
        ax_graph.set_title("Rendered Points", fontsize=10, family='monospace', color='white')
        ax_graph.set_xlim(1, len(point_counts))

    fig.canvas.draw_idle()

# ---------------------------------------------------
# Keyboard Event Processor
# ---------------------------------------------------
def on_key(event):
    global depth, show_right_panel, show_count

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
        show_count = not show_count
        draw(depth)

fig.canvas.mpl_connect('key_press_event', on_key)
draw(depth)
plt.show()
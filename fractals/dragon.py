import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# ---------------------------------------------------
# Generate Dragon Curve via segment rotation
# ---------------------------------------------------
def next_generation(segments):
    new_segments = []
    
    # Rotation matrices for +90 and -90 degrees, scaled down by 1/sqrt(2)
    s = 0.5
    R_left = np.array([[s, -s], 
                       [s,  s]])
    R_right = np.array([[s,  s], 
                        [-s, s]])
    
    for i, seg in enumerate(segments):
        p1, p2 = seg[0], seg[1]
        v = p2 - p1
        
        # Alternate turning left and right at each step
        if i % 2 == 0:
            p_mid = p1 + np.dot(R_left, v)
        else:
            p_mid = p1 + np.dot(R_right, v)
            
        new_segments.append([p1, p_mid])
        new_segments.append([p_mid, p2])
        
    return np.array(new_segments)

# ---------------------------------------------------
# Initial State (Single baseline segment)
# ---------------------------------------------------
initial_segments = np.array([[[0.0, 0.0], [1.0, 0.0]]])

generations = [initial_segments]
max_depth = 12  
depth = 0

# ---------------------------------------------------
# Interactive Toggles
# ---------------------------------------------------
show_right_panel = False
show_segments = False
show_length = False

# ---------------------------------------------------
# Precompute all generations
# ---------------------------------------------------
for _ in range(max_depth):
    generations.append(next_generation(generations[-1]))

# ---------------------------------------------------
# Figure & Layout Setup (Dark Mode)
# ---------------------------------------------------
fig = plt.figure(figsize=(9, 7))
fig.patch.set_facecolor('#121212') # Deep charcoal background

ax_fractal = fig.add_axes([0.05, 0.08, 0.90, 0.84])
ax_count   = fig.add_axes([0.72, 0.55, 0.22, 0.22])
ax_length  = fig.add_axes([0.72, 0.20, 0.22, 0.22])

# Configure panels to match dark theme
for ax in [ax_fractal, ax_count, ax_length]:
    ax.set_facecolor('#121212')
    ax.tick_params(colors='white', labelsize=9)
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    for spine in ax.spines.values():
        spine.set_color('#444444') # Muted borders for graphs

# Initially hidden panels
ax_count.set_visible(False)
ax_length.set_visible(False)

# ---------------------------------------------------
# Draw Canvas
# ---------------------------------------------------
def draw(depth):
    global show_right_panel

    ax_fractal.clear()
    ax_count.clear()
    ax_length.clear()

    # Dynamic panel positioning
    if show_right_panel:
        ax_fractal.set_position([0.05, 0.08, 0.62, 0.84])
    else:
        ax_fractal.set_position([0.05, 0.08, 0.90, 0.84])

    ax_fractal.set_aspect('equal')
    ax_fractal.axis('off')

    segments = generations[depth]

    # 'plasma' and 'inferno' maps work brilliantly against dark backgrounds
    color_map = plt.cm.plasma(np.linspace(0, 0.85, len(segments)))

    collection = LineCollection(
        segments,
        colors=color_map,
        linewidths=1.8 if depth < 6 else 0.9
    )
    ax_fractal.add_collection(collection)

    # Dynamic camera bound setting
    all_points = segments.reshape(-1, 2)
    x_coords, y_coords = all_points[:, 0], all_points[:, 1]
    
    x_min, x_max = x_coords.min(), x_coords.max()
    y_min, y_max = y_coords.min(), y_coords.max()
    
    x_pad = (x_max - x_min) * 0.05 if x_max != x_min else 0.1
    y_pad = (y_max - y_min) * 0.05 if y_max != y_min else 0.1
    
    ax_fractal.set_xlim(x_min - x_pad, x_max + x_pad)
    ax_fractal.set_ylim(y_min - y_pad, y_max + y_pad)

    # Calculate properties
    num_segments = 2**depth
    total_length = np.sqrt(2)**depth

    # Info Text Block (Styled White)
    info_lines = [f"Depth: {depth}", ""]
    if show_segments:
        info_lines.append(f"segments     : {num_segments}")
    if show_length:
        info_lines.append(f"total length : {total_length:.4f}")

    info_lines.extend([
        "",
        "z : toggle segment count",
        "x : toggle total length",
        "r : toggle graph panel"
    ])

    ax_fractal.text(
        0.02, 0.98, "\n".join(info_lines),
        fontsize=11, family='monospace', color='white',
        transform=ax_fractal.transAxes,
        verticalalignment='top'
    )

    # Reset panel visibilities first
    ax_count.set_visible(False)
    ax_length.set_visible(False)

    if show_right_panel:
        explored_depths = np.arange(depth + 1)
        visible_axes = []

        if show_segments: visible_axes.append(ax_count)
        if show_length:   visible_axes.append(ax_length)

        n_visible = len(visible_axes)
        if n_visible > 0:
            top = 0.70
            height = 0.24
            gap = 0.08
            for i, ax in enumerate(visible_axes):
                y = top - i * (height + gap)
                ax.set_position([0.72, y, 0.22, height])
                ax.set_visible(True)

        if show_segments:
            counts = 2**explored_depths
            ax_count.plot(explored_depths, counts, marker='o', color='#666666')
            ax_count.scatter([depth], [num_segments], s=60, color='darkorange')
            ax_count.set_title("Segment Count", fontsize=10, family='monospace', color='white')
            ax_count.set_xlim(0, max_depth)

        if show_length:
            lengths = np.sqrt(2)**explored_depths
            ax_length.plot(explored_depths, lengths, marker='o', color='#666666')
            ax_length.scatter([depth], [total_length], s=60, color='darkorange')
            ax_length.set_title("Total Line Length", fontsize=10, family='monospace', color='white')
            ax_length.set_xlim(0, max_depth)

    fig.canvas.draw_idle()

# ---------------------------------------------------
# Keyboard Event Processor
# ---------------------------------------------------
def on_key(event):
    global depth, show_right_panel, show_segments, show_length

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
        show_length = not show_length
        draw(depth)

fig.canvas.mpl_connect('key_press_event', on_key)
draw(depth)
plt.show()
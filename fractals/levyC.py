import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# ---------------------------------------------------
# Generate Fractal Tree / Cauliflower Branches
# ---------------------------------------------------
def next_generation(segments):
    """
    
    Takes every branch segment and grows two new smaller branches 
    off its tip, splitting left and right at 45-degree angles.
    """
    new_segments = []
    
    # Rotation matrices for +45 and -45 degrees, scaled down by 1/sqrt(2)
    s = 1.0 /  5
    theta = np.radians(90)
    
    # theta = np.radians(np.random.uniform(0,45))
    
    R_left = np.array([[np.cos(theta), -np.sin(theta)], 
                       [np.sin(theta),  np.cos(theta)]]) * s
                       
    R_right = np.array([[np.cos(-theta), -np.sin(-theta)], 
                        [np.sin(-theta),  np.cos(-theta)]]) * s
    
    for seg in segments:
        # seg[1] is the tip of the current branch
        p_start = seg[1]
        v = seg[1] - seg[0]  # The direction vector of the current branch
        
        # Calculate the two new split branches extending from the tip
        p_left = p_start + np.dot(R_left, v)
        p_right = p_start + np.dot(R_right, v)
            
        new_segments.append([p_start, p_left])
        new_segments.append([p_start, p_right])
        
    return np.array(new_segments)

# ---------------------------------------------------
# Initial State (A single vertical stalk/trunk)
# ---------------------------------------------------
initial_stalk = np.array([[[0.0, 0.0], [0.0, 1.0]]])

generations = [initial_stalk]
max_depth = 11  # Scales by 2^depth
depth = 0

# ---------------------------------------------------
# Interactive Toggles
# ---------------------------------------------------
show_right_panel = False
show_segments = False

# ---------------------------------------------------
# Precompute all generations
# ---------------------------------------------------
for _ in range(max_depth):
    generations.append(next_generation(generations[-1]))

# ---------------------------------------------------
# Figure & Layout Setup (Dark Mode)
# ---------------------------------------------------
fig = plt.figure(figsize=(9, 7))
fig.patch.set_facecolor('#121212') 

ax_fractal = fig.add_axes([0.05, 0.08, 0.90, 0.84])
ax_count   = fig.add_axes([0.72, 0.38, 0.22, 0.26])

# Configure panels
for ax in [ax_fractal, ax_count]:
    ax.set_facecolor('#121212')
    ax.tick_params(colors='white', labelsize=9)
    for spine in ax.spines.values():
        spine.set_color('#444444') 

ax_count.set_visible(False)

# ---------------------------------------------------
# Draw Canvas
# ---------------------------------------------------
def draw(depth):
    global show_right_panel

    ax_fractal.clear()
    ax_count.clear()

    if show_right_panel:
        ax_fractal.set_position([0.05, 0.08, 0.62, 0.84])
    else:
        ax_fractal.set_position([0.05, 0.08, 0.90, 0.84])

    ax_fractal.set_aspect('equal')
    ax_fractal.axis('off')

    # Gather all generations up to the current depth to draw the WHOLE plant
    all_visible_segments = []
    colors_list = []
    
    # A vibrant green-to-yellow chartreuse map perfectly mimicking Romanesco broccoli
    cmap = plt.cm.YlGn
    
    for d in range(depth + 1):
        gen_segs = generations[d]
        all_visible_segments.extend(gen_segs)
        
        # Map colors so the trunk is dark green and the dense top florets are bright yellow/green
        color_val = 0.4 + (d / max_depth) * 0.5
        colors_list.extend([cmap(color_val)] * len(gen_segs))

    collection = LineCollection(
        all_visible_segments,
        colors=colors_list,
        linewidths=[max(0.5, 3.5 - d*0.3) for d in range(depth + 1) for _ in range(len(generations[d]))]
    )
    ax_fractal.add_collection(collection)

    # Dynamic camera bound setting to perfectly frame the plant
    flat_points = np.array(all_visible_segments).reshape(-1, 2)
    x_coords, y_coords = flat_points[:, 0], flat_points[:, 1]
    
    x_min, x_max = x_coords.min(), x_coords.max()
    y_min, y_max = y_coords.min(), y_coords.max()
    
    x_pad = (x_max - x_min) * 0.1 if x_max != x_min else 0.5
    y_pad = (y_max - y_min) * 0.1 if y_max != y_min else 0.5
    
    ax_fractal.set_xlim(x_min - x_pad, x_max + x_pad)
    ax_fractal.set_ylim(y_min - y_pad, y_max + y_pad)

    # Info Text Block
    num_tips = 2**depth
    info_lines = [
        f"Depth: {depth}",
        "",
        f"Floret Tips : {num_tips}" if show_segments else "",
        "",
        "z : toggle tip count",
        "r : toggle graph panel"
    ]

    ax_fractal.text(
        0.02, 0.98, "\n".join(info_lines),
        fontsize=11, family='monospace', color='white',
        transform=ax_fractal.transAxes,
        verticalalignment='top'
    )

    ax_count.set_visible(False)

    if show_right_panel:
        ax_count.set_visible(True)
        explored_depths = np.arange(depth + 1)
        tips = 2**explored_depths
        
        ax_count.plot(explored_depths, tips, marker='o', color='#666666')
        ax_count.scatter([depth], [num_tips], s=60, color='chartreuse')
        ax_count.set_title("Floret Tip Count", fontsize=10, family='monospace', color='white')
        ax_count.set_xlim(0, max_depth)

    fig.canvas.draw_idle()

# ---------------------------------------------------
# Keyboard Event Processor
# ---------------------------------------------------
def on_key(event):
    global depth, show_right_panel, show_segments

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

fig.canvas.mpl_connect('key_press_event', on_key)
draw(depth)
plt.show()
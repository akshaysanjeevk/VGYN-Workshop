import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


# ---------------------------------------------------
# Subdivide one triangle
# ---------------------------------------------------

def subdivide(tri):

    p1, p2, p3 = tri

    m12 = (p1 + p2) / 2
    m23 = (p2 + p3) / 2
    m31 = (p3 + p1) / 2

    return [
        np.array([p1,  m12, m31]),
        np.array([m12, p2,  m23]),
        np.array([m31, m23, p3 ])
    ]


# ---------------------------------------------------
# Generate next depth
# ---------------------------------------------------

def next_generation(triangles):

    new_triangles = []

    for tri in triangles:

        children = subdivide(tri)

        new_triangles.extend(children)

    return new_triangles


# ---------------------------------------------------
# Initial triangle
# ---------------------------------------------------

initial_triangle = np.array([
    [0, 0],
    [1, 0],
    [0.5, np.sqrt(3)/2]
])

generations = [[initial_triangle]]

max_depth = 10
depth = 0

# Toggle for right-side panels
show_right_panel = False


# ---------------------------------------------------
# Figure setup
# ---------------------------------------------------

fig = plt.figure(figsize=(8, 6))

# Main fractal plot
ax_fractal = fig.add_axes([0.05, 0.08, 0.90, 0.84])

# Smaller side plots
ax_area  = fig.add_axes([0.72, 0.60, 0.22, 0.22])
ax_count = fig.add_axes([0.72, 0.22, 0.22, 0.22])

# Initially hidden
ax_area.set_visible(False)
ax_count.set_visible(False)


# ---------------------------------------------------
# Draw everything
# ---------------------------------------------------

def draw(depth):

    global show_right_panel

    # -----------------------------------------------
    # Clear axes
    # -----------------------------------------------

    ax_fractal.clear()
    ax_area.clear()
    ax_count.clear()

    # -----------------------------------------------
    # Resize fractal panel dynamically
    # -----------------------------------------------

    if show_right_panel:

        ax_fractal.set_position([0.05, 0.08, 0.62, 0.84])

        ax_area.set_visible(True)
        ax_count.set_visible(True)

    else:

        ax_fractal.set_position([0.05, 0.08, 0.90, 0.84])

        ax_area.set_visible(False)
        ax_count.set_visible(False)

    # -----------------------------------------------
    # Fractal axis setup
    # -----------------------------------------------

    ax_fractal.set_aspect('equal')
    ax_fractal.axis('off')

    triangles = generations[depth]

    # -----------------------------------------------
    # Draw triangles
    # -----------------------------------------------

    for tri in triangles:

        patch = Polygon(
            tri,
            edgecolor='black',
            facecolor='red'
        )

        ax_fractal.add_patch(patch)

    # -----------------------------------------------
    # Information panel
    # -----------------------------------------------

    area_fraction = (3/4)**depth

    info = (
        f"Depth: {depth}\n"
        f"Triangles: {len(triangles)}\n"
        f"Remaining Area: {area_fraction:.6f}\n\n"
        f"W / D : Increase depth\n"
        f"S / A : Decrease depth\n"
        f"R     : Toggle info panel"
    )

    ax_fractal.text(
        0.05,
        0.80,
        info,
        fontsize=12,
        family='monospace',
        transform=ax_fractal.transAxes
    )

    # -----------------------------------------------
    # Draw right panel only if enabled
    # -----------------------------------------------

    if show_right_panel:

        # -------------------------------------------
        # Theoretical curves
        # -------------------------------------------

        theory_depths = np.arange(max_depth + 1)

        theory_areas = (3/4)**theory_depths

        theory_counts = 3**theory_depths

        # -------------------------------------------
        # Current explored values
        # -------------------------------------------

        explored_depths = np.arange(depth + 1)

        explored_areas = (3/4)**explored_depths

        explored_counts = 3**explored_depths

        # -------------------------------------------
        # Area plot
        # -------------------------------------------

        ax_area.plot(
            theory_depths,
            theory_areas,
            linewidth=1,
            alpha=0.5,
            color='grey'
        )

        ax_area.plot(
            explored_depths,
            explored_areas,
            marker='o',
            color='grey'
        )

        ax_area.scatter(
            [depth],
            [area_fraction],
            s=80,
            zorder=5,
            color='red'
        )

        ax_area.set_title(
            "Remaining Area",
            family='monospace',
            fontsize=11
        )

        ax_area.set_xlabel(
            "Depth",
            family='monospace',
            fontsize=9
        )

        ax_area.set_ylabel(
            "Area",
            family='monospace',
            fontsize=9
        )

        ax_area.set_xlim(0, max_depth)

        ax_area.set_ylim(0, 1.05)

        # -------------------------------------------
        # Triangle count plot
        # -------------------------------------------

        ax_count.plot(
            theory_depths,
            theory_counts,
            linewidth=2,
            alpha=0.5,
            color='grey'
        )

        ax_count.plot(
            explored_depths,
            explored_counts,
            marker='o',
            color='grey'
        )

        ax_count.scatter(
            [depth],
            [3**depth],
            s=80,
            zorder=5,
            color='red'
        )

        ax_count.set_title(
            "Solid Triangles",
            fontsize=11,
            family='monospace'
        )

        ax_count.set_xlabel(
            "Depth",
            fontsize=9,
            family='monospace'
        )

        ax_count.set_ylabel(
            "Count",
            fontsize=9,
            family='monospace'
        )

        ax_count.set_xlim(0, max_depth)

        ax_count.set_yscale('log')

    plt.draw()


# ---------------------------------------------------
# Keyboard controls
# ---------------------------------------------------

def on_key(event):

    global depth
    global generations
    global show_right_panel

    # -----------------------------------------------
    # Increase depth
    # -----------------------------------------------

    if event.key in ['w', 'd']:

        if depth < max_depth:

            if depth + 1 >= len(generations):

                next_triangles = next_generation(
                    generations[depth]
                )

                generations.append(next_triangles)

            depth += 1

            draw(depth)

    # -----------------------------------------------
    # Decrease depth
    # -----------------------------------------------

    elif event.key in ['s', 'a']:

        if depth > 0:

            depth -= 1

            draw(depth)

    # -----------------------------------------------
    # Toggle right panel
    # -----------------------------------------------

    elif event.key == 'r':

        show_right_panel = not show_right_panel

        draw(depth)


# ---------------------------------------------------
# Connect keyboard event
# ---------------------------------------------------

fig.canvas.mpl_connect(
    'key_press_event',
    on_key
)

# ---------------------------------------------------
# Initial draw
# ---------------------------------------------------

draw(depth)

plt.show()
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection


# ---------------------------------------------------
# Subdivide one triangle
# ---------------------------------------------------

def subdivide(tri):

    p1, p2, p3 = tri

    m12 = (p1 + p2) / 2
    m23 = (p2 + p3) / 2
    m31 = (p3 + p1) / 2

    return np.array([
        [p1,  m12, m31],
        [m12, p2,  m23],
        [m31, m23, p3 ]
    ])


# ---------------------------------------------------
# Generate next depth
# ---------------------------------------------------

def next_generation(triangles):

    new_triangles = []

    for tri in triangles:

        children = subdivide(tri)

        new_triangles.extend(children)

    return np.array(new_triangles)


# ---------------------------------------------------
# Initial triangle
# ---------------------------------------------------

initial_triangle = np.array([
    [0, 0],
    [1, 0],
    [0.5, np.sqrt(3)/2]
])

generations = [np.array([initial_triangle])]

max_depth = 10
depth = 0


# ---------------------------------------------------
# Toggles
# ---------------------------------------------------

show_right_panel = False

show_triangles = False
show_area = False
show_boundary = False
show_side = False


# ---------------------------------------------------
# Precompute all generations
# ---------------------------------------------------

for _ in range(max_depth):

    generations.append(
        next_generation(generations[-1])
    )


# ---------------------------------------------------
# Figure setup
# ---------------------------------------------------

fig = plt.figure(figsize=(8, 6))

ax_fractal = fig.add_axes([0.05, 0.08, 0.90, 0.84])

ax_area  = fig.add_axes([0.72, 0.69, 0.22, 0.17])

ax_count = fig.add_axes([0.72, 0.42, 0.22, 0.17])

ax_perim = fig.add_axes([0.72, 0.15, 0.22, 0.17])


# ---------------------------------------------------
# Initially hidden
# ---------------------------------------------------

ax_area.set_visible(False)
ax_count.set_visible(False)
ax_perim.set_visible(False)


# ---------------------------------------------------
# Precompute theory curves
# ---------------------------------------------------

theory_depths = np.arange(max_depth + 1)

theory_areas = (3/4)**theory_depths

theory_counts = 3**theory_depths

theory_perimeters = 3 * (3/2)**theory_depths


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

    triangles = generations[depth]

    edge_color = 'black' if depth < 7 else 'none'

    collection = PolyCollection(
        triangles,
        facecolors='red',
        edgecolors=edge_color,
        linewidths=0.2
    )

    ax_fractal.add_collection(collection)

    ax_fractal.set_xlim(-0.05, 1.05)

    ax_fractal.set_ylim(-0.05, 0.92)

    # -----------------------------------------------
    # Quantities
    # -----------------------------------------------

    num_triangles = 3**depth

    area_fraction = (3/4)**depth

    boundary_length = 3 * (3/2)**depth

    side_length = (1/2)**depth

    # -----------------------------------------------
    # Information text
    # -----------------------------------------------

    info_lines = [f"Depth: {depth}", ""]

    if show_triangles:

        info_lines.append(
            f"coloured triangles : {num_triangles}"
        )

    if show_area:

        info_lines.append(
            f"remaining area     : {area_fraction:.6f}"
        )

    if show_boundary:

        info_lines.append(
            f"boundary length    : {boundary_length:.6f}"
        )

    # if show_side:

    #     info_lines.append(
    #         f"triangle side      : {side_length:.6f}"
    #     )

    info_lines.extend([
        "",
        "z : toggle number of triangles",
        "x : toggle shaded area",
        "c : toggle boundary",
        # "v : toggle side length",
        "r : toggle graph panel"
    ])

    info = "\n".join(info_lines)

    ax_fractal.text(
        0.05,
        0.82,
        info,
        fontsize=11,
        family='monospace',
        transform=ax_fractal.transAxes
    )

    # ------------------------------------------------
    # Hide all plots first
    # ------------------------------------------------

    ax_area.set_visible(False)
    ax_count.set_visible(False)
    ax_perim.set_visible(False)

    # ------------------------------------------------
    # Graphs
    # ------------------------------------------------

    if show_right_panel:

        explored_depths = np.arange(depth + 1)

        # --------------------------------------------
        # Dynamic positioning
        # --------------------------------------------

        visible_axes = []

        if show_area:

            visible_axes.append(ax_area)

        if show_triangles:

            visible_axes.append(ax_count)

        if show_boundary:

            visible_axes.append(ax_perim)

        n_visible = len(visible_axes)

        if n_visible > 0:

            top = 0.75

            height = 0.18

            gap = 0.06

            for i, ax in enumerate(visible_axes):

                y = top - i * (height + gap)

                ax.set_position([0.72, y, 0.22, height])

                ax.set_visible(True)

        # --------------------------------------------
        # Area graph
        # --------------------------------------------

        if show_area:

            explored_areas = (3/4)**explored_depths

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
                color='red'
            )

            ax_area.set_title(
                "Remaining Area",
                fontsize=10,
                family='monospace'
            )

            ax_area.set_xlim(0, max_depth)

            ax_area.set_ylim(0, 1.05)

        # --------------------------------------------
        # Triangle graph
        # --------------------------------------------

        if show_triangles:

            explored_counts = 3**explored_depths

            ax_count.plot(
                theory_depths,
                theory_counts,
                linewidth=1.5,
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
                [num_triangles],
                s=80,
                color='red'
            )

            ax_count.set_title(
                "Solid Triangles",
                fontsize=10,
                family='monospace'
            )

            ax_count.set_xlim(0, max_depth)

            ax_count.set_yscale('log')

        # --------------------------------------------
        # Boundary graph
        # --------------------------------------------

        if show_boundary:

            explored_perimeters = (
                3 * (3/2)**explored_depths
            )

            ax_perim.plot(
                theory_depths,
                theory_perimeters,
                linewidth=1.5,
                alpha=0.5,
                color='grey'
            )

            ax_perim.plot(
                explored_depths,
                explored_perimeters,
                marker='o',
                color='grey'
            )

            ax_perim.scatter(
                [depth],
                [boundary_length],
                s=80,
                color='red'
            )

            ax_perim.set_title(
                "Boundary Length",
                fontsize=10,
                family='monospace'
            )

            ax_perim.set_xlim(0, max_depth)

            ax_perim.set_yscale('log')

    fig.canvas.draw_idle()


# ---------------------------------------------------
# Keyboard controls
# ---------------------------------------------------

def on_key(event):

    global depth
    global show_right_panel

    global show_triangles
    global show_area
    global show_boundary
    global show_side

    # -----------------------------------------------
    # Increase depth
    # -----------------------------------------------

    if event.key in ['w', 'd']:

        if depth < max_depth:

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
    # Toggle graphs
    # -----------------------------------------------

    elif event.key == 'r':

        show_right_panel = not show_right_panel

        draw(depth)

    # -----------------------------------------------
    # Toggle triangles
    # -----------------------------------------------

    elif event.key == 'z':

        show_triangles = not show_triangles

        draw(depth)

    # -----------------------------------------------
    # Toggle area
    # -----------------------------------------------

    elif event.key == 'x':

        show_area = not show_area

        draw(depth)

    # -----------------------------------------------
    # Toggle boundary
    # -----------------------------------------------

    elif event.key == 'c':

        show_boundary = not show_boundary

        draw(depth)

    # -----------------------------------------------
    # Toggle side length
    # -----------------------------------------------

    elif event.key == 'v':

        show_side = not show_side

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
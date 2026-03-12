# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 12:05:39 2026

@author: jmarggra
"""

import numpy as np
from scipy import ndimage as ndi
from scipy.spatial import cKDTree
from PIL import Image, ImageFile
import os
import math
import matplotlib.pyplot as plt
import csv
import matplotlib.patheffects as pe\
    
"""
Compute the minimum edge-to-edge distance between distinct white features
in a binary raster (white = features, black = background).

Designed for very large images exported from Photoshop.

What this script does:
 1) Load the image and threshold to get a boolean mask (True = white features).
 2) Label connected components (4- or 8-connectivity).
 3) Extract 1-pixel-wide boundaries of each component.
 4) Build a KD-tree over all boundary pixels.
 5) For each boundary pixel, find the nearest boundary pixel from a *different* component.
 6) Report the global minimum distance, the two closest points, and their component IDs.
 7) Save results to a text file. Optionally create a visualization (downscaled).
"""

    
# --- Allow large PNGs 
Image.MAX_IMAGE_PIXELS = 300_000_000  
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Define paths
# image_path = r"C:\Users\jmarggra\Documents\Analysis\Thin_sections\Lester_Top6_5x\Lester_Top6_5x_Amygdules_BW.png"
image_path = r"C:\Users\jmarggra\Documents\Analysis\Thin_sections\Lester_Top4_5x\combi0102_amygdules_BW.png"
out_dir    = r"C:\Users\jmarggra\Documents\Analysis\Thin_sections\Lester_Top4_5x"

# Definitions
def load_binary_image(path, white_as_feature=True, threshold=128):
    img = Image.open(path).convert('L')
    arr = np.array(img)
    features = arr >= threshold
    if not white_as_feature:
        features = ~features
    return features

def label_components(features, connectivity=2):
    structure = ndi.generate_binary_structure(rank=2, connectivity=connectivity)
    labels, num = ndi.label(features, structure=structure)
    return labels, num

def extract_inner_boundary(mask):
    # cross-shaped kernel (gentler than full 3x3)
    se = np.array([[0,1,0],
                   [1,1,1],
                   [0,1,0]], dtype=bool)
    eroded = ndi.binary_erosion(mask, structure=se, border_value=0)
    boundary = mask ^ eroded
    return boundary

def build_boundary_points(labels, num_components):
    points_list, owners_list = [], []
    label_to_indices = {}

    offset = 0
    for lab in range(1, num_components + 1):
        comp_mask = (labels == lab)
        if not np.any(comp_mask):
            continue
        boundary = extract_inner_boundary(comp_mask)
        coords = np.column_stack(np.nonzero(boundary))
        if coords.size == 0:
            coords = np.column_stack(np.nonzero(comp_mask))

        points_list.append(coords)
        owners_list.append(np.full(coords.shape[0], lab, dtype=np.int64))
        label_to_indices[lab] = np.arange(offset, offset + coords.shape[0])
        offset += coords.shape[0]

    if points_list:
        points = np.vstack(points_list).astype(float)
        owners = np.concatenate(owners_list).astype(np.int64)
    else:
        points = np.empty((0, 2), dtype=float)
        owners = np.empty((0,), dtype=np.int64)
    return points, owners, label_to_indices

def pairwise_min_edge_distances(points, owners, label_to_indices, tol=1e-12):
    labels_sorted = sorted(label_to_indices.keys())
    rows = []
    for a in range(len(labels_sorted)):
        li = labels_sorted[a]
        Ai = label_to_indices[li]
        if Ai.size == 0: 
            continue
        for b in range(a+1, len(labels_sorted)):
            lj = labels_sorted[b]
            Aj = label_to_indices[lj]
            if Aj.size == 0: 
                continue

            if Ai.size <= Aj.size:
                tree = cKDTree(points[Ai])
                d, j = tree.query(points[Aj], k=1)
                base, to = Aj, Ai
            else:
                tree = cKDTree(points[Aj])
                d, j = tree.query(points[Ai], k=1)
                base, to = Ai, Aj

            d = np.atleast_1d(d); j = np.atleast_1d(j)
            if d.size == 0 or not np.isfinite(d).any():
                continue

            min_d = float(np.min(d))
            tie_ids = np.where(np.abs(d - min_d) <= tol)[0]
            t = tie_ids[0]
            p_global = int(base[t]); q_global = int(to[j[t]])
            pr, pc = float(points[p_global, 0]), float(points[p_global, 1])
            qr, qc = float(points[q_global, 0]), float(points[q_global, 1])

            rows.append({
                'label_i': int(li), 'label_j': int(lj),
                'min_dist_px': float(min_d), 'tie_count': int(tie_ids.size),
                'p_index': p_global, 'q_index': q_global,
                'p_row': pr, 'p_col': pc, 'q_row': qr, 'q_col': qc
            })
    return rows

def reduce_to_nearest_neighbor(rows, pixel_size=None):
    labels_set = set()
    for r in rows:
        labels_set.add(r['label_i']); labels_set.add(r['label_j'])
    labels_sorted = sorted(labels_set)

    best = {lab: {'label': lab, 'nearest_label': None, 'min_dist_px': math.inf,
                  'min_dist_phys_mum': None, 'p_row': None, 'p_col': None,
                  'q_row': None, 'q_col': None}
            for lab in labels_sorted}

    for r in rows:
        li, lj, dpx = r['label_i'], r['label_j'], r['min_dist_px']
        if dpx < best[li]['min_dist_px']:
            best[li].update({'min_dist_px': dpx, 'nearest_label': lj,
                             'p_row': r['p_row'], 'p_col': r['p_col'],
                             'q_row': r['q_row'], 'q_col': r['q_col']})
        if dpx < best[lj]['min_dist_px']:
            best[lj].update({'min_dist_px': dpx, 'nearest_label': li,
                             'p_row': r['q_row'], 'p_col': r['q_col'],
                             'q_row': r['p_row'], 'q_col': r['p_col']})

    out = []
    for lab in labels_sorted:
        row = best[lab]
        if pixel_size is not None and math.isfinite(row['min_dist_px']):
            row['min_dist_phys_mum'] = row['min_dist_px'] * float(pixel_size)
        out.append(row)
    return out

def build_distance_matrix(rows):
    labels_set = set()
    for r in rows:
        labels_set.add(r['label_i']); labels_set.add(r['label_j'])
    labels_sorted = sorted(labels_set)
    idx = {lab: i for i, lab in enumerate(labels_sorted)}
    n = len(labels_sorted)
    M = [[float('nan')]*n for _ in range(n)]
    for r in rows:
        i = idx[r['label_i']]; j = idx[r['label_j']]
        d = r['min_dist_px']
        if math.isnan(M[i][j]) or d < M[i][j]:
            M[i][j] = d; M[j][i] = d
    return labels_sorted, M

def compute_component_centroids(labels, label_ids=None):
    """
    Return dict: label_id -> (row, col) centroid (float).
    """
    if label_ids is None:
        label_ids = [lab for lab in np.unique(labels) if lab != 0]
    centroids = {}
    for lab in label_ids:
        ys, xs = np.nonzero(labels == lab)
        if ys.size == 0:
            continue
        centroids[lab] = (float(ys.mean()), float(xs.mean()))
    return centroids

def prepare_display_image(features_bool, max_dim=4000):
    """
    Convert a boolean mask to a uint8 image and downscale if needed for plotting.
    Returns (disp_img_uint8, scale_factor).
    scale_factor = disp_img_size / original_size (same for rows and cols).
    """
    h, w = features_bool.shape
    # uint8 0/255 for display
    img_u8 = (features_bool.astype(np.uint8) * 255)
    scale = 1.0
    if max(h, w) > max_dim:
        if h >= w:
            scale = max_dim / float(h)
        else:
            scale = max_dim / float(w)
        new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
        # PIL expects size = (width, height)
        disp = Image.fromarray(img_u8, mode='L').resize(new_size, Image.BILINEAR)
        disp = np.array(disp)
    else:
        disp = img_u8
    return disp, float(scale)

def plot_shortest_feature_distances(features_bool,
                                    labels,
                                    pairwise_rows,
                                    pixel_size=None,
                                    top_k=20,
                                    max_dim=4000,
                                    figsize=(10, 10),
                                    dpi=200,
                                    out_path=None,
                                    annotate_all_components=True,
                                    text_size=8,
                                    line_width=2):
    """
    Create an overview PNG with:
      - background = (downscaled) binary mask
      - red lines = TOP-K shortest inter-feature segments
      - per-segment distance annotation (px and physical units if pixel_size provided)
      - component IDs at centroids (optional)

    Returns: out_path
    """
    # Prepare display image & scale factor
    disp_img, sf = prepare_display_image(features_bool, max_dim=max_dim)
    h, w = features_bool.shape

    # Sort pairs by distance and keep top_k
    rows_sorted = sorted(pairwise_rows, key=lambda r: r['min_dist_px'])
    rows_show = rows_sorted[:min(top_k, len(rows_sorted))]

    # Compute centroids for labels (before scaling)
    labs = [lab for lab in np.unique(labels) if lab != 0]
    centroids = compute_component_centroids(labels, labs)

    # Start plot
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.imshow(disp_img, cmap='gray', interpolation='nearest')
    ax.set_axis_off()
    ax.set_title(f"Shortest inter-feature distances (top {len(rows_show)})")

    # helper: outline for readability
    outline = [pe.withStroke(linewidth=2.5, foreground='black')]

    # Draw all component labels at centroid
    if annotate_all_components:
        for lab in labs:
            if lab not in centroids: 
                continue
            r, c = centroids[lab]
            ax.text(c*sf, r*sf, str(lab),
                    color='yellow', fontsize=text_size,
                    ha='center', va='center',
                    path_effects=outline)

    # Draw shortest segments with annotations
    for r in rows_show:
        (r1, c1) = (r['p_row'], r['p_col'])
        (r2, c2) = (r['q_row'], r['q_col'])
        # scale for display
        x1, y1 = c1 * sf, r1 * sf
        x2, y2 = c2 * sf, r2 * sf
        ax.plot([x1, x2], [y1, y2], color='red', lw=line_width, alpha=0.95)

        # Distance text near the midpoint
        midx, midy = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        label_i, label_j = r['label_i'], r['label_j']
        txt = f"{r['min_dist_px']:.2f} px"
        if pixel_size is not None:
            txt += f" ({r['min_dist_px']*float(pixel_size):.2f} units)"
        ax.text(midx, midy, f"{txt}\n[{label_i}–{label_j}]",
                color='white', fontsize=max(7, text_size-1),
                ha='center', va='center',
                path_effects=outline)

    # Save
    if out_path is None:
        out_path = "shortest_feature_distances.png"
    fig.tight_layout(pad=0)
    fig.savefig(out_path, bbox_inches='tight', pad_inches=0.3)
    plt.close(fig)
    return out_path

def compute_and_save_all_min_distances(
    image_path,
    out_dir=None,
    pixel_size=None,
    white_as_feature=True,
    connectivity=2,
    threshold=128,
    diagnostics=True,
    write_matrix=True,
    # plotting params:
    top_k_plot=20,
    plot_max_dim=4000,
    figsize=(10, 10),
    dpi=200,
    annotate_all_components=True,
    text_size=8,
    line_width=2
):
    """
    Compute minimum edge-to-edge distances between all features and save:
      - pairwise list (CSV)
      - per-component nearest neighbor (CSV)
      - optional NxN distance matrix (CSV)
      - overview PNG: top-K shortest segments + component labels

    Returns a dict with file paths and stats.
    """
    if out_dir is None:
        out_dir = os.path.dirname(os.path.abspath(image_path))
    os.makedirs(out_dir, exist_ok=True)

    # --- Load & label ---
    features = load_binary_image(image_path, white_as_feature=white_as_feature, threshold=threshold)
    labels, num = label_components(features, connectivity=connectivity)
    if num < 2 and connectivity == 2:
        labels, num = label_components(features, connectivity=1)

    if diagnostics:
        h, w = features.shape
        print(f"[diag] Image: {os.path.basename(image_path)}")
        print(f"[diag] Size: {w}×{h} px | Foreground: {int(features.sum())} px | Components: {num}")

    if num < 2:
        raise ValueError("Need at least 2 components to compute inter-feature distances. "
                         "Adjust threshold/white_as_feature or try connectivity=1.")

    # --- Boundaries ---
    points, owners, label_to_indices = build_boundary_points(labels, num)
    if diagnostics:
        print(f"[diag] Boundary points: {points.shape[0]}")
        labs_present = sorted(label_to_indices.keys())
        print(f"[diag] Labels present: {labs_present}")

    if points.shape[0] == 0:
        raise RuntimeError("Boundary extraction returned no points. "
                           "Try a gentler erosion kernel or fallback to component pixels.")

    # --- Pairwise computations ---
    rows = pairwise_min_edge_distances(points, owners, label_to_indices, tol=1e-12)

    # --- Save pairwise CSV ---
    base = os.path.splitext(os.path.basename(image_path))[0]
    pairwise_path = os.path.join(out_dir, f"{base}_pairwise_min_distances.csv")
    with open(pairwise_path, "w", newline="") as f:
        writer = csv.writer(f)
        header = ["label_i","label_j","min_dist_px","min_dist_phys_mum","tie_count",
                  "p_row","p_col","q_row","q_col","p_index","q_index"]
        writer.writerow(header)
        for r in rows:
            d_phys = (r['min_dist_px'] * float(pixel_size)) if pixel_size is not None else ""
            writer.writerow([r['label_i'], r['label_j'],
                             f"{r['min_dist_px']:.6f}",
                             f"{d_phys:.6f}" if d_phys != "" else "",
                             r['tie_count'],
                             f"{r['p_row']:.3f}", f"{r['p_col']:.3f}",
                             f"{r['q_row']:.3f}", f"{r['q_col']:.3f}",
                             r['p_index'], r['q_index']])

    # --- Save per-component nearest neighbor CSV ---
    nn_rows = reduce_to_nearest_neighbor(rows, pixel_size=pixel_size)
    nn_path = os.path.join(out_dir, f"{base}_nearest_neighbor.csv")
    with open(nn_path, "w", newline="") as f:
        writer = csv.writer(f)
        header = ["label","nearest_label","min_dist_px","min_dist_phys_mum","p_row","p_col","q_row","q_col"]
        writer.writerow(header)
        for r in nn_rows:
            writer.writerow([
                r['label'], r['nearest_label'],
                f"{r['min_dist_px']:.6f}",
                f"{r['min_dist_phys_mum']:.6f}" if r['min_dist_phys_mum'] is not None else "",
                f"{r['p_row']:.3f}" if r['p_row'] is not None else "",
                f"{r['p_col']:.3f}" if r['p_col'] is not None else "",
                f"{r['q_row']:.3f}" if r['q_row'] is not None else "",
                f"{r['q_col']:.3f}" if r['q_col'] is not None else "",
            ])

    # --- Optional: Save an NxN matrix CSV ---
    matrix_path = None
    if write_matrix:
        labels_sorted, M = build_distance_matrix(rows)
        matrix_path = os.path.join(out_dir, f"{base}_distance_matrix.csv")
        with open(matrix_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["label"] + labels_sorted)
            for i, li in enumerate(labels_sorted):
                row = [li] + [("" if math.isnan(x) else f"{x:.6f}") for x in M[i]]
                writer.writerow(row)

    # --- Plot shortest distances & label features ---
    overlay_path = os.path.join(out_dir, f"{base}_shortest_pairs.png")
    overlay_path = plot_shortest_feature_distances(
        features_bool=features,
        labels=labels,
        pairwise_rows=rows,
        pixel_size=pixel_size,
        top_k=top_k_plot,
        max_dim=plot_max_dim,
        figsize=figsize,
        dpi=dpi,
        out_path=overlay_path,
        annotate_all_components=annotate_all_components,
        text_size=text_size,
        line_width=line_width
    )

    return {
        "pairwise_csv": pairwise_path,
        "nearest_neighbor_csv": nn_path,
        "matrix_csv": matrix_path,
        "overlay_png": overlay_path,
        "num_components": num,
        "num_pairs": len(rows),
        "boundary_points": int(points.shape[0])
    }

#%% Analyse pictures

summary = compute_and_save_all_min_distances(
    image_path=image_path,
    out_dir=out_dir,
    pixel_size= 1/1.84,          # e.g., 0.5 for 0.5 µm/pixel, for 5x magnification with the used microscope
    white_as_feature=True,    # set False if features are black
    connectivity=2,           # 2=8-neighborhood, 1=4-neighborhood
    threshold=128,
    diagnostics=True,
    write_matrix=True
)

print(summary)















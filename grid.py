unique_x = np.unique(x_vals)
unique_y = np.unique(y_vals)

is_grid = len(x_vals) == len(unique_x) * len(unique_y)

if is_grid and len(unique_x) > 1 and len(unique_y) > 1:
    # ✅ Surface (valid case)
    fig.add_trace(go.Surface(...))
else:
    # 🔥 Fallback → Scatter3D
    fig.add_trace(go.Scatter3d(
        x=x_vals,
        y=y_vals,
        z=z_vals,
        mode='markers+lines',
        marker=dict(size=4)
    ))
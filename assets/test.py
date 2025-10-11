def barchart3D(x_vals, y_vals, z_vals, title, z_title, x_title, y_title,
               color='royalblue', opacity=1):
    import numpy as np
    import plotly.graph_objects as go

    fig, ann = go.Figure(), []

    # 🔹 Force numeric types (x as int, y/z as float)
    x_vals = np.array(x_vals, dtype=int)
    y_vals = np.array(y_vals, dtype=float)
    z_vals = np.array(z_vals, dtype=float)

    # 🔹 Compute spacing (avoid 0 division)
    dx = np.min(np.diff(np.unique(x_vals))) * 0.4 if len(np.unique(x_vals)) > 1 else 1.0
    dy = np.min(np.diff(np.unique(y_vals))) * 0.4 if len(np.unique(y_vals)) > 1 else 1.0
    dx, dy = max(dx, 1e-6), max(dy, 1e-6)

    for i, z_max in enumerate(z_vals):
        x_cnt, y_cnt = x_vals[i], y_vals[i]
        x_min, x_max = x_cnt - dx/2, x_cnt + dx/2
        y_min, y_max = y_cnt - dy/2, y_cnt + dy/2
        x = [x_min, x_min, x_max, x_max, x_min, x_min, x_max, x_max]
        y = [y_min, y_max, y_max, y_min, y_min, y_max, y_max, y_min]
        z = [0, 0, 0, 0, z_max, z_max, z_max, z_max]

        # 🔹 Solid color bar (no gradient)
        fig.add_trace(go.Mesh3d(
            x=x, y=y, z=z,
            alphahull=0,
            color=color,
            showscale=False,
            opacity=opacity,
            hoverinfo='skip'
        ))

        # Transparent hover plane
        fig.add_trace(go.Mesh3d(
            x=[x_min, x_max, x_max, x_min],
            y=[y_min, y_min, y_max, y_max],
            z=[z_max, z_max, z_max, z_max],
            color='rgba(0,0,0,0)',
            opacity=0.01,
            hovertemplate=(
                f"<b>{x_title}</b>: {x_cnt}<br>"
                f"<b>{y_title}</b>: {y_cnt:.2f}<br>"
                f"<b>{z_title}</b>: {z_max:.2f}<extra></extra>"
            ),
            hoverlabel=dict(
                bgcolor='rgba(30,30,30,0.8)',
                font_color='white',
                bordercolor='white'
            ),
            showlegend=False
        ))

        # Annotation
        ann.append(dict(
            showarrow=False,
            x=x_cnt, y=y_cnt, z=z_max,
            text=f'{z_max:.2f}',
            font=dict(color='white', size=10),
            bgcolor='rgba(0,0,0,0.3)',
            xanchor='center', yanchor='middle'
        ))

    # 🔹 Force integer tick labels on x-axis
    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor='center', yanchor='top'),
        scene=dict(
            xaxis=dict(
                title=x_title,
                tickmode='array',
                tickvals=x_vals,
                ticktext=[str(int(v)) for v in x_vals],
                title_font=dict(size=10),
                tickfont=dict(size=10),
            ),
            yaxis=dict(
                title=y_title,
                title_font=dict(size=10),
                tickfont=dict(size=10),
            ),
            zaxis=dict(
                title=z_title,
                title_font=dict(size=10),
                tickfont=dict(size=10),
            ),
            annotations=ann,
        ),
        hoverlabel=dict(
            bgcolor='rgba(50,50,50,0.8)',
            font_color='white',
            bordercolor='white'
        )
    )

    return fig

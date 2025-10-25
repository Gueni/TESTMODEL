def write_html_report(html_file, plots, base64_img, script_name, date, UTC, iterSplit=False, parameters_dict=None):
    """Export interactive Plotly figures to a styled HTML report using template."""
    
    # Convert plots to HTML
    plot_items = ""
    
    if iterSplit:
        # 2 figures per row layout
        plot_items += '<div class="plot-grid-2col">\n'
        for fig in plots:
            # Set figure height for consistency
            fig.update_layout(height=500, margin=dict(t=50, b=50, l=50, r=50))
            fig_html = to_html(fig, include_plotlyjs='cdn', full_html=False, div_id=f"plot-{hash(fig)}")
            plot_items += f'<div class="plot-grid-item">{fig_html}</div>\n'
        plot_items += '</div>\n'
    else:
        # 1 figure per row layout
        plot_items += '<div class="plot-container">\n'
        for i, fig in enumerate(plots):
            # Set figure height for consistency
            fig.update_layout(height=500, margin=dict(t=50, b=50, l=50, r=50))
            fig_html = to_html(fig, include_plotlyjs='cdn', full_html=False, div_id=f"plot-{i}")
            plot_items += f'<div class="plot-item">{fig_html}</div>\n'
        plot_items += '</div>\n'
    
    # Use the template approach
    populate_html_template_with_base64(
        template_path="HTML_REPORT_TEMPLATE.html",
        output_path=html_file,
        script_name=script_name,
        date_time=date,
        simulation_id=UTC,
        logo_base64=base64_img,
        plot_items=plot_items,
        parameters_dict=parameters_dict
    )
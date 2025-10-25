# Your original approach adapted for templates
plot_items = ""

for i in range(len(figures)):
    # Add the plot
    plot_items += figures[i].to_html(full_html=False, include_plotlyjs=False)
    
    # Add comment if conditions are met
    if dp.JSON["figureName"] and dp.JSON["figureComment"]:
        if not comments[i] == " ":
            plot_items += f'<input type="text" class="comment-box" value="{comments[i]}" readonly="readonly">'
    
    # Add separator (you can style this in CSS)
    plot_items += '<div class="separator"></div>'

# Then pass plot_items to your template
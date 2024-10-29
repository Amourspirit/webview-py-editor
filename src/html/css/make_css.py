from pygments.formatters import HtmlFormatter

# Generate CSS styles
formatter = HtmlFormatter()
css_styles = formatter.get_style_defs(".highlight")

# Save the CSS styles to a file
with open("pygments_styles.css", "w") as f:
    f.write(css_styles)

# Print the CSS styles (for demonstration purposes)
print(css_styles)

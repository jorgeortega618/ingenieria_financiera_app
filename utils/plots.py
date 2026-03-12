import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

# Set default template to plotly for a cleaner native look
pio.templates.default = "plotly"

def apply_custom_theme(fig):
    """
    Applies custom styling for a professional and corporate
    financial look matching Streamlit's native light/dark mode.
    """
    fig.update_layout(
        font=dict(family="Inter, sans-serif"),
        margin=dict(l=40, r=40, t=60, b=40),
        title_font=dict(size=20, family="Inter, sans-serif", color="#1e3a8a"),
        hoverlabel=dict(
            font_size=14,
            font_family="Inter, sans-serif"
        )
    )
    return fig

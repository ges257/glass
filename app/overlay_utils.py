"""
Overlay rendering utilities for GLASS demo.
Draws column boundary lines on PDF page images.
"""

from PIL import Image, ImageDraw, ImageFont


def draw_column_overlay(image: Image.Image, columns: list, table_y_start: float = 0.18, table_y_end: float = 0.95) -> Image.Image:
    """
    Draw column boundary overlay on a PDF page image.

    Args:
        image: PIL Image of the PDF page
        columns: List of column dicts with x_start, x_end, name
        table_y_start: Normalized Y start of table region (0-1)
        table_y_end: Normalized Y end of table region (0-1)

    Returns:
        Image with column overlays drawn
    """
    img = image.copy()
    draw = ImageDraw.Draw(img, 'RGBA')

    width, height = img.size
    y_top = int(table_y_start * height)
    y_bottom = int(table_y_end * height)

    # Colors for alternating columns (semi-transparent)
    colors = [
        (168, 139, 250, 40),   # Purple
        (59, 130, 246, 40),    # Blue
    ]

    for i, col in enumerate(columns):
        x_start = int(col['x_start'] * width)
        x_end = int(col['x_end'] * width)

        # Draw filled rectangle
        color = colors[i % 2]
        draw.rectangle([x_start, y_top, x_end, y_bottom], fill=color)

        # Draw boundary lines
        line_color = (168, 139, 250, 180)  # Purple, more opaque
        draw.line([(x_start, y_top), (x_start, y_bottom)], fill=line_color, width=2)
        draw.line([(x_end, y_top), (x_end, y_bottom)], fill=line_color, width=2)

    return img


def create_column_annotations(columns: list, image_width: int, image_height: int,
                               table_y_start: float = 0.18, table_y_end: float = 0.95) -> list:
    """
    Create annotation rectangles for streamlit-image-annotation.

    Args:
        columns: List of column dicts with x_start, x_end, name
        image_width: Width of the image in pixels
        image_height: Height of the image in pixels
        table_y_start: Normalized Y start of table region (0-1)
        table_y_end: Normalized Y end of table region (0-1)

    Returns:
        List of annotation dicts in streamlit-image-annotation format
    """
    y_top = int(table_y_start * image_height)
    y_bottom = int(table_y_end * image_height)

    annotations = []
    for col in columns:
        annotations.append({
            "left": int(col['x_start'] * image_width),
            "top": y_top,
            "width": int((col['x_end'] - col['x_start']) * image_width),
            "height": y_bottom - y_top,
            "label": col['name']
        })

    return annotations


def annotations_to_template(annotations: list, image_width: int, columns: list) -> list:
    """
    Convert streamlit-image-annotation rectangles back to normalized template format.

    Args:
        annotations: List of annotation dicts from the component
        image_width: Width of the image in pixels
        columns: Original columns list (to preserve data_type and order)

    Returns:
        Updated columns list with new boundaries
    """
    # Sort annotations by x position
    sorted_anns = sorted(annotations, key=lambda a: a['left'])

    updated_columns = []
    for i, ann in enumerate(sorted_anns):
        x_start = ann['left'] / image_width
        x_end = (ann['left'] + ann['width']) / image_width

        # Find matching column by label or use index
        original = columns[i] if i < len(columns) else {'data_type': 'text'}

        updated_columns.append({
            'name': ann.get('label', f'Column {i+1}'),
            'x_start': round(x_start, 3),
            'x_end': round(x_end, 3),
            'data_type': original.get('data_type', 'text')
        })

    return updated_columns

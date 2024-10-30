# Image_creation_from_df.py

import random
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
import matplotlib.colors as mcolors
from matplotlib.font_manager import FontProperties


class ColorfulTableGenerator:
    def __init__(self, data, font_size=12, scale=1.2, output_file="colorful_table.png", fixed_colors=None):
        """
        Initialize the table generator with customization options.
        
        Parameters:
        - data: pandas DataFrame or dictionary to convert to DataFrame
        - font_size: int, the font size of the text in the table
        - scale: float, the scaling factor for the table size
        - output_file: str, the name of the output PNG file
        - fixed_colors: dict, specifies the color for certain columns. 
                        Example: {0: (0, 122, 255), 1: (0, 0, 0)}
        """
        self.data = pd.DataFrame(data, index=None) if isinstance(data, dict) else data
        self.font_size = font_size
        self.scale = scale
        self.output_file = output_file
        self.fixed_colors = fixed_colors if fixed_colors else (1,1,1)

    def _prepare_data(self):
        """Convert lists in each cell to strings for display in the table."""
        self.data = self.data.applymap(
            lambda x: "\n".join(map(str, x)) if isinstance(x, list) else str(x)
        )

    def generate_colorful_table(self):
        """Generate and save a colorful table as a PNG file."""
        # Prepare the data for display
        self._prepare_data()

        # Calculate column widths based on the maximum length of the content in each column
        col_widths = [max(self.data[col].astype(str).map(len).max(), len(str(col))) for col in self.data.columns]
        col_widths = [col_widths[0] * 0.018, col_widths[1] * 0.019, col_widths[2] * 0.019, col_widths[3] * 0.021]
        # col_widths = [width * 0.02 for width in col_widths]  # Scale to appropriate figure size
        # print(col_widths)
        
        # col_widths = [0.48, 0.30]
        # # col_widths = [col_widths[0] * 0.017, col_widths[1] * 0.02]
        # print(type(col_widths))
        # print((col_widths))
        # col_widths =[0.46, 0.28]
        # Set font properties
        font_prop_col_head = FontProperties(family="Arial", weight="bold", size=13)
        font_prop_except_col_head = FontProperties(family="Arial")

        # Plot setup
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.axis("off")  # Turn off the axis

        # Create table in plot with custom font and background
        table_obj = table(ax, self.data, loc="center", cellLoc="center", colWidths=col_widths, rowLabels=None)
        table_obj.auto_set_font_size(False)
        table_obj.set_fontsize(self.font_size)
        table_obj.scale(self.scale, self.scale)

        # Customize cell colors based on column index
        for (row, col), cell in table_obj.get_celld().items():
            if col == 3:
                cell.set_edgecolor("none")
            else:
                cell.set_edgecolor("none")
            # cell.set_text_props(color="white" if key[1] in self.fixed_colors else "black")
            if row == 0:  
                cell.set_text_props(fontproperties=font_prop_col_head, ha='left')  # Bold Arial, left-aligned headers
                cell.set_text_props(color = (0.65234375, 0.13671875, 0.171875))
                cell.set_facecolor(color='white')

            else:
                cell.set_text_props(fontproperties=font_prop_except_col_head, ha='left')
                cell.set_text_props(color="white")
                cell.set_facecolor(self.fixed_colors)

        # Add dark red line below the first row
        # first_row_bottom = 0.9 - 0.1 * self.scale  # Position based on scale
        # first_row_bottom = 0.1
        # ax.plot(
        #     [0.05, 0.95],  # Line start and end positions (horizontal)
        #     [first_row_bottom, first_row_bottom],  # Vertical position for the line
        #     color="darkred",
        #     linewidth=2
        # )

        # Save as PNG
        plt.savefig(self.output_file, bbox_inches="tight", dpi=300)
        plt.close()
        print(f"Colorful DataFrame saved as {self.output_file}")
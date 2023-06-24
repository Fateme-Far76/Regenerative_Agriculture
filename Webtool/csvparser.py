import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import random
import seaborn as sns 

def organic_compund(df):
    grouped_df = df.groupby(['Eenheid'])
    percentage_df = grouped_df.get_group('%')
    percentage_df['Resultaat.1'] = percentage_df['Resultaat.1'].str.replace(',', '.')
    percentage_df['Resultaat.1'] = percentage_df['Resultaat.1'].astype(float)

    # Calculate the cumulative percentage
    percentage_df['Cumulative_Percentage'] = percentage_df['Resultaat.1'].cumsum()

    # Calculate the remaining percentage
    remaining_percentage = 100 - percentage_df['Cumulative_Percentage'].iloc[-1]

    # Add 'Other' category with the remaining percentage if applicable
    if remaining_percentage > 0:
        percentage_df = percentage_df.append({'Mineral': 'Other',
                                            'Resultaat.1': remaining_percentage},
                                            ignore_index=True)

    num_colors = len(percentage_df) - 1
    colors = sns.color_palette('husl', n_colors=num_colors).as_hex()

    # Shuffle the colors
    random.shuffle(colors)

    # Assign white color specifically to 'Other' category
    colors.append('white')

    # Plot the rectangle box with colored segments and text annotations
    fig, ax = plt.subplots()
    x = 0
    y = 0
    width = 100
    height = 100

    for i in range(len(percentage_df)):
        percentage = percentage_df['Resultaat.1'].iloc[i]
        color = colors[i]
        rect = Rectangle((x, y), width, (height * percentage) / 100, facecolor=color, edgecolor='black')
        ax.add_patch(rect)

        annotation = f'{percentage_df["Mineral"].iloc[i]}: {percentage}%'

        ax.annotate(annotation, xy=(x + width / 2, y + (height * percentage) / 200),
                    xytext=(0, 0), textcoords='offset points', ha='center', va='center')
        y += (height * percentage) / 100

    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    plt.axis('off')  # Hide axis
    plt.title('Organic compound', loc='left')
    plt.savefig('static/plot1.png')
    plt.close()


def pH(df):
    
    # Searching for 'pH' in the 'Mineral' column
    pH_row = df['Mineral'].str.contains('(pH)')

    # Retrieving the number from the same row where 'pH' is found
    pH = df.loc[pH_row, 'Resultaat.1'].values[0]

    pH = pH.replace(',', '.')

    # Convert to a numeric value
    pH_value = float(pH)

    # pH values and corresponding colors
    pH_values = [i for i in range(15)]
    colors = ['red', 'tomato', 'orange', 'yellow', 'palegreen', 'greenyellow', 'lawngreen', 'limegreen', 'lime',
            'aqua', 'cornflowerblue', 'royalblue', 'slateblue', 'blueviolet', 'indigo']

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Set the size and position of the rectangle
    rect_width = 1
    rect_height = 1
    rect_x = 0
    rect_y = 0

    # Iterate over the pH values and colors to draw rectangles
    for i in range(len(pH_values)):
        rect_color = colors[i]
        rect = plt.Rectangle((rect_x, rect_y), rect_width, rect_height, color=rect_color)
        ax.add_patch(rect)
        rect_x += rect_width

    # Set the x-axis and y-axis limits
    ax.set_xlim(0, rect_x)
    ax.set_ylim(rect_y, rect_y + rect_height)

    # Add an arrow and text annotation for the pH value
    arrow_x = pH_value
    arrow_y = rect_y + rect_height
    ax.annotate(str(pH_value), xy=(arrow_x, arrow_y), xytext=(arrow_x, arrow_y + 0.08),
                arrowprops=dict(arrowstyle='->'))

    plt.yticks([0, 1])

    # Add labels
    plt.xlabel('pH')

    plt.savefig('static/plot2.png')
    plt.close()



def csvparser(): 
    
    # Read the uploaded CSV file into a DataFrame
    df = pd.read_csv('csv_output.csv',encoding='ISO-8859-1')
    df = df.dropna(axis=1, how='all')
    df = df.dropna(thresh=2).reset_index(drop=True) 

    grouped_df = df.groupby('Resultaat', sort=True)
    first_group_name = list(grouped_df.groups.keys())[0]
    df['Resultaat'] = df['Resultaat'].fillna(first_group_name) 

    return df


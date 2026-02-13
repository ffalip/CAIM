import matplotlib.pyplot as plt
import seaborn as sns
import re

# Function to read and parse the file
def parse_file(file_path):
    category_data = {}
    current_category = None

    # Regular expression to match lines containing category and similarity
    category_pattern = re.compile(r'-----------------(.*?)-------------------')
    similarity_pattern = re.compile(r'Similarity = ([0-9.]+)')

    with open(file_path, 'r') as file:
        for line in file:
            # Check for category
            category_match = category_pattern.search(line)
            if category_match:
                current_category = category_match.group(1)
                if current_category not in category_data:
                    category_data[current_category] = []
            else:
                # Check for similarity value
                similarity_match = similarity_pattern.search(line)
                if similarity_match:
                    similarity_value = float(similarity_match.group(1))
                    category_data[current_category].append(similarity_value)
    
    return category_data

# Function to extract the main category from category.subcategory.name
def extract_main_category(full_category):
    return full_category.split('.')[0]

# Function to create the boxplot with different colors for each main category
def create_boxplot(category_data):
    # Sort categories alphabetically
    sorted_categories = sorted(category_data.keys())

    # Extract main categories
    main_categories = [extract_main_category(cat) for cat in sorted_categories]

    # Get unique main categories and assign a color to each
    unique_main_categories = sorted(set(main_categories))
    palette = sns.color_palette("husl", len(unique_main_categories))  # Generate colors
    color_map = {main_cat: palette[i] for i, main_cat in enumerate(unique_main_categories)}
    
    # Prepare data for plotting
    data = []
    categories = []
    colors = []
    for category in sorted_categories:
        similarities = category_data[category]
        main_category = extract_main_category(category)
        data.extend(similarities)
        categories.extend([category] * len(similarities))
        colors.extend([color_map[main_category]] * len(similarities))
        print(main_category)
    print(colors)
        
    colors2 = [palette[0], palette[1], palette[1], palette[1], palette[1], palette[1], palette[2], palette[3], palette[3], palette[3], palette[3], palette[4], palette[4], palette[4], palette[4], palette[5], palette[6], palette[6], palette[6], palette[6]  ]
    # Create the boxplot without outliers, with colors by main category
    plt.figure(figsize=(14, 6))
    sns.boxplot(x=categories, y=data, palette=colors2, showfliers=False)  # Disable outliers
    plt.xlabel('Temàtica')
    plt.ylabel('Similitud cosinus')
    plt.title('Similitud entre el fitxer 0001566 i diferents fitxers de diferents temàtiques')
    plt.xticks(rotation=50)  # Rotate category labels if needed
    plt.tight_layout()
    legend_labels = ['alt', 'comp', 'misc', 'rec', 'sci', 'talk']
    handles = [plt.Line2D([0], [0], color=palette[i], lw=4) for i in range(len(palette))]
    plt.legend(handles, legend_labels, loc='upper right') 
    plt.show()

# Example usage
file_path = 'dataRes.txt'  # Replace with your file path
category_data = parse_file(file_path)
create_boxplot(category_data)


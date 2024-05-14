def json_visualizer(file: str, create_file: bool) -> str:
    '''
    Converts JSON into graphical flow chart

    This function takes a JSON file and returns (and optionally creates) an HTML document with SVG elements inside it

    Args:
        file (str) = file name with extension (ex: data.json)
        create_file (bool) = Should the HTML doc be created with the same name or not

    Returns:
        (str) = The HTML doc containing flowchart
    
    Raises:
        FileNotFoundError: If the file was not found
    '''
    # Import libraries
    from statistics import mean
    import json

    # Define functions and classes
    def json_sorter(obj, initial_string='ROOT') -> None:
        '''
        Flatten the json structure and put them into a list

        Args:
            obj (str) = variable that needs to be flattened
            initial_string (str) = Prefix showing the position of the obj

        Returns:
            None
        
        Raises:
            None
        '''
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, int) or isinstance(value, float) or isinstance(value, str) or isinstance(value, bool):
                    result = initial_string + '.' + key
                    all_items.append(result)
                else:
                    stringy = initial_string + '.' + key
                    json_sorter(value, initial_string=stringy)
        elif isinstance(obj, list):
            length = len(obj)
            extra = initial_string.split('.')[-1]
            stringy = f'{initial_string}.ARRAY__{len(obj)}__ITEMS'
            for item in obj:
                if isinstance(item, int) or isinstance(item, float) or isinstance(item, str) or isinstance(item, bool):
                    result = f'{initial_string}.ARRAY__{length}__ITEMS'
                    all_items.append(result)
                else:
                    json_sorter(item, initial_string=stringy)

    def consolidate(listy: list[str]) -> list:
        '''
        Consolidates and replaces repeated elements with one element at the centre

        Args:
            listy (list[str]) = List of elements that needs to be consolidated

        Returns:
            (list) : Same list without repititons and consolidated elements
        
        Raises:
            None
        '''
        keys = [x[0] for x in listy]
        keys_unique = []
        for key in keys:
            if key not in keys_unique:
                keys_unique.append(key)
        consolidated_list = []
        for key in keys_unique:
            x_dims = []
            y_dims = []
            for i in vals:
                if i[0] == key:
                    x_dims.append(i[1])
                    y_dims.append(i[2])
            consolidated_list.append((key, mean(x_dims), mean(y_dims)))
        return consolidated_list


    class rectangle_with_text:
        '''
        A rectangle with some text centered in it

        Attrbutes:
            RECTANGLE
            rect_x (float): Top left X coordinate of rectangle
            rect_y (float): Top left Y coordinate of rectangle
            rect_rx (float): Rounded corner X radius of rectangle
            rect_ry (float): Rounded corner Y radius of rectangle
            rect_width (float): Width of rectangle
            rect_height (float): Height of rectangle
            rect_fill (str): Color of rectangle insides
            TEXT
            text (str): Text that needs to be put inside rectangle
            text_x (float) = Top left X coordinate of rectangle
            text_y (float) = Top left Y coordinate of rectangle
            CONNECTOR
            left_connector_x (float): X coordinate of center of circle to connect to rectangle from left
            left_connector_y (float): Y coordinate of center of circle to connect to rectangle from left
            right_connector_x (float): X coordinate of center of circle to connect to rectangle from right
            right_connector_y (float): Y coordinate of center of circle to connect to rectangle from right


        Methods:
            draw (self): Returns the rectangle and text element 
        '''
        def __init__(self, text, rect_x, rect_y):
            # Text
            self.text = text.split('.')[-1]

            # Rectangle
            self.rect_x = rect_x
            self.rect_y = rect_y
            self.rect_rx = 10
            self.rect_ry = 10
            self.rect_width = self.rect_rx + len(self.text) * 8 + self.rect_ry
            self.rect_height = 50
            self.rect_fill = '#141E46'

            # Text
            self.text_x = self.rect_x + (self.rect_width - len(self.text) * 8)/2
            self.text_y = self.rect_y + int(self.rect_height*0.6)

            # Connector
            self.left_connector_x = self.rect_x
            self.left_connector_y = self.rect_y + self.rect_height/2
            self.right_connector_x = self.rect_x + self.rect_width
            self.right_connector_y = self.left_connector_y

        def draw(self):
            self.rect_width = self.rect_rx + len(self.text) * 8 + self.rect_ry
            self.right_connector_x = self.rect_x + self.rect_width

            if self.text[-7:] == '__ITEMS':
                draw_rect = f'<rect x="{self.rect_x}" y="{self.rect_y}" width="{self.rect_width}" height="{self.rect_height}" rx="{self.rect_rx}" ry="{self.rect_ry}" fill="{self.rect_fill}" stroke="#f07171" stroke-width="4"/>'
            else:
                draw_rect = f'<rect x="{self.rect_x}" y="{self.rect_y}" width="{self.rect_width}" height="{self.rect_height}" rx="{self.rect_rx}" ry="{self.rect_ry}" fill="{self.rect_fill}" />'
            draw_text = f'<text x="{self.text_x}" y="{self.text_y}" style="fill: #8DECB4;">{self.text}</text>'
            draw_left_connector = f'<circle cx="{self.left_connector_x}" cy="{self.left_connector_y}" r="5" fill="#41B06E"/>'
            draw_right_connector = f'<circle cx="{self.right_connector_x}" cy="{self.right_connector_y}" r="5" fill="#41B06E"/>'
            return draw_rect + '\n' + draw_text + '\n' + draw_left_connector + '\n' + draw_right_connector

    def draw_quadratic_curve(stringy: str) -> str:
        '''
        Draws the connector

        Args:
            stringy (str) = What to connect (ex: 'start_element.end_element')

        Returns:
            (str) : Quadratic path element
        
        Raises:
            None
        '''
        start, end = stringy.split('<->')
        start_x = rectangle_instances[start].right_connector_x
        start_y = rectangle_instances[start].right_connector_y
        end_x = rectangle_instances[end].left_connector_x
        end_y = rectangle_instances[end].left_connector_y

        control_in_x = (start_x + end_x)*0.5
        control_in_y = start_y

        control_out_x = (start_x + end_x)*0.5
        control_out_y = end_y

        return f'<path d="M{start_x},{start_y} C {control_in_x},{control_in_y}, {control_out_x},{control_out_y}, {end_x},{end_y}" stroke="#41B06E" stroke-width="2" fill="none"/>'

    def get_paths(stringy: str) -> list[str]:
        '''
        Produces sub strings of the main string

        Args:
            stringy (str) = What to connect (ex: 'start.in_between.in_between.in_between.end')

        Returns:
            (list) : List of all paths in the main path
        
        Raises:
            None
        '''
        splitted_list = stringy.split('.')
        answer = []
        for i in range(1, len(splitted_list)):
            start_list = splitted_list[:i]
            end_list = splitted_list[:i+1]
            p = f"{'.'.join(start_list)}<->{'.'.join(end_list)}"
            answer.append(p)
        return answer


    # Read data
    with open(file, 'r') as f:
        data = json.load(f)
    
    # Flatten JSON
    all_items = []
    json_sorter(data)

    # Get unique items
    all_unique_items = []
    for x in all_items:
        if x not in all_unique_items:
            all_unique_items.append(x)

    # Calculate max depth
    max_length = 0
    for item in all_unique_items:
        splitted_list = item.split('.')
        max_length = max(max_length, len(splitted_list))

    # Normalise all items by adding .NULL and make everything reach same depth
    all_items_normalised = []
    for item in all_unique_items:
        splitted_list = item.split('.')
        nulls_to_add = max_length - len(splitted_list)
        if nulls_to_add:
            stringy = item + '.NULL'*nulls_to_add
        else:
            stringy = item
        all_items_normalised.append(item + '.NULL'*nulls_to_add)

    # Matrix type dimensioning
    matrix_cols = max_length
    matrix_rows = len(all_items_normalised)
    length_dict = {x:0 for x in range(matrix_cols)}
    for item in all_items_normalised:
        splitted_list = item.split('.')
        for i in range(matrix_cols):
            length_dict[i] = max(length_dict[i], len(splitted_list[i]))
    x_dim_dict = {0:10}
    for i in range(1, matrix_cols):
        x_dim_dict[i] =  x_dim_dict[i-1] + length_dict[i-1]*8 + 100
    y = list(range(10, 60*matrix_rows, 60))
    y_dim_dict = {i:y[i] for i in range(matrix_rows)}

    # Create arrays in matrix structure
    final_array = []
    for i in range(matrix_rows):
        items = all_items_normalised[i].split('.')
        array = []
        for j in range(len(items)):
            full_name = '.'.join(items[:j+1])
            array.append((full_name, x_dim_dict[j], y_dim_dict[i]))
        final_array.append(array)

    # Remove repitions and consolidate
    final_consolidated_list = []
    for i in range(matrix_cols):
        vals = []
        for row in final_array:
            vals.append(row[i])
        consolidated_list = consolidate(vals)
        final_consolidated_list.extend(consolidated_list)

    # HTML data
    width = max(x_dim_dict.values()) + 200
    height = max(y_dim_dict.values()) + 60
    html_head = '''
    <!DOCTYPE html>
    <html>
        <head>
            <title>JSON Visual</title>
            <style>body {background-color: #defaea; font-family:monospace;}</style>
        </head>
        <body>
    '''
    html_head += f'\t\t<svg width="{width}" height="{height}">' 
    html_tail = '''
            </svg>
        </body>
    </html>
    '''

    # Calculate all connectors/paths
    all_paths_master = []
    for item in all_items:
        all_paths = get_paths(item)
        all_paths_master.extend(all_paths)
    all_paths_master = list(set(all_paths_master))

    # Draw
    rectangle_instances = {}
    solution = ''
    ## Head
    solution += html_head
    solution += '\n'
    ## Rectangles
    for text, rect_x, rect_y in final_consolidated_list:
        if text.split('.')[-1] != 'NULL':
            temp = rectangle_with_text(text=text, rect_x=rect_x, rect_y=rect_y)
            rectangle_instances[text] = temp
            solution += temp.draw()
            solution += '\n'
    ## Paths
    for item in all_paths_master:
        p = draw_quadratic_curve(item)
        solution += p
        solution += '\n'
    ## Tail
    solution += html_tail

    # Create File
    if create_file:
        with open(file.replace('.json', '.html'), 'w') as f:
            f.write(solution)

    # Return
    return solution
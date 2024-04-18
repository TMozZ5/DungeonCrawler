def merge_sort(numbers):
    """
    recursive function that sorts numbers from lowest to highest using a merge sort
    :param numbers: the numbers to be sorted
    :type numbers: list
    """
    if len(numbers) == 1:  # If there is only one number left in this list
        return numbers  # Return it since it cannot be halved again
    else:  # If not
        num_1 = numbers[0:len(numbers)//2]  # Slice one half of the list
        num_2 = numbers[len(numbers)//2:]  # Slice the other half
        num_1 = merge_sort(num_1)  # Sort the first half of the list recursively
        num_2 = merge_sort(num_2)  # Sort the second half of the list recursively
        for num in num_2:  # For each number in the second list
            count = -1  # This is used as the index to insert a number into the first number list
            found = False  # This is the stopping condition of the while loop and is met when the number has found
            # its place in the first list or the number is bigger than everything in the first list
            while not found:  # While its place hasn't been found
                count += 1
                if count > len(num_1) - 1:  # If the count is bigger than the length of the first list
                    num_1.append(num)  # Insert the number at the end of that list
                    found = True
                elif num < num_1[count]:  # If it is smaller than the number it is being compared to
                    num_1.insert(count, num)  # Insert it before the number it is being compared to
                    found = True
        return num_1


def find_shortest_path(new_map, start_vertex, end_vertex):
    """
    Find the shortest path from one set of coordinates to another if one exists using the A* algorithm
    :param new_map: list of map tiles with their properties and vertices
    :type new_map: list
    :param start_vertex: the start vertexes x and y coordinates
    :type start_vertex: tuple
    :param end_vertex: the end vertexes x and y coordinates
    :type end_vertex: tuple
    :return path: a list of tiles that is the path from the start vertex to the end vertex
    """
    open_vertices = []  # Initialise open list
    closed_vertices = []  # Initialise closed list
    path = []  # Initialise path list
    x, y = start_vertex  # x and y values of start vertex
    new_map[x][y].vertex.calculate_values(end_vertex)  # Calculate g, h, and f values for first vertex
    current_vertex = start_vertex  # Set the current vertex to the first vertex
    open_vertices.append(start_vertex)  # Add the first vertex to the open list
    while current_vertex != end_vertex and len(open_vertices) > 0:  # While the current vertex isn't the final vertex
        # and the open list isn't empty
        x, y = current_vertex  # x and y values of current vertex
        total_distance = new_map[x][y].vertex.g  # Update the total distance travelled (equal to the current vertex g)
        for vertex, distance in new_map[x][y].vertex.adjacent_vertices.items():  # For the vertex and the distance to it
            x, y = vertex  # Vertexes x and y values
            if vertex not in open_vertices and vertex not in closed_vertices and new_map[x][y].block_path is False \
                    and new_map[x][y].occupied is False:  # If the vertex isn't in the open or closed list
                # and the tile isn't occupied or a wall tile
                open_vertices.append(vertex)  # Add the vertex to the open list
                new_map[x][y].vertex.calculate_values(end_vertex, total_distance, distance)  # Calculate the vertexes
                # g, h, and f values
                new_map[x][y].vertex.set_parent(current_vertex)  # Set its parent to the current vertex
                # (used for re-tracing the path)
        open_vertices.remove(current_vertex)  # Remove the current vertex from the open list
        closed_vertices.append(current_vertex)  # And add it to the closed list
        lowest_f = -1  # The current lowest f value in the open list
        for vertex in open_vertices:  # For each vertex in the open list
            x, y = vertex  # Vertexes x and y values
            if new_map[x][y].vertex.f < lowest_f or lowest_f == -1:  # If the vertex has a lower f value than
                # the previous vertex with the lowest f value or the lowest f value is -1
                # meaning no lowest f value exists
                current_vertex = vertex  # Set this vertex as the current vertex
                lowest_f = new_map[x][y].vertex.f  # Set this vertexes f value to the lowest f value found

    current_path = end_vertex  # Set the first vertex in the path to the end vertex
    path.append(end_vertex)  # Add the last vertex to the path
    if len(open_vertices) == 0:  # If there are no vertices in the open list (meaning a path couldn't be found)
        return []  # Return a blank list as no path exists
    else:  # Else
        while current_path != start_vertex:  # While the current vertex isn't the start tile
            x, y = current_path  # Current vertexes x and y values
            current_path = new_map[x][y].vertex.parent  # Set the new current vertex to the vertexes parent
            path.append(current_path)  # Add the current vertex to the path
        return list(reversed(path))  # Return the path list in reverse
        # (as the path is found by backtracking from the end)

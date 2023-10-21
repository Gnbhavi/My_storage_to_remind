!pip install -r requirements.txt

# Importing the libraries
import numpy as np
import cv2
import networkx as nx 
# import matplotlib.pyplot as plt
import os


# To create a directory(for train n test n four classes) if it does not exist
def check_if_directory_exists(folder_path):
    if not os.path.exists(folder_path):
            os.makedirs(folder_path)


# To save the n_u and n_v values to a text file
def save_list_to_text_file(file_name, data_list):
    try:
        with open(file_name, 'w') as file:
            for item in data_list:
                file.write(str(item) + '\n')
        print(f"List saved to '{file_name}' successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


# To generate the neighbourhood values of u and v the soul of the code
def neighbourhood_values_generator(G):
    minimum_distances = dict(nx.shortest_path_length(G))     # To find the minimum distance between the nodes
    cardinality_of_v_neighbourhood = []
    cardinality_of_u_neighbourhood = []
    for edges_of_graph in G.edges():             # It iterates through all the edges of the graph
        the_val_u, the_val_v = [], []            # To store the set of nodes nearer to u and v
        for vertex_x_in_G in range(G.number_of_nodes()):      # It iterates through all the nodes of the graph
            if minimum_distances[edges_of_graph[0]][vertex_x_in_G] < minimum_distances[edges_of_graph[1]][vertex_x_in_G]:
                the_val_u.append(vertex_x_in_G)      # Adds to val_u if the distance of x to u is less than x to v
            elif minimum_distances[edges_of_graph[0]][vertex_x_in_G] > minimum_distances[edges_of_graph[1]][vertex_x_in_G]:
                the_val_v.append(vertex_x_in_G)     # Adds to val_v if the distance of x to v is less than x to u
        cardinality_of_v_neighbourhood.append(len(the_val_v)) 
        cardinality_of_u_neighbourhood.append(len(the_val_u))   
    return cardinality_of_u_neighbourhood, cardinality_of_v_neighbourhood


# It creates a list of neighbourhood values for all the images in the one class of dataset
def creating_dataset_for_different_classes(img_dir):
    completion_val = 0                                       # To check if 2 images are done
    n_u_all = []
    n_v_all = []
    for file in os.listdir(img_dir):
        brain_img = cv2.imread(img_dir + '/' + file, cv2.IMREAD_GRAYSCALE)
        brain_img_1 = cv2.resize(brain_img, (25, 15))       # Resizing the image to 25x15 for checkng the code
        print("brain read and resized")    # If program runs corectly then remove this n before line
        # brain_img_1 = np.int16(brain_img)     # If program runs corectly then use this line
        brain_img_1 = np.int16(brain_img_1)
        num_of_nodes = 1
        for i in brain_img_1.shape:
            num_of_nodes *= i
        print("nodes created")
        brain_img_1_column = brain_img_1.reshape(num_of_nodes)
        bright_mat = [0] * num_of_nodes
        for i, val in enumerate(brain_img_1_column):
            bright_mat[i] = np.absolute(np.subtract(brain_img_1_column, val))
        

        bright_mat = np.vstack(bright_mat)

        min_val_least = np.amin(bright_mat)
        max_val_atmost = np.amax(bright_mat)

        neigh_mat = 1 - (np.subtract(bright_mat, min_val_least)/ (max_val_atmost - min_val_least))
        neigh_mat[neigh_mat < 0.5] = 0
        neigh_mat[neigh_mat != 0]  = 1
        print("neighbourhood matrix created")   
        G = nx.from_numpy_array(neigh_mat)

        n_u, n_v = neighbourhood_values_generator(G)
        completion_val += 1     # If program runs corectly then remove this line
        if completion_val == 2:    # If program runs corectly then remove this condition  
            print("2 images done")
            break
        n_u_all.append(n_u)
        n_u_all.append(n_v)

    return n_u_all, n_v_all



if __name__ == '__main__':
    # Load the images
    img_dir = "Alzheimers_Dataset"
    target_dir = "Alzheimers_graph_valued_Dataset"
    for files in os.listdir(img_dir):       # It iterates through the train and test folders
        img_dir_tn_or_tst = img_dir + '/' + files
        target_dir_tn_or_tst = target_dir + '/' + files 
        for files_inside_tn_or_ts in os.listdir(img_dir_tn_or_tst):  # It iterates through the four classes
            print(files_inside_tn_or_ts)
            target_final = target_dir_tn_or_tst + '/' + files_inside_tn_or_ts
            check_if_directory_exists(target_final)
            print("Directory created")
            neigh_u_val, neigh_v_val = creating_dataset_for_different_classes(img_dir_tn_or_tst + '/' + files_inside_tn_or_ts)
            save_list_to_text_file(target_final + '/' + 'neigh_u_val.txt', neigh_u_val)
            save_list_to_text_file(target_final + '/' + 'neigh_v_val.txt', neigh_v_val)
    


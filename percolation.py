import numpy as np
import re
import os
#import matplotlib.pyplot as plt
#import matplotlib.cm as cm

# We will try to find a path from the lower indexes of the matrix to the higher ones
# along the first axis

# To simplify the algorithm, we add 1's to both sides of the matrix, and to the bottom

#    11111 

#  1 01111 1
#  1 01000 1
#  1 00010 1
#  1 11110 1

FOLDER_TO_LOAD = "C:/Users/d0m05do/Programs/Pruebas/Matrices"


def walk(mat, visited, i, j, height): # i, j are the actual position inside the matrix
    #### If there is no path
    if mat[i,j]:
        return None
    #### If we have already visited this cell
    if visited[i,j]:
        return None
    visited[i,j] = True
    #### If we have already found an exit
    if i == height:
        return [(i,j)]
    #### Now we move
    # Move to the front
    aux = walk(mat, visited, i+1, j, height)
    if aux:
        return [(i, j)] + aux
    # Move to the left
    aux = walk(mat, visited, i, j-1, height)
    if aux:
        return [(i, j)] + aux
    # Move to the right
    aux = walk(mat, visited, i, j+1, height)
    if aux:
        return [(i, j)] + aux
    # Move to the back
    aux = walk(mat, visited, i-1, j, height)
    if aux:
        return [(i, j)] + aux
    return None

def walk_iterative(mat, visited, ini_i, ini_j, height):
    # Set up
    mystack = list()
    mypath = list()
    mystack.append((ini_i, ini_j))
    #mypath.append((ini_i, ini_j))
    # Run
    while(len(mystack) > 0):
        i,j = mystack[len(mystack)-1]
        if not mat[i,j]:
            mypath.append((i, j))
            if not visited[i,j]:
                visited[i,j] = True
                if i == height:
                    return mypath
                mystack.append((i-1, j))
                mystack.append((i, j-1))
                mystack.append((i, j+1))
                mystack.append((i+1, j))
            else:
                mystack.pop()
                if mypath.pop() == mypath[len(mypath)-1]:
                    mypath.pop()
        else:
            mystack.pop()
    return None

def find_path(mymat):
    # First we pepare the matrix boundaries
    mymat = np.insert(mymat, 0, 1, axis=1)
    mymat = np.insert(mymat, len(mymat[0]), 1, axis=1)
    mymat = np.insert(mymat, 0, 1, axis=0)
    # Then we prepare the auxiliar matrix    
    already_visited = np.zeros(mymat.shape, dtype=bool)
    # Finally we start the process
    for j in range(1, len(mymat[0])-1):
        path = walk_iterative(mymat, already_visited, 1, j, len(mymat)-1)
        if path:
            break
    # Print path into new matrix
    newmat = np.array(mymat, dtype=float)
    if path:
        color = 3
        col_dt = 5.0 / len(path)
        for idx in path:
            newmat[idx] = color
            color = color + col_dt
    # Remove the added boundaries
    newmat = np.delete(newmat, 0, axis=0)
    newmat = np.delete(newmat, 0, axis=1)
    newmat = np.delete(newmat, len(newmat[0])-1, axis=1)
    return path, newmat

def load_matrix(filename):
    aux = list()
    with open(filename,'r') as f:
        aux = f.readlines()
    aux = [[int(j) for j in re.split('\D',i) if len(j) > 0] for i in aux if re.search('\d', i)]
    print("Loaded ",len(aux), 'x', len(aux[0]),"matrix")
    return np.array(aux)

#def plot_mat(mymat):
#    plt.imshow(mymat)
#    plt.show()

def save_results(res_file, data):
    with open(res_file, 'w') as f:
        for d in data:
            if d[1]:
                f.write("file: " + d[0] + " : Path found!\n")
            else:
                f.write("file: " + d[0] + " : Nope\n")


def main():
    res_file = os.path.join(FOLDER_TO_LOAD, "FindPath_Results.txt")
    if os.path.exists(res_file):
        os.remove(res_file)
    files_to_process = [os.path.join(FOLDER_TO_LOAD, f) for f in os.listdir(FOLDER_TO_LOAD)
                        if os.path.isfile(os.path.join(FOLDER_TO_LOAD, f))]
    results = list()
    for f in files_to_process:
        mymat = load_matrix(f)
        #print("Original Matrix:")
        #print(mymat)
        path, newmat = find_path(mymat)
        results.append((f, path))
    for r in results:
        if r[1]:
            print("Path found for the file '", r[0], "'!!")
        else:
            print("No path found for the file '", r[0], "'")
    save_results(res_file, results)


if __name__ == '__main__':
    main()

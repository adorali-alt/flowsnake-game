import numpy as np

# USEFUL FUNCTIONS

# renders the all_segments list param in 3D. 
#
# example uses: call with all segments to display generator, active segments to see states mid-way thru solving,
#    or with the segment path list to see the generator traversal path. 
#
# returns: a list. each list element is 6 doubles reping the coords of a triangular prism. 
#    the list elements are written in a typical cartesian basis, not in eisenstein-ish coords.
#    we want the output of this function to integrate with mathemetica's rendering abilities smoothly.
#
#    for example: Graphics3D[Prism[{{1, 0, 1}, {0, 0, 0}, {2, 0, 0}, {1, 2, 1}, {0, 2, 0}, {2, 2, 0}}]]

#    worked example: Graphics3D[Prism[{{-0.275,  0.5  ,  0.726}, {-1.001,  0.   ,  1.001}, {0., 0., 0.}, {-0.22495, 0.4548549, 0.7760500000000001}, {-0.9509500000000001, -0.045145100000000014, 1.05105}, {0.05005000000000001, -0.045145100000000014, 0.05005000000000001}}]]
def render_segments_3D(all_segments):
    # every triangular plane needs to be extended very slightly along its normal vector. 
    result = []

    # see app.py for explanation of these matrices
    cart_to_hex_basis = np.array([[1.1, 0, 0], [-0.55 ,1.0, -0.55], [0, 0, 1.1]]) 
    hex_to_cart_basis = np.array([[0.91, 0, 0], [0.5 ,1.0, 0.5], [0, 0, 0.91]]) 

    for s in all_segments:
        # change basis to cartesian
        segment_edges_hex = np.array(s.get_two_vectors())
        points_hex = np.array(s.get_all_coords_hex())
        segment_edges_cart = np.matmul(np.transpose(
            np.matmul(hex_to_cart_basis, np.transpose(segment_edges_hex))), cart_to_hex_basis)
        points_cart = np.matmul(np.transpose(
            np.matmul(hex_to_cart_basis, np.transpose(points_hex))), cart_to_hex_basis)

        a_cart = points_cart[0]
        b_cart = points_cart[1]
        c_cart = points_cart[2]

        # print([a_cart, b_cart, c_cart])

        norm_vect = np.cross(segment_edges_cart[0], segment_edges_cart[1]) * .1
        result.append([a_cart, b_cart, c_cart, 
            [sum(x) for x in zip(a_cart, norm_vect)], 
            [sum(x) for x in zip(b_cart, norm_vect)], 
            [sum(x) for x in zip(c_cart, norm_vect)]])

    # print(result)
    return result
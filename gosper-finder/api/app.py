import os
import game_state_manager
from flask import (
    Flask, render_template, redirect, url_for, request, make_response, Blueprint
)
from wolframclient.language import wl
from wolframclient.evaluation import SecuredAuthenticationKey, WolframCloudSession
import numpy as np


bp = Blueprint('generate', __name__, url_prefix='/')

manager = None

def create_app(test_config=None):
    # create and configure the app
    # creates Flask instance
    app = Flask(__name__, instance_relative_config=True)
    # override SECRET_KEY with random
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(bp)
    app.add_url_rule('/', view_func=appMounted)

    return app


@bp.route("/model", methods=['GET', 'POST'])
def appMounted():
    list_of_flags_renderable = []
    manager = None
    if request.method == 'POST' and request.form['numFlags'] is not None:
        try:

            # start wolfram client 
            sak = GenerateSecuredAuthenticationKey["pythonclientlibrary"]
            sak["ConsumerKey"]      # "T2ghIEhpISDinIw="
            sak["ConsumerSecret"]   # "VGhhdCdzIE1ZIHNlY3JldCE="
            sak = SecuredAuthenticationKey(
                'T2ghIEhpISDinIw=',
                'VGhhdCdzIE1ZIHNlY3JldCE=')

            session = WolframCloudSession(credentials=sak)
            session.start()
            assert session.authorized()

            manager = game_state_manager.GameStateManager(int(request.form['numFlags']))
            manager.auto_solve()

            # Getting a bit confused here, accidentally turning the path into a renderable object of hard vectors, 
            # when the real goal  is to render some output string in l - system format into a matching 3D object.
            # The rendered auto_solve base path will be valuable for debugging! However the ultimate goal of rep-tiling needs more thought and planning. 
            # The input to the following code should be either a string in l-system format (if wal can handle that), 
            # or else a list of vectors that have been derived from said l-system-formatted string.
            #    * note, replace vectors with triangular prisms. 
            # Basically I need an l-system formatted string before I can proceed. That string might need more pre-processing too for wal to render. 


            # Debugging note: take a tetrahedral disphenoid and cut it in half. the following are measurements of a right triangular slice
            # opp length = 1/2
            # hyp length = 13/16
            # refer: https://www.statlect.com/matrix-algebra/change-of-basis
            cart_to_hex_basis = np.array([[1.1, 0, 0], [-0.55 ,1.0, -0.55], [0, 0, 1.1]]) 
            hex_to_cart_basis = np.array([[0.91, 0, 0], [0.5 ,1.0, 0.5], [0, 0, 0.91]]) 
            
            all_hex_vectors = list(map(lambda line: line.to_vector(), manager.get_selected_path_stack()))
            all_cart_vectors = numpy.matmul(numpy.matmul(hex_to_cart_basis, all_hex_vectors), cart_to_hex_basis)


            # https://mathematica.stackexchange.com/questions/143214/l-system-in-mathematica
            # https://mathematica.stackexchange.com/questions/256431/how-to-use-vectorangle-in-anglepath3d
            # https://reference.wolfram.com/language/ref/Graphics3D.html


            for i in range(len(all_cart_vectors) - 1):
                # Graphics[ Line@AnglePath3D@StringCases[str, {"A" -> {1, 0, 0}, "B" -> {0, Pi/2, 0}, "+" -> {0, -Pi/2, 0}}]]
                # 
                # 
                # path = AnglePath3D[N@ConstantArray[EulerAngles[RotationMatrix[{all_cart_vectors[i],all_cart_vectors[i + 1]}]], 5], {"Position", "RotationTranslation"}] 
                # path = AnglePath3D[N@ConstantArray[{all_cart_vectors[i],all_cart_vectors[i + 1]}, 5], {"Position", "RotationTranslation"}] 

            # finally below is example rotating the local frame by Euler angles x, y, z° with respect to each axis, n times
            r = session.evaluate(wl.Graphics3D[wl.Tube[wl.AnglePath3D[wl.ConstantArray[{100. °, 100. °, 100. °}, 20]]], wl.Boxed -> False]) 
            print(r)

            # ultimately deposit the file in the wl cloud, only return response code 

            print("done !")
        except Exception as inst:
            print(type(inst))    # the exception type
            print(inst.args)     # arguments stored in .args
            print(inst)
    
    return render_template('game_state.html', sample={
        "flags":list_of_flags_renderable
        }
    )

# @bp.route('/segSelected', methods=['POST'])
# def segSelected():
#     try:
#         old_next_options = manager.valid_next_options()
#         nextFlagOptions = manager.handle_seg_selection(request.form['flag'], request.form['segType'])
#         new_next_options = manager.valid_next_options()
#     except InvalidInputError as invalid_input:
#         # todo tell the user their choice was invalid
#         print(type(inst))    # the exception type
#         print(inst.args)     # arguments stored in .args
#         print(inst)

#     return render_template('game_state.html', sample={"author_name": author_name.title(), "speech": speech})


app = create_app()


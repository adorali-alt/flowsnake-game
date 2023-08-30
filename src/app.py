from collections import deque
import generator_flag_graph
from flask import (
    Flask, render_template, redirect, url_for, request, make_response
)

bp = Blueprint('generate', __name__, url_prefix='/')

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
    app.add_url_rule('/', endpoint='game_state')

    return app


@app.route("/", methods=['POST'])
def appMounted():
    list_of_flagss = set_up_game(request.form['numFlags'])
    
    resp = make_response('{"response": '+nextFlagOptions+'}')
    resp.headers['Content-Type'] = "application/json"
    return render_template('game_state.html', message='')


@app.route('/segSelected', methods=['POST'])
def segSelected():
    message = None
    if generatorFlagGraph is not None:
        flag = request.form['flag']
        segType = request.form['segType']
        if len(selected_path_stack) == 0:
            path_end_coords = curr_corner_coords.plus(segType)
            flag_from_graph = retrieveFlag(startCornerCoords, flag)
            flag.setFlagAsSelected(path_end_coords, segType)

            selected_path_stack.append(flag_from_graph)
            selectedGeneratorFlagsCountdown += 1

        elif selected_path_stack[0] != flag:
            path_end_coords = curr_corner_coords.plus(segType)
            flag_from_graph = retrieveFlag(selectedPath[0].getPathEndCoords(), flag)
            flag.setFlagAsSelected(path_end_coords, segType)
            
            selected_path_stack.append(flag_from_graph)
            selectedGeneratorFlagsCountdown += 1

        elif selected_path_stack[0] == flag:
            selected_path_stack.pop()
            flag.setFlagAsUnselected()
            flag = selected_path_stack[0]
            selectedGeneratorFlagsCountdown -= 1


    nextFlagOptions = generator_flag_graph.getInPlayAdjacentFlags(flag)
    resp = make_response('{"response": '+nextFlagOptions+'}')
    resp.headers['Content-Type'] = "application/json"
    return resp
    return render_template('game_state.html', sample={"author_name": author_name.title(), "speech": speech})


app = create_app()


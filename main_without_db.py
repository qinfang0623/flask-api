from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)


# //////////////////////////////////////////////////////////////////////


# -----------------------------------
#           🚨 data
# -----------------------------------

videos = {}


# -----------------------------------
#       🚨 parse request body
# -----------------------------------

video_put_args = reqparse.RequestParser()

video_put_args.add_argument(
    "name", type=str, help="Name of the video is required.", required=True
)  # help: error message
video_put_args.add_argument(
    "views", type=int, help="Views of the video is required.", required=True
)
video_put_args.add_argument(
    "likes", type=int, help="Likes on the video is required.", required=True
)


# -----------------------------------
#       🚨 define resources
# -----------------------------------

def abort_video_if_not_exist(video_id):
    """abort if video id does not exist"""
    if video_id not in videos:
        abort(404, message="Could not find video...")


def abort_video_if_exist(video_id):
    """abort if video id already exists"""
    if video_id in videos:
        abort(409, message="Video already exists with that ID...")


class Video(Resource):
    def get(self, video_id):
        abort_video_if_not_exist(video_id)
        return videos[video_id]

    def post(self, video_id):
        """Create new records"""
        abort_video_if_exist(video_id)
        # 💥 Method 1:
        # print(request.form)
        # print(request.form["likes"])
        # 💥 Method 2:
        args = video_put_args.parse_args()
        videos[video_id] = args  # dict
        return videos[video_id], 201

    def put(self, video_id):
        """Replace existing records"""
        abort_video_if_not_exist(video_id)
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201

    def delete(self, video_id):
        abort_video_if_not_exist(video_id)
        del videos[video_id]
        return '', 204


# -----------------------------------
#       🚨 register resources
# -----------------------------------

api.add_resource(Video, "/video/<int:video_id>")  # string; int; float; path


# //////////////////////////////////////////////////////////////////////


if __name__ == "__main__":
    app.run(debug=True)

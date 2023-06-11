from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)


# //////////////////////////////////////////////////////////////////////


# -----------------------------------
#       🚨 data & database
# -----------------------------------

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VideoModel(db.Model):
    # primary_key: set as unique identifier
    id = db.Column(db.Integer, primary_key=True)
    # set max length as 100; nullable=False: must have information
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={self.name}, views={self.views}, likes={self.likes})"


# 💥 run once only to avoid overwriting the database
db.create_all()


# -----------------------------------
#       🚨 parse request body
# -----------------------------------

video_post_args = reqparse.RequestParser()

video_post_args.add_argument(
    "name", type=str, help="Name of the video is required.", required=True
)  # help: error message
video_post_args.add_argument(
    "views", type=int, help="Views of the video is required.", required=True
)
video_post_args.add_argument(
    "likes", type=int, help="Likes on the video is required.", required=True
)


video_update_args = reqparse.RequestParser()

video_update_args.add_argument(
    "name", type=str, help="Name of the video"
)
video_update_args.add_argument(
    "views", type=int, help="Views of the video"
)
video_update_args.add_argument(
    "likes", type=int, help="Likes on the video"
)


# -----------------------------------
#       🚨 define resources
# -----------------------------------

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer,
}


class Video(Resource):

    # 💥 marshal_with(resource_fields): take the retured instance and serialize it using defined 'resource_fields'
    @marshal_with(resource_fields)
    def get(self, video_id):
        video = VideoModel.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message=f"Could not find the video with id {video_id}.")
        return video

    @marshal_with(resource_fields)
    def post(self, video_id):
        """Create new records"""
        # check whether the video id already exists
        result = VideoModel.query.filter_by(id=video_id).first()
        print(result)
        if result:
            abort(409, message="Video id taken...")
        # create a new model
        args = video_post_args.parse_args()
        video = VideoModel(
            id=video_id, name=args['name'], views=args['views'], likes=args['likes']
        )
        # save the new model
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        """Update existing records"""
        # get the existing model
        video = VideoModel.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message="Video doesn't exist, cannot update!")
        # update the existing model
        args = video_update_args.parse_args()
        if args['name']:
            video.name = args['name']
        if args['views']:
            video.views = args['views']
        if args['likes']:
            video.likes = args['likes']
        # save the updated model
        db.session.commit()
        return video, 201

    def delete(self, video_id):
        # get the existing model
        video = VideoModel.query.filter_by(id=video_id).first()
        # delete this model
        db.session.delete(video)
        db.session.commit()
        return '', 204


# -----------------------------------
#       🚨 register resources
# -----------------------------------

api.add_resource(Video, "/video/<int:video_id>")  # string; int; float; path


# //////////////////////////////////////////////////////////////////////


if __name__ == "__main__":
    app.run(debug=True)

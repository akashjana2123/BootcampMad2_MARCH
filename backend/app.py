from flask import Flask,jsonify,make_response
from flask_restful import Api,Resource,reqparse
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity, unset_jwt_cookies
from flask_cors import CORS
from werkzeug.security import generate_password_hash,check_password_hash 
from model import db,User,Category,Product

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'grocery'

db.init_app(app)
CORS(app,origins='*')
jwt = JWTManager(app)
api = Api(app)

class SignupResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username',type=str,required=True)
        parser.add_argument('email',type=str,required=True)
        parser.add_argument('password',type=str)
        parser.add_argument('role',type=str,default='user')


        args = parser.parse_args()

        if User.query.filter_by(username=args['username']).first():
            return {"message":"Username already exists"}, 400
        
        hashed_password = generate_password_hash(args['password'])
        if args['role'] == 'store-manager':
            new_user = User(username=args['username'],password=hashed_password,email=args['email'],role=args['role'],approved=False)
        else:
            new_user = User(username=args['username'],password=hashed_password,email=args['email'],role=args['role'],approved=True)
        db.session.add(new_user)
        db.session.commit()

        return {"message":"User Created Successfully"}, 200


class LoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username',type=str,required=True)
        parser.add_argument('password',type=str)


        args = parser.parse_args()

        user = User.query.filter_by(username=args['username']).first()
        
        if user and check_password_hash(user.password,args['password']):
            if user.approved== False:
                return {'message':'Please wait for approval from the admin'}, 401
            access_token = create_access_token(identity=user.role)
            user_info={
                "id":user.id,
                "username":user.username,
                "role":user.role
            }

            return {'access_token':access_token,"user":user_info}, 200
        else:
            return {'message':"invalide username and password"}, 401

class Logout(Resource):
    @jwt_required()
    def post(self):
        role = get_jwt_identity()
        print(role)
        resp = {"message":"Logged out successfully"}
        unset_jwt_cookies(jsonify(resp))
        return resp,200


class UserInfo(Resource):
    @jwt_required()
    def get(self):
        users = User.query.all()
        user_info = [{
            "id":user.id,
            "username":user.username,
            "role":user.role
        } for user in users]

        return user_info
    

class CategoryResource(Resource):
    @jwt_required()
    def get(self):
        categories = Category.query.all()

        return jsonify([{
            'id':category.id,
            'name':category.name
        } for category in categories])
    
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name',type=str,required=True)

        args= parser.parse_args()

        if Category.query.filter_by(name=args['name']).first():
            return {"message":"category already exists"}, 400
        new_category = Category(name=args['name'])
        db.session.add(new_category)
        db.session.commit()

        return {"message":"category created succesully"}, 200

    @jwt_required()
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',type=int,required=True)
        parser.add_argument('name',type=str,required=True)

        args= parser.parse_args()

        category = Category.query.get(args['id'])
        if not category:
            return {"message":"category not found"}, 404
        
        category.name = args['name']

        db.session.commit()

        return {"message":"category updated successfully"}, 200
    
    @jwt_required()
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',type=int,required=True)

        args= parser.parse_args()

        category = Category.query.get(args['id'])
        if not category:
            return {"message":"category not found"}, 404
        
        db.session.delete(category)
        db.session.commit()

        return {"message":'category deleted successully'}, 200

api.add_resource(CategoryResource,'/api/category')
api.add_resource(UserInfo,'/api/info')
api.add_resource(SignupResource,'/api/signup')
api.add_resource(LoginResource,'/api/login')
api.add_resource(Logout,'/logout')

if __name__ == "__main__":
    app.run(debug=True)


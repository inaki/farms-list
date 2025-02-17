import json
import jsonpickle
from decimal import Decimal

from flask import Blueprint
from farmsList.public.models import Parcel, Farmland, AdditionalLayer
from farmsList.database import db
from sqlalchemy import func


blueprint = Blueprint('api', __name__, url_prefix='/api',
						static_folder="../static")

def pre_json_encode(obj):
	for key in obj.__dict__.keys():
		if isinstance(obj.__dict__[key], Decimal):
			obj.__dict__[key] = float(obj.__dict__[key])
	obj.__dict__['_sa_instance_state'] = None
	return obj

@blueprint.route("/parcel/", methods=["GET", "POST"])
def api_parcel():
	farmlandData = Farmland.query.filter(Farmland.public == True).all()
	for farmland in farmlandData:
		farmland.geometry = db.session.query(func.ST_AsGeoJson(farmland.geometry)).all()[0][0]
		db.session.close()
		farmland.center = db.session.query(func.ST_AsGeoJson(farmland.center)).all()[0][0]
		db.session.close()
		farmland.center = json.loads(str(farmland.center))
		farmland = pre_json_encode(farmland)
	return jsonpickle.encode(farmlandData, unpicklable=False, make_refs=False)

@blueprint.route("/farmland/<int:farmlandId>", methods=["GET", "POST"])
def api_farmland_by_id(farmlandId):
	farmlandData = Farmland.query.filter_by(id=farmlandId).all()[0]
	farmlandData.center = db.session.query(func.ST_AsGeoJson(farmlandData.center)).all()[0][0]
	db.session.close()
	farmlandData.geometry = db.session.query(func.ST_AsGeoJson(farmlandData.geometry)).all()[0][0]
	db.session.close()
	farmlandData.center = json.loads(str(farmlandData.center))
	farmlandData = pre_json_encode(farmlandData)
	return jsonpickle.encode(farmlandData, unpicklable=False, make_refs=False)

@blueprint.route("/tax-incentive-zones", methods=["GET"])
def tax_incentive_zones():
	taxIncentiveZones = AdditionalLayer.query.filter_by(name="taxIncentive").all()
	for taxIncentiveZone in taxIncentiveZones:
		taxIncentiveZone.geometry = db.session.query(func.ST_AsGeoJson(taxIncentiveZone.geom)).all()[0][0]
		db.session.close()
	return jsonpickle.encode(taxIncentiveZones, unpicklable=False, make_refs=False)

@blueprint.route("/food-deserts", methods=["GET"])
def food_desert_zones():
	foodDeserts = AdditionalLayer.query.filter_by(name="foodDesert").all()
	for taxIncentiveZone in foodDeserts:
		taxIncentiveZone.geometry = db.session.query(func.ST_AsGeoJson(taxIncentiveZone.geom)).all()[0][0]
		db.session.close()
	return jsonpickle.encode(foodDeserts, unpicklable=False, make_refs=False)

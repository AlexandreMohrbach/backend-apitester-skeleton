import pathlib as pl

import numpy as np
import pandas as pd

from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

data = pl.Path(__file__).parent.absolute() / 'data'

# Charger les données CSV
associations_df = pd.read_csv(data / 'associations_etudiantes.csv')
evenements_df = pd.read_csv(data / 'evenements_associations.csv')

# # Vous devez ajouter les routes ici : 



# 1. Vérifier si le serveur est actif
@app.route("/api/alive", methods=["GET"])
def alive():
    return jsonify({"message": "Alive"}), 200

# 2. Liste de toutes les associations (IDs)
@app.route("/api/associations", methods=["GET"])
def get_associations():
    ids = associations_df["id"].tolist()
    return jsonify(ids), 200

# 3. Détails d'une association par ID
@app.route("/api/association/<int:assoc_id>", methods=["GET"])
def get_association_by_id(assoc_id):
    assoc = associations_df[associations_df["id"] == assoc_id]
    if assoc.empty:
        return jsonify({"error": "Association not found"}), 404
    return jsonify(assoc.iloc[0].to_dict()), 200

# 4. Liste de tous les événements (IDs)
@app.route("/api/evenements", methods=["GET"])
def get_evenements():
    ids = evenements_df["id"].tolist()
    return jsonify(ids), 200

# 5. Détails d'un événement par ID
@app.route("/api/evenement/<int:event_id>", methods=["GET"])
def get_evenement_by_id(event_id):
    event = evenements_df[evenements_df["id"] == event_id]
    if event.empty:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(event.iloc[0].to_dict()), 200

# 6. Liste des événements d'une association
@app.route("/api/association/<int:assoc_id>/evenements", methods=["GET"])
def get_evenements_by_association(assoc_id):
    events = evenements_df[evenements_df["association_id"] == assoc_id]
    return jsonify(events.to_dict(orient="records")), 200

# 7. Liste des associations par type
@app.route("/api/associations/type/<type_name>", methods=["GET"])
def get_associations_by_type(type_name):
    filtered = associations_df[associations_df["type"].str.lower() == type_name.lower()]
    return jsonify(filtered.to_dict(orient="records")), 200

# Lancer le serveur Flask
if __name__ == "__main__":
    app.run(debug=True, port=5000)
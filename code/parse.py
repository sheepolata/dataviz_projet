#!/usr/bin/env python

import json

def name_and_stats(nom_fichier):
	#Beta
	fichier = open("../data/60ind_20gen.json", 'r')

	data = json.load(fichier)

	generations = data["generations"]

	dico_names = {}

	for gen in generations:
		matchs = gen["matchs"]
		for match in matchs:
			p1 = match["player_1"]
			p2 = match["player_2"]
			dico_names[p1["name"]] = {"intelligence" : p1["Intelligence"],
									  "force" : p1["Force"],
						              "vitesse" : p1["Vitesse"], 
						              "somme" : round(p1["Intelligence"] + p1["Force"] + p1["Vitesse"], 2) }
			dico_names[p2["name"]] = {"intelligence" : p2["Intelligence"],
									  "force" : p2["Force"],
						              "vitesse" : p2["Vitesse"], 
						              "somme" : round(p2["Intelligence"] + p2["Force"] + p2["Vitesse"], 2) }

	json_tmp = []
	for k in dico_names:
		json_tmp.append({"name" : k, "stats" : dico_names[k]})

	json_data = {"players" : json_tmp}


	fichier_res = open("../data/data_noms_stats.json", 'w')

	fichier_res.write(json.dumps(json_data, indent=4, sort_keys=True))




if __name__ == '__main__':
	name_and_stats("test")

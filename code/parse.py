#!/usr/bin/env python

import json

"""Cree un fichier json contenant le nom de chaque agent, ses stats, la somme de celle ci, sa premiere generation et sa derniere generation"""
def name_and_stats(nom_fichier):
	#Beta
	fichier = open("../data/60ind_20gen.json", 'r')

	data = json.load(fichier)

	generations = data["generations"]

	dico_names = {}

	data_gen = {}

	for gen in generations:
		matchs = gen["matchs"]
		nb_gen = gen["gen_number"]
		for match in matchs:
			p1 = match["player_1"]
			p2 = match["player_2"]

			data_gen[p1["name"]] = nb_gen
			data_gen[p2["name"]] = nb_gen

			dico_names[p1["name"]] = {"intelligence" : p1["Intelligence"],
									  "force" : p1["Force"],
						              "vitesse" : p1["Vitesse"], 
						              "somme" : round(p1["Intelligence"] + p1["Force"] + p1["Vitesse"], 2)}
			dico_names[p2["name"]] = {"intelligence" : p2["Intelligence"],
									  "force" : p2["Force"],
						              "vitesse" : p2["Vitesse"], 
						              "somme" : round(p2["Intelligence"] + p2["Force"] + p2["Vitesse"], 2)}

	json_tmp = []
	for k in dico_names:
		json_tmp.append({"name" : k, "stats" : dico_names[k], "first_gen" : get_gen_from_name(k), "last_gen" : data_gen[k]})

	json_data = {"players" : json_tmp}


	fichier_res = open("../data/data_noms_stats.json", 'w')

	fichier_res.write(json.dumps(json_data, indent=4, sort_keys=True))

"""Recupere le numero de la generation dans laquel l'agent est cree a partir du nom"""
def get_gen_from_name(name):
	c = 1
	resl = []
	while c < len(name):
		if name[c] != 'J':
			resl.append(name[c])
		else:
			break
		c += 1
	res = "".join(resl)
	return int(res)

"""Cree un fichier json contenant chaque agent et ses parents"""
def genealogie_simple(nom_fichier):
	fichier = open("../data/60ind_20gen.json", 'r')

	data = json.load(fichier)

	generations = data["generations"]

	dico_parent = {}

	for gen in generations:
		matchs = gen["matchs"]
		for match in matchs:
			p1 = match["player_1"]
			p2 = match["player_2"]

			dico_parent[p1["name"]] = {"parent_1" : p1["parent_1"], "parent_2" : p1["parent_2"]}
			dico_parent[p2["name"]] = {"parent_1" : p2["parent_1"], "parent_2" : p2["parent_2"]}

	json_tmp = []
	for k in dico_parent:
		json_tmp.append({"name" : k, "parent_1" : dico_parent[k]["parent_1"], "parent_2" : dico_parent[k]["parent_2"]})

	json_data = {"players" : json_tmp}

	fichier_res = open("../data/data_ancetres.json", 'w')

	fichier_res.write(json.dumps(json_data, indent=4, sort_keys=True))
	
def stat_gen(nom_fichier):
	fichier = open("../data/60ind_20gen.json", 'r')

	data = json.load(fichier)

	generations = data["generations"]

	dico_stats_gen = {"Generations" : []}
	dico_stats_gen["Mutation_Fixe"] = data["fixed_mutation_rate"]
	for gen in generations:
		force = 0
		intel = 0
		vites = 0
		matchs = gen["matchs"]
		for match in matchs:
			p1 = match["player_1"]
			p2 = match["player_2"]

			force += p1["Force"] + p2["Force"]
			intel += p1["Intelligence"] + p2["Intelligence"]
			vites += p1["Vitesse"] + p2["Vitesse"]
		force = round(force / (len(matchs)*2), 2)
		intel = round(intel / (len(matchs)*2), 2)
		vites = round(vites / (len(matchs)*2), 2)
		dico_stats_gen["Generations"].append({"Numero_Gen" : gen["gen_number"], "Force" : force, "Vitesse" : vites, "Intelligence" : intel, "Mutation" : gen["gen_real_mutation_rate"]})
	

	fichier_res = open("../data/data_stats_gen.json", 'w')

	fichier_res.write(json.dumps(dico_stats_gen, indent=4, sort_keys=True))
		
	
if __name__ == '__main__':
	name_and_stats("test")
	genealogie_simple("test")
	stat_gen("test")
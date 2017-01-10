#!/usr/bin/env python

import json, os

"""Cree plusieurs csv pour la pie chart, uniquement ubuntu"""
def data_strat_csv(in_file,out_file="data/data_strat_gen"):
	fichier = open(in_file, 'r')

	data = json.load(fichier)
	generation = data["generations"]

	nb_strat_total = []
	nb_dumb        = []
	nb_off         = []
	nb_def         = []

	for gen in generation:
		matchs = gen["matchs"]
		tmp_total = 0
		tmp_dumb  = 0
		tmp_off   = 0
		tmp_def   = 0
		for m in matchs:
			p1 = m["player_1"]
			p2 = m["player_2"]
			fav1 = p1["favorite_strategy"]
			fav2 = p2["favorite_strategy"]
			tmp_total += fav1["def"] + fav1["dumb"] + fav1["off"] + fav2["def"] + fav2["dumb"] + fav2["off"]
			tmp_dumb  += fav1["dumb"] + fav2["dumb"]
			tmp_off   += fav1["off"] + fav2["off"]
			tmp_def   += fav1["def"] + fav2["def"]
		nb_strat_total.append(tmp_total)
		nb_dumb       .append(tmp_dumb)
		nb_off        .append(tmp_off)
		nb_def        .append(tmp_def)

	for i in range(len(generation)):
		fichier_res = open(out_file+str(i+1)+".csv", 'w')
		fichier_res.write("class,value\n")
		fichier_res.write("dumb,"+ str(nb_dumb[i]) + "\n")
		fichier_res.write("off," + str(nb_off[i])  + "\n")
		fichier_res.write("def," + str(nb_def[i]))
		fichier_res.close()



"""Cree un fichier json contenant les informations pour cree la pie chart des strategies"""
def data_strat(in_file, out_file="data/data_strats.json"):
	fichier = open(in_file, 'r')

	data = json.load(fichier)
	generation = data["generations"]

	nb_strat_total = []
	nb_dumb        = []
	nb_off         = []
	nb_def         = []

	for gen in generation:
		matchs = gen["matchs"]
		tmp_total = 0
		tmp_dumb  = 0
		tmp_off   = 0
		tmp_def   = 0
		for m in matchs:
			p1 = m["player_1"]
			p2 = m["player_2"]
			fav1 = p1["favorite_strategy"]
			fav2 = p2["favorite_strategy"]
			tmp_total += fav1["def"] + fav1["dumb"] + fav1["off"] + fav2["def"] + fav2["dumb"] + fav2["off"]
			tmp_dumb  += fav1["dumb"] + fav2["dumb"]
			tmp_off   += fav1["off"] + fav2["off"]
			tmp_def   += fav1["def"] + fav2["def"]
		nb_strat_total.append(tmp_total)
		nb_dumb       .append(tmp_dumb)
		nb_off        .append(tmp_off)
		nb_def        .append(tmp_def)


	json_tmp = []
	for i in range(len(nb_strat_total)):
		json_tmp.append({})
		json_tmp[i]["generation"]     = i+1
		json_tmp[i]["nb_total_strat"] = nb_strat_total[i] 
		json_tmp[i]["nb_dumb"]        = nb_dumb[i] 
		json_tmp[i]["nb_off"]         = nb_off[i] 
		json_tmp[i]["nb_def"]         = nb_def[i] 

	json_data = {"generations" : json_tmp}

	fichier_res = open(out_file, 'w')

	fichier_res.write(json.dumps(json_data, indent=4, sort_keys=True))
		


"""Cree un fichier json contenant le nom de chaque agent, ses stats, la somme de celle ci, sa premiere generation et sa derniere generation"""
def name_and_stats(in_file, out_file="data/data_noms_stats.json"):
	#Beta
	fichier = open(in_file, 'r')

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


	fichier_res = open(out_file, 'w')

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
def genealogie_simple(in_file, out_file="data/data_ancetres.json"):
	fichier = open(in_file, 'r')

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

	fichier_res = open(out_file, 'w')

	fichier_res.write(json.dumps(json_data, indent=4, sort_keys=True))
	
def stat_gen(in_file, out_file="data/data_stats_gen.json"):
	fichier = open(in_file, 'r')

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
	

	fichier_res = open(out_file, 'w')

	fichier_res.write(json.dumps(dico_stats_gen, indent=4, sort_keys=True))

def result_match(in_file, out_file="data/data_stats_matchs.json"):
	# fichier = open("C:/Users/Janjak/Desktop/testDV/Projet/60ind_20gen.json", 'r')
	fichier = open(in_file, 'r')

	data = json.load(fichier)
	
	generations = data["generations"]
	matchs = []
	dico_match = {"Generations" : []}
	for gen in generations:
		dico_match["Generations"].append({"Generation" : gen["gen_number"]})
		new_matchs = []
		for match in gen["matchs"]:
			new_match   = {}

			id_match	= match["match_nb"]
			p1 			= match["player_1"]
			p1_color 	= p1["team"]
			p1_points 	= p1["points"]
			p1_name 	= p1["name"]
			p1_strat	= p1["favorite_strategy"]
			
			p2 			= match["player_2"]            
			p2_color	= p2["team"]
			p2_points 	= p2["points"]   
			p2_name 	= p2["name"]
			p2_strat	= p2["favorite_strategy"]

			new_match["id_match"] = id_match
			new_match["p1_color"] = p1_color
			new_match["p1_points"] = p1_points
			new_match["p1_name"] = p1_name
			new_match["p1_strat"] = p1_strat
			new_match["p2_color"] = p2_color
			new_match["p2_points"] = p2_points
			new_match["p2_color"] = p2_color
			new_match["p2_name"] = p2_name
			new_match["p2_strat"] = p2_strat
			
			new_matchs.append(new_match)

		dico_match["Generations"][-1]["Matchs"] = new_matchs

	fichier_res = open(out_file, 'w')

	fichier_res.write(json.dumps(dico_match, indent=4, sort_keys=True))	
	


if __name__ == '__main__':

	"""Ubuntu 16.04"""
	file1 = "data/60ind_20gen.json"
	file2 = "data/60ind_60gen.json"
	name_and_stats(file2)
	genealogie_simple(file2)
	stat_gen(file2)
	result_match(file2)
	data_strat(file2)
	data_strat_csv(file2)

	"""Windows"""
	# name_and_stats("C:/Users/Janjak/Desktop/testDV/Projet/60ind_20gen.json", TOADD)
	# genealogie_simple("C:/Users/Janjak/Desktop/testDV/Projet/60ind_20gen.json", TOADD)
	# stat_gen("C:/Users/Janjak/Desktop/testDV/Projet/60ind_20gen.json", TOADD)
	# result_match("C:/Users/Janjak/Desktop/testDV/Projet/60ind_20gen.json", "C:/Users/Janjak/Desktop/testDV/Projet/data_stats_matchs.json")
	# data_strat("C:/Users/Janjak/Desktop/testDV/Projet/60ind_20gen.json", "C:/Users/Janjak/Desktop/testDV/Projet/60ind_20gen.json")
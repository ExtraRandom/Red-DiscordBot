kills_cop = steam_json.steam_read(data, "enemy_kills_cop")
kills_fbi = steam_json.steam_read(data, "enemy_kills_fbi")
kills_fbi_swat = steam_json.steam_read(data, "enemy_kills_fbi_swat")
kills_fbi_heavy_swat = steam_json.steam_read(data, "enemy_kills_fbi_heavy_swat")
kills_swat = steam_json.steam_read(data, "enemy_kills_swat")
kills_heavy_swat = steam_json.steam_read(data, "enemy_kills_heavy_swat")
kills_city_swat = steam_json.steam_read(data, "enemy_kills_city_swat")
kills_security = steam_json.steam_read(data, "enemy_kills_security")
kills_gensec = steam_json.steam_read(data, "enemy_kills_gensec")
kills_gangster = steam_json.steam_read(data, "enemy_kills_gangster")
kills_sniper = steam_json.steam_read(data, "enemy_kills_sniper")
kills_shield = steam_json.steam_read(data, "enemy_kills_shield")
kills_cloaker = steam_json.steam_read(data, "enemy_kills_spooc")
kills_tank = steam_json.steam_read(data, "enemy_kills_tank")
kills_taser = steam_json.steam_read(data, "enemy_kills_taser")
kills_mobster = steam_json.steam_read(data, "enemy_kills_mobster")
kills_mobster_boss = steam_json.steam_read(data, "enemy_kills_mobster_boss")
kills_civilian = steam_json.steam_read(data, "enemy_kills_civilian")
kills_civilian_female = steam_json.steam_read(data, "enemy_kills_civilian")
kills_tank_hw = steam_json.steam_read(data, "enemy_kills_tank_hw")
kills_hector_boss = steam_json.steam_read(data, "enemy_kills_hector_boss")
kills_hector_boss_no_armor = steam_json.steam_read(data, "enemy_kills_hector_boss_no_armor")
kills_tank_green = steam_json.steam_read(data, "enemy_kills_tank_green")
kills_tank_black = steam_json.steam_read(data, "enemy_kills_tank_black")
kills_tank_skull = steam_json.steam_read(data, "enemy_kills_tank_skull")
kills_hostage_rescue = steam_json.steam_read(data, "enemy_kills_hostage_rescue")
kills_murkywater = steam_json.steam_read(data, "enemy_kills_murkywater")
kills_winters_minion = steam_json.steam_read(data, "enemy_kills_phalanx_minion")
kills_biker_boss = steam_json.steam_read(data, "enemy_kills_biker_boss")
kills_cop_female = steam_json.steam_read(data, "enemy_kills_cop_female")
kills_medic = steam_json.steam_read(data, "enemy_kills_medic")
kills_chavez_boss = steam_json.steam_read(data, "enemy_kills_chavez_boss")

total_kills = kills_cop + kills_fbi + kills_fbi_swat + kills_fbi_heavy_swat + kills_swat + \
              kills_heavy_swat + kills_city_swat + kills_security + kills_gensec + kills_gangster + \
              kills_sniper + kills_shield + kills_cloaker + kills_tank + kills_taser + kills_mobster + \
              kills_mobster_boss + kills_civilian + kills_civilian_female + kills_tank_hw + \
              kills_hector_boss + kills_hector_boss_no_armor + kills_tank_green + kills_tank_black + \
              kills_tank_skull + kills_hostage_rescue + kills_murkywater + kills_winters_minion + \
              kills_biker_boss + kills_cop_female + kills_medic + kills_chavez_boss

tank_kills = kills_tank + kills_tank_skull + kills_tank_green + kills_tank_hw + kills_tank_black
civ_kills = kills_civilian + kills_civilian_female
gang_mob_kills = kills_gangster + kills_mobster_boss + kills_mobster

cop_swat = kills_cop + kills_cop_female + kills_city_swat + kills_heavy_swat + kills_swat
fbi = kills_fbi + kills_fbi_heavy_swat + kills_fbi_swat

shield_sniper_cloaker = kills_sniper + kills_shield + kills_cloaker
other_kills = total_kills - (tank_kills + gang_mob_kills + civ_kills + shield_sniper_cloaker +
                             cop_swat + fbi)




# norm_vh_diff = diff_norm + diff_h + diff_vh
# ovk_may_diff = diff_ovk + diff_my
# dw_od_diff = diff_dw + diff_od

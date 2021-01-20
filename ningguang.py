from utils import calc_dmg, calc_dmg_obj, avg_crit_dmg, AttrObj, DmgTag

# list of damage applications, tags, 
# combo as a list of damage applications with tags

'''
C0-C1: (Normal + Charged) x 5 + E + Q		10.3	Attack	Geo	CR/CD	Petra + Gladiator’s		Petra + Gladiator’s	
C1-C4: (Normal + Charged) x 5 + 2x E + Q		11.2							
C6: (Normal + Charged) x 4 + 2x E + Q + Charged		10.8							
Shield Uptime	75.0%								
'''

auto_time = 1 # sec
skyward_atlas_attacks = 6 # should be 160% each time

gems_hit = 10 # 6 from burst, 6 from jade screen 2 into ground (-2)
field_time = 10.3
atlas_field_time = 30 + auto_time # cooldown + autotime because 50% chance 
resist_down = 0 # .2 geo resonance, .4 zl + geo resonance
strat_reserve_uptime = 1 # a4

artifact_main_stats = AttrObj(flat_atk=311, atk_pct=.466, crit_rate=.311, dmg_bonus={DmgTag.GEO: .466})
artifact_substats = AttrObj(flat_atk=50, atk_pct=.249, crit_rate=.198, crit_dmg=.396, em=99, er=.275, flat_hp=762, hp_pct=.149, flat_def=59, def_pct=.186) # should this include all?
artifact_set_effects = AttrObj(atk_pct=.18, dmg_bonus={DmgTag.GEO: .15}) # glad, petra

char_attr = AttrObj(base_atk=188, crit_rate=.05, crit_dmg=.50, dmg_bonus={DmgTag.GEO: .18})
#weapon_attr = AttrObj(base_atk=565, em=110, dmg_bonus={DmgTag.GEO: .14}) # mappa mare, lvl 90/90, .14 from zakharov sheet

weapon_attr = AttrObj(base_atk=674, atk_pct=.331, dmg_bonus={DmgTag.GEO: .12}) # skyward atlas, lvl 90/90, .14 from zakharov sheet


a4 = AttrObj(dmg_bonus={DmgTag.GEO: .12*strat_reserve_uptime})

tot_attr = char_attr + weapon_attr + artifact_main_stats + artifact_substats + artifact_set_effects

print(tot_attr)

na_ca_dmg = avg_crit_dmg(calc_dmg_obj(tot_attr, (.392*2+2.44+.694), [DmgTag.GEO, DmgTag.CHARGED], enemy_resist_pct=.1-resist_down), tot_attr.crit_rate, tot_attr.crit_dmg)*5

skill_dmg = avg_crit_dmg(calc_dmg_obj(tot_attr, 3.23, [DmgTag.GEO, DmgTag.SKILL], enemy_resist_pct=.1-resist_down), tot_attr.crit_rate, tot_attr.crit_dmg)*1

burst_dmg = avg_crit_dmg(calc_dmg_obj(tot_attr, gems_hit*1.22, [DmgTag.GEO, DmgTag.SKILL], enemy_resist_pct=.1-resist_down), tot_attr.crit_rate, tot_attr.crit_dmg)*1


atlas_passive_dmg = avg_crit_dmg(calc_dmg_obj(tot_attr, 1.60, []), tot_attr.crit_rate, tot_attr.crit_dmg)*skyward_atlas_attacks
tot_dmg = na_ca_dmg + skill_dmg + burst_dmg  

dps = tot_dmg/field_time
dps_wep = atlas_passive_dmg/atlas_field_time
print(dps + dps_wep)

# (39.2%*2+244%+69.4%)*5 , 5 (normal + charged)
# (39.2%*2+244%+69.4%)*4 + 244%+69.4%*7, 4 normal + charged + 1 charged
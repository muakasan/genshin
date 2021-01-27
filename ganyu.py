# Python Port of Zakharov's Ganyu DPS Calculation https://docs.google.com/spreadsheets/d/1RAz3jx4x1ThWED8XWg8GKIf73RjPrZrnSukYZUCSRU8/edit#gid=1120258150
from utils import calc_dmg, calc_dmg_obj, avg_crit_dmg, AttrObj, DmgTag

# list of damage applications, tags, 
# combo as a list of damage applications with tags

celestial_shower_hits_per_enemy = 12
a1_passive_uptime = .75
a1_passive_bloom_uptime = 1
a4_passive_uptime = .675
prototype_crescent_uptime = .9
viridescent_hunt_proc_rate = .938
headshot_rate = .3
cryo_uptime = .90
freeze_uptime = 0
field_time = 10

artifact_main_stats = AttrObj(flat_atk=311, atk_pct=.466, crit_rate=.311, dmg_bonus={DmgTag.CRYO: .466}) # cryo goblet
artifact_substats = AttrObj(flat_atk=50, atk_pct=.249, crit_rate=.198, crit_dmg=.396, em=99, er=.275, flat_hp=762, hp_pct=.149, flat_def=59, def_pct=.186) # should this include all?
artifact_set_effects = AttrObj(crit_rate=(cryo_uptime*.20 + freeze_uptime * .20), dmg_bonus={DmgTag.CRYO: .15})

char_attr = AttrObj(base_atk=295, crit_rate=.05, crit_dmg=(.50 + .288)) #ascension + base values, c0
weapon_attr = AttrObj(base_atk=510, atk_pct=.413 + .36*prototype_crescent_uptime) # prototype_crescent, lvl 90

burst_bonus = AttrObj(dmg_bonus={DmgTag.CRYO: a4_passive_uptime*.20})


tot_attr = char_attr + artifact_main_stats + artifact_substats + artifact_set_effects + weapon_attr + burst_bonus 
print(tot_attr)


a1 = AttrObj(crit_rate=a1_passive_uptime*.20)
ca_attr = tot_attr + a1
cr = headshot_rate + (1-headshot_rate)*ca_attr.crit_rate
#print('cr', cr)

ca_dmg = avg_crit_dmg(calc_dmg_obj(ca_attr, 1.792, [DmgTag.CRYO, DmgTag.CHARGED]), cr, ca_attr.crit_dmg)*4
print(ca_dmg)

a1 = AttrObj(crit_rate=a1_passive_bloom_uptime*.20)
bloom_attr = tot_attr + a1
# Bloom cannot guaranteed crit without angle trick
bloom_dmg = avg_crit_dmg(calc_dmg_obj(bloom_attr, 3.0464, [DmgTag.CRYO, DmgTag.CHARGED]), bloom_attr.crit_rate, bloom_attr.crit_dmg)*4
print(bloom_dmg)

skill_dmg = avg_crit_dmg(calc_dmg_obj(tot_attr, 3.326, [DmgTag.CRYO, DmgTag.SKILL]), tot_attr.crit_rate, tot_attr.crit_dmg)*1
print(skill_dmg)

burst_dmg = avg_crit_dmg(calc_dmg_obj(tot_attr, 11.806, [DmgTag.CRYO, DmgTag.SKILL]), tot_attr.crit_rate, tot_attr.crit_dmg)*1
print(burst_dmg)

tot_dmg = ca_dmg + bloom_dmg + skill_dmg + burst_dmg
dps = tot_dmg/field_time
print(dps)
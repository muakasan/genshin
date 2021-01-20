from utils import calc_dmg, calc_dmg_obj, avg_crit_dmg, calc_avg_crit_dmg_obj, AttrObj, DmgTag, calc_tot_atk

# list of damage applications, tags, 
# combo as a list of damage applications with tags
'''
From Mathalos: Full combo frames = 192 (60 FPS)
'''
'''
From Zakharov: 
(4 x Normal) x 4 + E + Q
Has energy support to maintain burst uptime
Field time 15
'''

'''
a4:
Every 4 Normal or Charged Attack hits will decrease the CD of Breastplate by 1s.
Hitting multiple opponents with a single attack is only counted as 1 hit.
'''

field_time = 15
resist_down = 0

artifact_main_stats = AttrObj(flat_atk=311, crit_dmg=.622, dmg_bonus={DmgTag.GEO: .466}, def_pct=.583)
artifact_substats = AttrObj(flat_atk=50, atk_pct=.249, crit_rate=.198, crit_dmg=.396, em=99, er=.275, flat_hp=762, hp_pct=.149, flat_def=59, def_pct=.186) # should this include all? TODO check this
artifact_set_effects = AttrObj(atk_pct=.18, dmg_bonus={DmgTag.NORMAL: .35}) # glad

char_attr = AttrObj(base_atk=169, crit_rate=.05, crit_dmg=.50, def_pct=.225)
weapon_attr = AttrObj(base_atk=510, crit_rate=.276, dmg_bonus={DmgTag.GEO: 5*.06}) # serpent spine, lvl 90/90, 5 stacks, should be all damage not just geo
tot_attr = char_attr + weapon_attr + artifact_main_stats + artifact_substats + artifact_set_effects

burst_atk_bonus = AttrObj(flat_atk=(.68 +.50) * calc_tot_atk(708, tot_attr.def_pct, tot_attr.flat_def)) #708 base def at 80/80 for noelle, .50 from c6

tot_attr += burst_atk_bonus



na_dmg = calc_avg_crit_dmg_obj(tot_attr, 1.15 + 1.07 + 1.25 + 1.65, [DmgTag.GEO, DmgTag.NORMAL], enemy_resist_pct=.1-resist_down)*4
skill_dmg = calc_avg_crit_dmg_obj(tot_attr, 2.04, [DmgTag.GEO, DmgTag.SKILL], enemy_resist_pct=.1-resist_down)*1
c4_dmg = calc_avg_crit_dmg_obj(tot_attr, 4.00, [DmgTag.GEO, DmgTag.SKILL], enemy_resist_pct=.1-resist_down)*1 #once per shield
burst_dmg = calc_avg_crit_dmg_obj(tot_attr, 1.14 + 1.58, [DmgTag.GEO, DmgTag.BURST], enemy_resist_pct=.1-resist_down)*1


tot_dmg = na_dmg + skill_dmg + c4_dmg + burst_dmg  

dps = tot_dmg/field_time
print(dps)

# c0 (39.2%*2+244%+69.4%)*5 , 5 (normal + charged)
# c6 (39.2%*2+244%+69.4%)*4 + 244%+69.4%*7, 4 (normal + charged) + 1 charged
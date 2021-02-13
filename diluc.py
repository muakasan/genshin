from utils import calc_dmg, calc_dmg_obj, avg_crit_dmg, AttrObj, DmgTag

'''
4pc Crimson Witch		
ATK%, Pyro%, Crit Rate/Crit Damage		
Q-NENENEN						
'''
'''
Hero Level	80
Enemey Level	80
Enemy Elem Res	10.0%
Enemy Phys Res	10.0%
'''

resist_down = 0

field_time = 7
cw_avg_stacks = 2.7
burst_procs = 4.0
spine_stacks = 3.0
wg_passive_uptime = .3
archaic_procs = 0.7
#starsilver_triggers = 1.0
liyue_chars = 2.0
a4_uptime = 1

#artifact_main_stats = AttrObj(flat_atk=311, atk_pct=.466, crit_rate=.311, dmg_bonus={DmgTag.PYRO: .466})
artifact_main_stats = AttrObj(flat_atk=311, atk_pct=.466, crit_dmg=.622, dmg_bonus={DmgTag.PYRO: .466})

artifact_substats = AttrObj(flat_atk=50, atk_pct=.249, crit_rate=.198, crit_dmg=.396, em=99, er=.275, flat_hp=762, hp_pct=.149, flat_def=59, def_pct=.186)
artifact_set_effects = AttrObj(dmg_bonus={DmgTag.PYRO: .15 + .15*.5*cw_avg_stacks}) # cw

char_attr = AttrObj(base_atk=295, crit_rate=.194, crit_dmg=.50, dmg_bonus={DmgTag.PYRO: a4_uptime*.2}) #crit rate ascension stat

archaic_attr = AttrObj(base_atk=565, atk_pct=.276) # archaic, lvl 90/90, phys procs later
spine_attr = AttrObj(base_atk=510, crit_rate=.276, dmg_bonus={DmgTag.PYRO: spine_stacks*.06}) # serpent spine, lvl 90/90
wg_attr = AttrObj(base_atk=608, atk_pct=.20+.496+.40*wg_passive_uptime) # wolf's gravestone, lvl 90/90
lithic_attr = AttrObj(base_atk=510, atk_pct=.331, dmg_bonus={DmgTag.GEO: .12}) # lithic blade, lvl 90/90 NOT DONE YET

for weapon_attr in [spine_attr, wg_attr]:
#for weapon_attr in [archaic_attr, spine_attr, wg_attr, lithic_attr]:

    tot_attr = char_attr + weapon_attr + artifact_main_stats + artifact_substats + artifact_set_effects

    print(tot_attr)
    na_ca_dmg = avg_crit_dmg(calc_dmg_obj(tot_attr, 1.3, [DmgTag.PYRO], enemy_resist_pct=.1-resist_down), tot_attr.crit_rate, tot_attr.crit_dmg)*4 # 4 N1's
    print(na_ca_dmg)
    skill_dmg = avg_crit_dmg(calc_dmg_obj(tot_attr, (1.32+1.37+1.8), [DmgTag.PYRO, DmgTag.SKILL], enemy_resist_pct=.1-resist_down), tot_attr.crit_rate, tot_attr.crit_dmg)*1
    print(skill_dmg)

    burst_dmg = avg_crit_dmg(calc_dmg_obj(tot_attr, 2.86+0.84*burst_procs, [DmgTag.PYRO, DmgTag.BURST], enemy_resist_pct=.1-resist_down), tot_attr.crit_rate, tot_attr.crit_dmg)*1
    print(burst_dmg)


    #atlas_passive_dmg = avg_crit_dmg(calc_dmg_obj(tot_attr, 1.60, []), tot_attr.crit_rate, tot_attr.crit_dmg)*skyward_atlas_attacks
    tot_dmg = na_ca_dmg + skill_dmg + burst_dmg  

    dps = tot_dmg/field_time
    #dps_wep = atlas_passive_dmg/atlas_field_time
    print(dps) #+ dps_wep)

# (39.2%*2+244%+69.4%)*5 , 5 (normal + charged)
# (39.2%*2+244%+69.4%)*4 + 244%+69.4%*7, 4 normal + charged + 1 charged
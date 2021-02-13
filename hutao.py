from utils import calc_dmg, calc_dmg_obj, calc_avg_crit_dmg_obj, AttrObj, DmgTag, calc_tot_atk

# Strongly based on Zakharov's sheets https://docs.google.com/spreadsheets/d/1RAz3jx4x1ThWED8XWg8GKIf73RjPrZrnSukYZUCSRU8/edit#gid=383481181

'''
4pc Crimson Witch		
HP%, Pyro%, Crit Rate/Crit Damage		
E + N4 x 4 + Q
(80+21)/60*4 = 6.733
'''

'''
Hero Level	80
Enemy Level	80
Enemy Elem Res	10.0%
Enemy Phys Res	10.0%
'''

'''
Determine best NA combo (N4), 21 frames for dash cancel (determined it was n4)
na_mv = [.6447, .6635, .8394, .9026, .9415, 1.1819]

na_frames = [14, 25, 51, 80, 116, 184]
for i in range(6):
    print(sum(na_mv[:i+1])/(na_frames[i]+21)*60)
'''
n4_time = (80 + 21)/60 # From Hail + 21 for dash cancel

# E lasts for 9 seconds
field_time = n4_time*4 + 1.5 + .3 # assuming 1.5 sec for burst cast and .3 for skill cast
resist_down = 0

low_hp = 0 # 0 when HP > 50% , 1 when HP is  < 50%

cw_avg_stacks = 1
dm_1_opp = .5
liyue_chars = 2.0
a4_uptime = 1
base_hp = 13721

cr_main_stats = AttrObj(flat_atk=311, hp_pct=.466, crit_rate=.311, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)
cd_main_stats = AttrObj(flat_atk=311, hp_pct=.466, crit_dmg=.622, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)

artifact_substats = AttrObj(flat_atk=50, atk_pct=.249, crit_rate=.198, crit_dmg=.396, em=99, er=.275, flat_hp=762, hp_pct=.149, flat_def=59, def_pct=.186)
artifact_set_effects = AttrObj(dmg_bonus={DmgTag.PYRO: .15 + .15*.5*cw_avg_stacks}) # cw

char_attr = AttrObj(base_atk=94, crit_rate=.05, crit_dmg=.788, dmg_bonus={DmgTag.PYRO: low_hp*.33}) #crit dmg ascension stat, a4

#archaic_attr = AttrObj(base_atk=565, atk_pct=.276) # archaic, lvl 90/90, phys procs later
dm_attr = AttrObj(base_atk=454, crit_rate=.368, atk_pct=.16+.08*dm_1_opp) # deathmatch , lvl 90/90
homa_attr = AttrObj(base_atk=608, hp_pct=.2, crit_dmg=.662) # Homa, lvl 90/90


weapons = {
    "Deathmatch": (dm_attr, cd_main_stats, False), # (weapon attributes, artifacts, is it homa?)
    "Homa": (homa_attr, cr_main_stats, True)
}

for weapon_name, weapon in weapons.items():
    print(weapon_name)
    weapon_attr, artifact_main_stats, is_homa = weapon

    tot_attr = char_attr + weapon_attr + artifact_main_stats + artifact_substats + artifact_set_effects
    tot_hp = calc_tot_atk(base_hp, tot_attr.hp_pct, tot_attr.flat_hp)
    
    # Adds additional flat attack from e skill and homa passive
    skill_flat_atk = tot_hp*.0506
    if skill_flat_atk > 4*tot_attr.base_atk:
        print('Exceeds atk limit')
    tot_attr.flat_atk += skill_flat_atk
    if is_homa:
        tot_attr.flat_atk += .008*tot_hp + .01*low_hp*tot_hp # only for homa

    print(tot_attr)
    
    na_ca_dmg = calc_avg_crit_dmg_obj(tot_attr, (.6447 + .6635 + .8394 + .9026), [DmgTag.PYRO], enemy_resist_pct=.1-resist_down)*4 # 4 N4's

    #print(na_ca_dmg)
    skill_dmg = calc_avg_crit_dmg_obj(tot_attr, .896, [DmgTag.PYRO, DmgTag.SKILL], enemy_resist_pct=.1-resist_down)*2 # 2 blood blossoms
    #print(skill_dmg)

    burst_dmg = calc_avg_crit_dmg_obj(tot_attr, 4.994 if low_hp else 3.9952, [DmgTag.PYRO, DmgTag.BURST], enemy_resist_pct=.1-resist_down)*1
    #print(burst_dmg)

    tot_dmg = na_ca_dmg + skill_dmg + burst_dmg  

    dps = tot_dmg/field_time
    print("DPS:", dps)
    print()
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
# Frames counteed from myself
skill_cast_time = 16/25 
burst_cast_time = 55/25 
# 2.84 seconds total

n4c_time = 58/25
n4c_casts = 2
n1c_time = 27/25 
n1c_casts = 5
# E lasts for 9 seconds

resist_down = 0

low_hp = 1 # 0 when HP > 50% , 1 when HP is  < 50%
use_bennet = 0 # 0 when excluding bennet atk buff, 1 when including

cw_avg_stacks = 1
liyue_chars = 2.0
a4_uptime = 1
base_hp = 13721

cr_main_stats = AttrObj(flat_atk=311, hp_pct=.466, crit_rate=.311, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)
cd_main_stats = AttrObj(flat_atk=311, hp_pct=.466, crit_dmg=.622, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)

artifact_substats = AttrObj(flat_atk=50, atk_pct=.249, crit_rate=.198, crit_dmg=.396, em=99, er=.275, flat_hp=762, hp_pct=.149, flat_def=59, def_pct=.186)
artifact_set_effects = AttrObj(dmg_bonus={DmgTag.PYRO: .15 + .15*.5*cw_avg_stacks}) # cw
#artifact_set_effects = AttrObj(dmg_bonus={DmgTag.NORMAL: .4}) # bolide 100% shield uptime

char_attr = AttrObj(base_atk=94, crit_rate=.05, crit_dmg=.788, dmg_bonus={DmgTag.PYRO: low_hp*.33}) #crit dmg ascension stat, a4

#archaic_attr = AttrObj(base_atk=565, atk_pct=.276) # archaic, lvl 90/90, phys procs later
wt_attr = AttrObj(base_atk=401, crit_rate=.221, dmg_bonus={DmgTag.NORMAL: .48}) # white tassel R5, lvl 90/90
bt_attr = AttrObj(base_atk=354, hp_pct=.469) # black tassel, lvl 90/90, assuming not slimes
dm_solo_attr = AttrObj(base_atk=454, crit_rate=.368, atk_pct=.16+.08) # deathmatch R1, lvl 90/90 < 2 enemy
dm_multi_attr = AttrObj(base_atk=454, crit_rate=.368, atk_pct=.16) # deathmatch R1, lvl 90/90 >= 2 enemy
homa_attr = AttrObj(base_atk=608, hp_pct=.2, crit_dmg=.662) # Homa R1, lvl 90/90
pjws0_attr = AttrObj(base_atk=674, crit_rate=.221) # Jade Winged Spear R1, 0 stacks, lvl 90/90
pjws7_attr = AttrObj(base_atk=674, crit_rate=.221, atk_pct=.224, dmg_bonus={DmgTag.PYRO: .12}) # Jade Winged Spear R1, 7 stacks, lvl 90/90, remember to change from PYRO if not all abilies/attacks are pyro


# (weapon attributes, artifacts, is it homa?)
weapons = {
    "White Tassel": (wt_attr, cr_main_stats, False),
    "Black Tassel": (bt_attr, cr_main_stats, False),
    "Deathmatch (Solo)": (dm_solo_attr, cd_main_stats, False), 
    "Deathmatch (Multi)": (dm_multi_attr, cd_main_stats, False), 
    "Homa": (homa_attr, cr_main_stats, True),
    "Jade Winged Spear (0 stacks)": (pjws0_attr, cr_main_stats, False),
    "Jade Winged Spear (7 stacks)": (pjws7_attr, cr_main_stats, False)
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
    
    # Hail's Puretao
    # Bennet baseatk 80/80 169, 90/90 191, t6: 78.4, t8: 90, t10: 101
    # Festering 510 90/90 Favonius 454
    bennet_base_atk = 169 + 510
    bennet_atk_bonus = bennet_base_atk * .784
    tot_attr.flat_atk += bennet_atk_bonus * use_bennet
    
    n4_mv = .6447 + .6635 + .8394 + .9026
    n1_mv = .6647
    charge_mv = 1.8695

    charge_dmg = calc_avg_crit_dmg_obj(tot_attr, charge_mv, [DmgTag.PYRO, DmgTag.CHARGED], enemy_resist_pct=.1-resist_down)

    n4c_dmg = calc_avg_crit_dmg_obj(tot_attr, n4_mv, [DmgTag.PYRO, DmgTag.NORMAL], enemy_resist_pct=.1-resist_down)*n4c_casts # 2 N4C's
    n4c_dmg += charge_dmg*n4c_casts
    #print(n4c_dmg)

    n1c_dmg = calc_avg_crit_dmg_obj(tot_attr, n1_mv, [DmgTag.PYRO, DmgTag.NORMAL], enemy_resist_pct=.1-resist_down)*n1c_casts # 5 N1C's
    n1c_dmg += charge_dmg*n1c_casts
    #print(n1c_dmg)

    skill_dmg = calc_avg_crit_dmg_obj(tot_attr, .896, [DmgTag.PYRO, DmgTag.SKILL], enemy_resist_pct=.1-resist_down)*2 # 2 blood blossoms
    #print(skill_dmg)

    burst_dmg = calc_avg_crit_dmg_obj(tot_attr, 4.994 if low_hp else 3.9952, [DmgTag.PYRO, DmgTag.BURST], enemy_resist_pct=.1-resist_down)*1
    #print(burst_dmg)

    tot_n4c_dmg = n4c_dmg + skill_dmg + burst_dmg  
    tot_n1c_dmg = n1c_dmg + skill_dmg + burst_dmg

    n4c_dps = tot_n4c_dmg/(burst_cast_time + skill_cast_time + n4c_casts*n4c_time)
    n1c_dps = tot_n1c_dmg/(burst_cast_time + skill_cast_time + n1c_casts*n1c_time)

    print("N4C DPS:", n4c_dps)
    print("N1C DPS:", n1c_dps)
    print()
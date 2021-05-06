from utils import calc_dmg, calc_dmg_obj, calc_avg_crit_dmg_obj, AttrObj, DmgTag, calc_tot_atk, amp_react_mult

# Strongly based on Zakharov's sheets https://docs.google.com/spreadsheets/d/1RAz3jx4x1ThWED8XWg8GKIf73RjPrZrnSukYZUCSRU8/edit#gid=383481181

'''
Phys Carry
BSC2Glad2
ATK%, PHYS%, Crit Rate/Crit Damage		
N1C
'''

'''
Subdps
VV4

4E1Q
140 and 160 ER
'''

'''
Hero Level	80/90
Enemy Level	80
Weapon level 90/90
Talent Level 8
Enemy Elem Res	10.0%
Enemy Phys Res	10.0%
'''
#Phys carry N1C

na8_mv = [.8261, .7791, 1.0305, 1.126, 1.3539]
charge8_mv = 2.7695
skill8_mv = 4.672
burst8_mv = 6.7968
burst_wall8_mv = 1.2544
wall_hits = 1

burst_heal8_mv = 4.0192 # 2888 flat
cont_heal8_mv = .4019 # 289 flat

n1c_dur = 1 # TODO fix this
eeeeq_dur =  1 # TODO fix this

resist_down = 0


cr_main_stats = AttrObj(flat_atk=311, hp_pct=.466, crit_rate=.311, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)
cd_main_stats = AttrObj(flat_atk=311, hp_pct=.466, crit_dmg=.622, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)
bsc2glad2_set_effects = AttrObj(dmg_bonus={DmgTag.PHYS: .25}, atk_pct=.18)

char_attr = AttrObj(base_hp=13662, base_atk=222, base_def=769, crit_rate=.05, crit_dmg=.5) # healing bonus not included

def n1c_dps(weapon_attr, artifact_main_stats, artifact_substats, artifact_set_effects, supress=False):
    tot_attr = char_attr + weapon_attr + artifact_main_stats + artifact_substats + artifact_set_effects
    charge_dmg = calc_avg_crit_dmg_obj(tot_attr, charge8_mv, [DmgTag.PHYS, DmgTag.CHARGED], enemy_resist_pct=.1-resist_down, supress=supress)
    n1_dmg =  calc_avg_crit_dmg_obj(tot_attr, na8_mv[0], [DmgTag.PHYS, DmgTag.NORMAL], enemy_resist_pct=.1-resist_down, supress=supress)
    n1c_dmg = n1_dmg + charge_dmg
    return n1c_dmg/n1c_dur

def eeeeq_dps(weapon_attr, artifact_main_stats, artifact_substats, artifact_set_effects, supress=False):
    tot_attr = char_attr + weapon_attr + artifact_main_stats + artifact_substats + artifact_set_effects
    e_dmg = calc_avg_crit_dmg_obj(tot_attr, skill8_mv, [DmgTag.ANEMO, DmgTag.SKILL], enemy_resist_pct=.1-resist_down, supress=supress)
    q_dmg = calc_avg_crit_dmg_obj(tot_attr, burst8_mv, [DmgTag.ANEMO, DmgTag.BURST], enemy_resist_pct=.1-resist_down, supress=supress)
    wall_dmg = calc_avg_crit_dmg_obj(tot_attr, burst_wall8_mv, [DmgTag.ANEMO, DmgTag.BURST], enemy_resist_pct=.1-resist_down, supress=supress)
    eeeeq_dmg = e_dmg*4 + q_dmg + wall_dmg*wall_hits
    return eeeeq_dmg/eeeeq_dur

rancour_stacks = 4

if __name__ == '__main__':
    rancour_attr = AttrObj(base_atk=565, dmg_bonus={DmgTag.PHYS: .345}, atk_pct=rancour_stacks*.04, def_pct=rancour_stacks*.04)
    print(n1c_dps(rancour_attr, cr_main_stats, AttrObj(), bsc2glad2_set_effects))
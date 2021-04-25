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

burst_heal8_mv = 4.0192 # 2888 flat
cont_heal8_mv = .4019 # 289 flat

resist_down = 0


cr_main_stats = AttrObj(flat_atk=311, hp_pct=.466, crit_rate=.311, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)
cd_main_stats = AttrObj(flat_atk=311, hp_pct=.466, crit_dmg=.622, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)
em_cr_main_stats = AttrObj(flat_atk=311, em=187, crit_rate=.311, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)
em_cd_main_stats = AttrObj(flat_atk=311, em=187, crit_dmg=.622, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)

artifact_substats = AttrObj(flat_atk=50, atk_pct=.149, crit_rate=.198, crit_dmg=.396, em=99, er=.275, flat_hp=762, hp_pct=.249, flat_def=59, def_pct=.186)
artifact_set_effects = AttrObj(dmg_bonus={DmgTag.PYRO: .15 + .15*.5*cw_avg_stacks}) # cw

dm_attr = AttrObj(base_atk=454, crit_rate=.368, atk_pct=.16+.08*dm_1_opp) # deathmatch R1, lvl 90/90


if __name__ == '__main__':
    n3c_burst_dps, _, _, _ = n3cq_dps(dm_attr, cr_main_stats, artifact_substats, artifact_set_effects, vape_bonus=.15, low_hp=0, is_homa=False)
    print("Deathmatch N3C Burst DPS:", n3c_burst_dps)
    #print("N3C DPS:", n3c_dps)
    print()

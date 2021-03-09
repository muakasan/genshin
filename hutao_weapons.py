from utils import calc_dmg, calc_dmg_obj, calc_avg_crit_dmg_obj, AttrObj, DmgTag, calc_tot_atk, amp_react_mult
from hutao import n3cq_dps, n3c_casts
from artifact_optimizer import perf_art_optim
from artifacts import MainstatType, SubstatType

# Strongly based on Zakharov's sheets https://docs.google.com/spreadsheets/d/1RAz3jx4x1ThWED8XWg8GKIf73RjPrZrnSukYZUCSRU8/edit#gid=383481181
# DM High HP should be 15262, Homa 17311 
'''
4pc Crimson Witch		
HP%, Pyro%, Crit Rate/Crit Damage		
E + N3C x 5 + Q
'''

'''
Hero Level	80
Enemy Level	80
Enemy Elem Res	10.0%
Enemy Phys Res	10.0%
'''

na6_mv = [.6447, .6635, .8394, .9026, .9415, 1.1819]
charge6_mv = 1.8695
skill6_mv = .896
low_hp_burst6_mv = 4.994
high_hp_burst6_mv = 3.9952

na8_mv = [.7406, .7622, .9643, .10368, 1.0816, 1.3578]
charge8_mv = 2.1476
skill8_mv = 1.024
low_hp_burst8_mv = 5.5842
high_hp_burst8_mv = 4.4674

# Frames counted by Artesians and JinJinx
skill_cast_time = 30/60 
burst_cast_time = 99/60 

n3c_time = 110/60
n3c_casts = 5
n1_vapes = 4 
n2_vapes = 0
n3_vapes = 3

resist_down = 0

low_hp = 1 # 0 when HP > 50% , 1 when HP is  < 50%
use_bennet = 0 # 0 when excluding bennet atk buff, 1 when including

cw_avg_stacks = 1
dm_1_opp = .5
liyue_chars = 3.0
vv_stacks = 5
dbane_passive_uptime = 1

cr_main_stats = AttrObj(flat_atk=311, hp_pct=.466, crit_rate=.311, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)
cd_main_stats = AttrObj(flat_atk=311, hp_pct=.466, crit_dmg=.622, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)
em_cr_main_stats = AttrObj(flat_atk=311, em=187, crit_rate=.311, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)
em_cd_main_stats = AttrObj(flat_atk=311, em=187, crit_dmg=.622, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)

artifact_substats = AttrObj()
artifact_set_effects = AttrObj(dmg_bonus={DmgTag.PYRO: .15 + .15*.5*cw_avg_stacks}) # cw

wt_attr = AttrObj(base_atk=401, crit_rate=.221, dmg_bonus={DmgTag.NORMAL: .48}) # white tassel R5, lvl 90/90
bt_attr = AttrObj(base_atk=354, hp_pct=.469) # black tassel, lvl 90/90, assuming not slimes
dm_2enem_attr = AttrObj(base_atk=454, crit_rate=.368, atk_pct=.16) # deathmatch R1, lvl 90/90
dm_solo_attr = AttrObj(base_atk=454, crit_rate=.368, atk_pct=.16+.08) # deathmatch R1, lvl 90/90
homa_attr = AttrObj(base_atk=608, hp_pct=.2, crit_dmg=.662) # Homa R1, lvl 90/90
pjws0_attr = AttrObj(base_atk=674, crit_rate=.221) # Jade Winged Spear R1, 0 stacks, lvl 90/90
pjws6_attr = AttrObj(base_atk=674, atk_pct=6*.032, crit_rate=.221, dmg_bonus={DmgTag.PYRO: .12}) # Jade Winged Spear R1, 7 stacks, lvl 90/90, remember to change from PYRO if not all abilies/attacks are pyro
pjws7_attr = AttrObj(base_atk=674, crit_rate=.221, atk_pct=7*.032, dmg_bonus={DmgTag.PYRO: .12}) # Jade Winged Spear R1, 7 stacks, lvl 90/90, remember to change from PYRO if not all abilies/attacks are pyro
vv_attr = AttrObj(base_atk=608, atk_pct=.496 + vv_stacks*.04) 
vv_shield_attr = AttrObj(base_atk=608, atk_pct=.496 + vv_stacks*2*.04)
db_attr = AttrObj(base_atk=454, em=221, dmg_bonus={DmgTag.PYRO: .20*dbane_passive_uptime}) 
db5_attr = AttrObj(base_atk=454, em=221, dmg_bonus={DmgTag.PYRO: .36*dbane_passive_uptime}) 
db_bonusless_attr = AttrObj(base_atk=454, em=221)
lithic2_attr = AttrObj(base_atk=565, atk_pct=.276 + 2*.07, crit_rate=.03*2)
lithic4_attr = AttrObj(base_atk=565, atk_pct=.276 + 4*.07, crit_rate=.03*4)
lithic2_5_attr = AttrObj(base_atk=565, atk_pct=.276 + 2*.11, crit_rate=.07*2)
lithic4_5_attr = AttrObj(base_atk=565, atk_pct=.276 + 4*.11, crit_rate=.07*4)
bc0 = AttrObj(base_atk=510, crit_dmg=.551)
bc3 = AttrObj(base_atk=510, atk_pct=.12*3, crit_dmg=.551)
sspine = AttrObj(base_atk=674, er=.368, crit_rate=.08)
if __name__ == '__main__':
    # (weapon attributes, artifacts, is it homa?)
    weapons = {
        "White Tassel (R5)": (wt_attr, cr_main_stats, False, False),
        "Black Tassel": (bt_attr, cr_main_stats, False, False),
        "Deathmatch (2 Enemies)": (dm_2enem_attr, cd_main_stats, False, False), 
        "Deathmatch (Solo)": (dm_solo_attr, cd_main_stats, False, False), 
        "DBane": (db_attr, cr_main_stats, False, False),
        "DBane R5": (db5_attr, cr_main_stats, False, False),
        "DBane (no bonus)": (db_bonusless_attr, cr_main_stats, False, False),
        "Vortex Vanquisher (5 stacks, No Shield)": (vv_attr, cr_main_stats, False, False), 
        "Vortex Vanquisher (5 stacks, Shield)": (vv_shield_attr, cr_main_stats, False, False), 
        "Homa": (homa_attr, cr_main_stats, True, False),
        "Jade Winged Spear (0 stacks)": (pjws0_attr, cr_main_stats, False, False),
        "Jade Winged Spear (6 stacks)": (pjws6_attr, cr_main_stats, False, False),
        "Jade Winged Spear (7 stacks)": (pjws7_attr, cr_main_stats, False, False),
        "Lithic Spear (2 Liyue)": (lithic2_attr, cr_main_stats, False, False),
        "Lithic Spear (4 Liyue)": (lithic4_5_attr, cr_main_stats, False, False),
        "Lithic Spear (2 Liyue)": (lithic2_5_attr, cr_main_stats, False, False),
        "Lithic Spear (4 Liyue)": (lithic4_attr, cr_main_stats, False, False),
        "Blackcliff (0 stacks)": (lithic2_attr, cr_main_stats, False, False),
        "Blackcliff (3 stacks)": (lithic4_attr, cr_main_stats, False, False),
        "Skyward Spine": (sspine, cr_main_stats, False, True),
    }
    low_hp = 1
    char_attr = AttrObj(base_atk=99, base_hp=14459, crit_rate=.05, crit_dmg=.884, dmg_bonus={DmgTag.PYRO: low_hp*.33})
    for weapon_name, weapon in weapons.items():
        print(weapon_name, "(Mainstats Only)")
        weapon_attr, artifact_main_stats, is_homa, is_sspine = weapon
        n3c_burst_dps, _, _, _ = n3cq_dps(weapon_attr, artifact_main_stats, artifact_substats, artifact_set_effects, char_attr=char_attr, talent=8, vape=True, vape_bonus=.15, low_hp=low_hp, is_homa=is_homa, is_sspine=is_sspine)
        print("N3C Burst DPS:", n3c_burst_dps)
        #print("N3C DPS:", n3c_dps)
        print(weapon_name, "(Perf. Subs)")

        weapon_attr, artifact_main_stats, is_homa, is_sspine = weapon
        dps_func = lambda art_mains, art_subs: n3cq_dps(weapon_attr, art_mains, art_subs, artifact_set_effects, char_attr=char_attr, talent=8, vape=True, vape_bonus=.15, low_hp=low_hp, is_homa=is_homa, is_sspine=is_sspine, supress=True)
        perf_art_optim(dps_func, sandss=[MainstatType.HP_PCT], goblets=["PYRO"], circlets=[MainstatType.CRIT_DMG, MainstatType.CRIT_RATE], 
            substats=[SubstatType.CRIT_RATE, SubstatType.CRIT_DMG, SubstatType.EM, SubstatType.HP_PCT])
        #        n3c_burst_dps, _, _, _ = 
        print("N3C Burst DPS:", n3c_burst_dps)
        
        print()

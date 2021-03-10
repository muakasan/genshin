from utils import calc_dmg, calc_dmg_obj, calc_avg_crit_dmg_obj, AttrObj, DmgTag, calc_tot_atk, amp_react_mult
from hutao import n3cq_dps, n3c_casts
from artifact_optimizer import perf_art_optim
from artifacts import MainstatType, SubstatType

# Strongly based on Zakharov's sheets https://docs.google.com/spreadsheets/d/1RAz3jx4x1ThWED8XWg8GKIf73RjPrZrnSukYZUCSRU8/edit#gid=383481181

cw_avg_stacks = 1
vv_stacks = 5
dbane_passive_uptime = 1

cr_main_stats = AttrObj(flat_atk=311, hp_pct=.466, crit_rate=.311, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)
cd_main_stats = AttrObj(flat_atk=311, hp_pct=.466, crit_dmg=.622, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)
em_cr_main_stats = AttrObj(flat_atk=311, em=187, crit_rate=.311, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)
em_cd_main_stats = AttrObj(flat_atk=311, em=187, crit_dmg=.622, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)
artifact_substats = AttrObj()
artifact_set_effects = AttrObj(dmg_bonus={DmgTag.PYRO: .15 + .15*.5*cw_avg_stacks}) # Crimson Witch (Vape bonus manually added later)

wt_attr = AttrObj(base_atk=401, crit_rate=.221, dmg_bonus={DmgTag.NORMAL: .48}) # white tassel R5, lvl 90/90
bt_attr = AttrObj(base_atk=354, hp_pct=.469) # black tassel, lvl 90/90, assuming not slimes

dm_2enem_attr = AttrObj(base_atk=454, crit_rate=.368, atk_pct=.16, def_pct=.16) # deathmatch R1, lvl 90/90
dm_solo_attr = AttrObj(base_atk=454, crit_rate=.368, atk_pct=.24) # deathmatch R1, lvl 90/90
db_attr = AttrObj(base_atk=454, em=221, dmg_bonus={DmgTag.PYRO: .20*dbane_passive_uptime})  # Dragon's bane: remember to change from PYRO if not all abilies/attacks are pyro
db5_attr = AttrObj(base_atk=454, em=221, dmg_bonus={DmgTag.PYRO: .36*dbane_passive_uptime}) # Dragon's bane: remember to change from PYRO if not all abilies/attacks are pyro
db_bonusless_attr = AttrObj(base_atk=454, em=221)
lithic2_attr = AttrObj(base_atk=565, atk_pct=.276 + 2*.07, crit_rate=.03*2)
lithic4_attr = AttrObj(base_atk=565, atk_pct=.276 + 4*.07, crit_rate=.03*4)
lithic2_5_attr = AttrObj(base_atk=565, atk_pct=.276 + 2*.11, crit_rate=.07*2)
lithic4_5_attr = AttrObj(base_atk=565, atk_pct=.276 + 4*.11, crit_rate=.07*4)
bc0_attr = AttrObj(base_atk=510, crit_dmg=.551)
bc3_attr = AttrObj(base_atk=510, atk_pct=.12*3, crit_dmg=.551)

homa_attr = AttrObj(base_atk=608, hp_pct=.2, crit_dmg=.662) # Homa R1, lvl 90/90
pjws0_attr = AttrObj(base_atk=674, crit_rate=.221) # Jade Winged Spear R1, 0 stacks, lvl 90/90
pjws6_attr = AttrObj(base_atk=674, atk_pct=6*.032, crit_rate=.221) # Jade Winged Spear R1, 6 stacks, lvl 90/90
pjws7_attr = AttrObj(base_atk=674, atk_pct=7*.032, crit_rate=.221, dmg_bonus={DmgTag.PYRO: .12}) # Jade Winged Spear R1, 7 stacks, lvl 90/90, remember to change from PYRO if not all abilies/attacks are pyro
vv_attr = AttrObj(base_atk=608, atk_pct=.496 + vv_stacks*.04) 
vv_shield_attr = AttrObj(base_atk=608, atk_pct=.496 + vv_stacks*2*.04)
sspine = AttrObj(base_atk=674, er=.368, crit_rate=.08)
if __name__ == '__main__':
    # (weapon attributes, artifacts, is it homa?)
    weapons = {
        "White Tassel (R5)": (wt_attr, cr_main_stats, False, False),
        "Black Tassel": (bt_attr, cr_main_stats, False, False),
        "Deathmatch (2 Enemies)": (dm_2enem_attr, cr_main_stats, False, False), 
        "Deathmatch (Solo)": (dm_solo_attr, cr_main_stats, False, False), 
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
        "Lithic Spear (4 Liyue)": (lithic4_attr, cr_main_stats, False, False),
        "Lithic Spear (R5) (2 Liyue)": (lithic2_5_attr, cr_main_stats, False, False),
        "Lithic Spear (R5) (4 Liyue)": (lithic4_5_attr, cr_main_stats, False, False),
        "Blackcliff (0 stacks)": (bc0_attr, cr_main_stats, False, False),
        "Blackcliff (3 stacks)": (bc3_attr, cr_main_stats, False, False),
        "Skyward Spine": (sspine, cr_main_stats, False, True),
    }
    low_hp = 1 # 0 when HP > 50% , 1 when HP is  < 50%
    char_attr = AttrObj(base_atk=99, base_hp=14459, crit_rate=.05, crit_dmg=.884, dmg_bonus={DmgTag.PYRO: low_hp*.33})
    for weapon_name, weapon in weapons.items():
        weapon_attr, artifact_main_stats, is_homa, is_sspine = weapon
        n3c_burst_dps, _, _, _ = n3cq_dps(weapon_attr, artifact_main_stats, artifact_substats, artifact_set_effects, char_attr=char_attr, talent=8, vape=True, vape_bonus=.15, low_hp=low_hp, is_homa=is_homa, is_sspine=is_sspine)
        print(weapon_name, "(Mainstats Only):", n3c_burst_dps)

        weapon_attr, artifact_main_stats, is_homa, is_sspine = weapon
        dps_func = lambda art_mains, art_subs: n3cq_dps(weapon_attr, art_mains, art_subs, artifact_set_effects, char_attr=char_attr, talent=8, vape=True, vape_bonus=.15, low_hp=low_hp, is_homa=is_homa, is_sspine=is_sspine, supress=True)
        highest_dps, highest_mainstat_attr, highest_substat_attr, highest_substat_dist, highest_tot_attr = perf_art_optim(dps_func, 
            sandss=[MainstatType.HP_PCT], goblets=["PYRO"], circlets=[MainstatType.CRIT_DMG, MainstatType.CRIT_RATE], 
            substats=[SubstatType.CRIT_RATE, SubstatType.CRIT_DMG, SubstatType.EM, SubstatType.HP_PCT])
        print(weapon_name, "(Perfect Subs):", highest_dps)
        print("Substats:\n", highest_substat_attr)
        print("Main Stats:\n",  highest_mainstat_attr)
        print("Total Stats:\n", highest_tot_attr)

        print()

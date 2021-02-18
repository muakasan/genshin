from utils import calc_dmg, calc_dmg_obj, calc_avg_crit_dmg_obj, AttrObj, DmgTag, calc_tot_atk, avg_crit_dmg

# Strongly based on Zakharov's sheets https://docs.google.com/spreadsheets/d/1RAz3jx4x1ThWED8XWg8GKIf73RjPrZrnSukYZUCSRU8/edit#gid=383481181

# ZL A4 na: .0139, e: .019, q: .33
# https://genshin.honeyhunterworld.com/db/char/zhongli/
# https://genshin.honeyhunterworld.com/db/char/xiao/

'''
Hero Level	80
Enemy Level	80
Enemy Elem Res	10.0%
Enemy Phys Res	10.0%
'''
zl_na_times = [0.050,0.433,0.600,1.150,1.583,1.683,1.783,1.883,2.317] # MVs are from Robin's sheet https://github.com/RobinGenshin/DPSSIM/blob/main/data/Characters.csv
zl_na_mvs = [.4472, .4528, .5607, .6241, .1563, .1563, .1563, .1563, .7921] 

xiao_na_times = [0.050,0.267,0.617,0.967,1.367,1.650,2.033,2.850]
xiao_na_mvs = [.3787, .3787, .7829, .9426, .5179, .5179, .9837, .13177]

zl_hits = 4 + 4 # N5
xiao_hits = 4 # 4 hits is best N3

zl_field_time = zl_na_times[zl_hits-1] + 21/60
xiao_field_time = xiao_na_times[xiao_hits-1] + 21/60 
anemo_xiao_field_time = 1.28 # From artesian's frame counts (slowest high plunge spam) https://docs.google.com/spreadsheets/d/1PN0WgqENUfV8i5hnrz1BOEU56fk7m8FYlFXzFzrsS3k/edit#gid=1742366399

dm_1_opp = .5

resist_down = 0

base_hp = 12965

cr_main_stats = AttrObj(flat_atk=311, atk_pct=.466, crit_rate=.311, dmg_bonus={DmgTag.PHYS: .583}, flat_hp=4780)
cd_main_stats = AttrObj(flat_atk=311, atk_pct=.466, crit_dmg=.622, dmg_bonus={DmgTag.PHYS: .583}, flat_hp=4780)
cd_anemo_main_stats = AttrObj(flat_atk=311, atk_pct=.466, crit_dmg=.622, dmg_bonus={DmgTag.ANEMO: .466}, flat_hp=4780)

artifact_substats = AttrObj(flat_atk=50, atk_pct=.249, crit_rate=.198, crit_dmg=.396, em=99, er=.275, flat_hp=762, hp_pct=.149, flat_def=59, def_pct=.186)
artifact_set_effects = AttrObj(atk_pct=.18, dmg_bonus={DmgTag.PHYS: .25}) # glad2 bsc2

xiao_attr = AttrObj(base_atk=308, crit_rate=.194, crit_dmg=.5)
zl_attr = AttrObj(base_atk=222, crit_rate=.05, crit_dmg=.5, dmg_bonus={DmgTag.GEO: .216})

cp_attr = AttrObj(base_atk=565, dmg_bonus={DmgTag.PHYS: .345}) # crescent pike , lvl 90/90
dm_attr = AttrObj(base_atk=454, crit_rate=.368, atk_pct=.16+.08*dm_1_opp) # deathmatch R1, lvl 90/90

xiao_burst = AttrObj(dmg_bonus={DmgTag.CHARGED: .77})

tot_zl_attr = zl_attr + cp_attr + cr_main_stats + artifact_substats
tot_xiao_attr = xiao_attr + cp_attr + cr_main_stats + artifact_substats
tot_anemo_xiao_attr = xiao_attr + dm_attr + cd_anemo_main_stats + artifact_substats + xiao_burst

zl_na_dmg = calc_avg_crit_dmg_obj(tot_zl_attr, sum(zl_na_mvs[:zl_hits]), [DmgTag.PHYS, DmgTag.NORMAL], enemy_resist_pct=.1-resist_down)
zl_cp_dmg = calc_avg_crit_dmg_obj(tot_zl_attr, .2, [DmgTag.PHYS], enemy_resist_pct=.1-resist_down)*zl_hits #.2 for r1 .4 for r5
zl_a4_dmg = avg_crit_dmg(
    calc_dmg(base_atk=base_hp, atk_pct=tot_zl_attr.hp_pct, flat_atk=tot_zl_attr.flat_hp, ability_mult=.0139, dmg_bonus_pct=tot_zl_attr.dmg_bonus[DmgTag.PHYS], enemy_resist_pct=.1-resist_down),
    tot_zl_attr.crit_rate, tot_zl_attr.crit_dmg)*zl_hits
print(zl_na_dmg, zl_cp_dmg, zl_a4_dmg)

xiao_na_dmg = calc_avg_crit_dmg_obj(tot_xiao_attr, sum(xiao_na_mvs[:xiao_hits]), [DmgTag.PHYS, DmgTag.NORMAL], enemy_resist_pct=.1-resist_down)
xiao_cp_dmg = calc_avg_crit_dmg_obj(tot_xiao_attr, .2, [DmgTag.PHYS], enemy_resist_pct=.1-resist_down)*xiao_hits

anemo_xiao_dmg = calc_avg_crit_dmg_obj(tot_anemo_xiao_attr, 2.97, [DmgTag.ANEMO, DmgTag.CHARGED], enemy_resist_pct=.1-resist_down) # should change charged to plunge
'''
#print(na_ca_dmg)
skill_dmg = calc_avg_crit_dmg_obj(tot_attr, .896, [DmgTag.PYRO, DmgTag.SKILL], enemy_resist_pct=.1-resist_down)*2 # 2 blood blossoms
#print(skill_dmg)

burst_dmg = calc_avg_crit_dmg_obj(tot_attr, 4.994 if low_hp else 3.9952, [DmgTag.PYRO, DmgTag.BURST], enemy_resist_pct=.1-resist_down)*1
#print(burst_dmg)

'''  
zl_tot_dmg = zl_na_dmg + zl_cp_dmg + zl_a4_dmg  
xiao_tot_dmg = xiao_na_dmg + xiao_cp_dmg

print("ZL:", zl_tot_dmg/zl_field_time)
print("Xiao:", xiao_tot_dmg/xiao_field_time)
print("Anemo Xiao:", anemo_xiao_dmg/anemo_xiao_field_time)
from utils import calc_dmg, calc_dmg_obj, calc_avg_crit_dmg_obj, AttrObj, DmgTag, calc_tot_atk, amp_react_mult

# REMOVE THE FEATHER TO GET RID OF 4 PC CW

na6_mv = [.6447, .6635, .8394, .9026, .9415, 1.1819]
charge6_mv = 1.8695
skill6_mv = .896
low_hp_burst6_mv = 4.994
high_hp_burst6_mv = 3.9952
hp_to_atk6 = .0506


na8_mv = [.7406, .7622, .9643, 1.0368, 1.0816, 1.3578]
charge8_mv = 2.1476
skill8_mv = 1.024
low_hp_burst8_mv = 5.5842
high_hp_burst8_mv = 4.4674
hp_to_atk8 = .0566

# https://docs.google.com/spreadsheets/d/1tXwNi_TPojdocCIci3v6nhd87kNwsmFpOjxJS3NKMKs/edit#gid=1353671486
# https://docs.google.com/spreadsheets/d/1PN0WgqENUfV8i5hnrz1BOEU56fk7m8FYlFXzFzrsS3k/edit#gid=565215807
# Frames counted by Artesians and JinJinx
skill_cast_time = 30/60 
burst_cast_time = 99/60 

n3c_sspine_time = 102/60
n3c_time = 108/60
n3c_casts = 5
n1_vapes = 4 
n2_vapes = 0
n3_vapes = 3
resist_down = 0



low_hp = 0 # 0 when HP > 50% , 1 when HP is  < 50%
cw_avg_stacks = 1 # Should be 1 or zero for hutao
dm_1_opp = 1
use_skill = False
use_bennet = True
use_noblesse = False

feather = AttrObj(flat_atk=258, crit_dmg=.194, flat_hp=209, atk_pct=.058, em=44)
flower = AttrObj(flat_hp=4780, crit_rate=.031, atk_pct=.14, crit_dmg=.117, er=.11)
sands = AttrObj(hp_pct=.466, flat_def=39, crit_dmg=.194, def_pct=.117, crit_rate=.078)
cup = AttrObj(dmg_bonus={DmgTag.PYRO: .466}, flat_hp=837, crit_rate=.066, hp_pct=.047, atk_pct=.111)
hat = AttrObj(crit_dmg=.622, flat_def=23, flat_atk=62, atk_pct=.099, flat_hp=299)

artifact_stats = flower + sands + cup + hat # + feather
#print('Artifact stats:', artifact_stats)
#artifact_set_effects = AttrObj(dmg_bonus={DmgTag.PYRO: .15 + .15*.5*cw_avg_stacks}) # cw
artifact_set_effects = AttrObj(dmg_bonus={DmgTag.PYRO: .15}) # 2P cw

char_lvl = 80
char_attr = AttrObj(base_atk=99, base_hp=14459, base_def=815, crit_rate=.05, crit_dmg=.884, dmg_bonus={DmgTag.PYRO: low_hp*.33}) #crit dmg ascension stat, a4, 80/90
skill_mv = skill8_mv
hp_to_atk = hp_to_atk8
high_hp_burst_mv = high_hp_burst6_mv

enemy_lvl = 85

bennet_base_atk = 666
bennet_atk_conv = .9 + .2# T8, .2 from C1 

#dm_attr = AttrObj(base_atk=454, crit_rate=.368, atk_pct=.16+.08*dm_1_opp) # deathmatch R1, lvl 90/90
dm_attr = AttrObj(base_atk=427, crit_rate=.335, atk_pct=.16+.08*dm_1_opp) # deathmatch R1, lvl 80/90
favlance_attr = AttrObj(base_atk=497, er=.279) # favlance R1, lvl 80/80
pyro_resonance =  AttrObj(atk_pct=.25)
tot_attr = artifact_stats + artifact_set_effects + char_attr + favlance_attr + pyro_resonance
print('No skill tot atk:', calc_tot_atk(tot_attr.base_atk, tot_attr.atk_pct, tot_attr.flat_atk))

print('total stats:', tot_attr)
if __name__ == '__main__':
    burst_mv = low_hp_burst_mv if low_hp else high_hp_burst_mv

    vape = False
    vape_mult = 1
    if vape:
        vape_mult = amp_react_mult(is_strong=False, em=tot_attr.em, bonus=vape_bonus) # vape, bonus from C
    crit_mult = tot_attr.crit_dmg + 1

    tot_hp = calc_tot_atk(tot_attr.base_hp, tot_attr.hp_pct, tot_attr.flat_hp)

    skill_flat_atk = tot_hp*hp_to_atk
    if skill_flat_atk > 4*tot_attr.base_atk:
        if not supress:
            print('Exceeds atk limit')
        skill_flat_atk = 4*tot_attr.base_atk
    if use_skill:
        tot_attr.flat_atk += skill_flat_atk
    
    print('skill tot atk', calc_tot_atk(tot_attr.base_atk, tot_attr.atk_pct, tot_attr.flat_atk))

    if use_bennet:
        bennet_flat_atk = bennet_atk_conv*bennet_base_atk
        tot_attr.flat_atk += bennet_flat_atk
    if use_noblesse:
        tot_attr.atk_pct += .2
    print(calc_tot_atk(tot_attr.base_atk, tot_attr.atk_pct, tot_attr.flat_atk))
    
    bb_dmg = calc_dmg_obj(tot_attr, skill_mv, [DmgTag.PYRO, DmgTag.SKILL], char_lvl=char_lvl, enemy_lvl=enemy_lvl, enemy_resist_pct=.1-resist_down)*vape_mult # 1 blood blossom that vapes
    burst_dmg = calc_dmg_obj(tot_attr, burst_mv, [DmgTag.PYRO, DmgTag.BURST], char_lvl=char_lvl, enemy_lvl=enemy_lvl, enemy_resist_pct=.1-resist_down)*vape_mult # 1 blood blossom that vapes
    #print(burst_dmg*crit_mult)
    print('bb dmg', bb_dmg)
    print('crit bb dmg', bb_dmg*crit_mult)
    print('burst dmg', burst_dmg)
    print('crit burst dmg', burst_dmg*crit_mult)

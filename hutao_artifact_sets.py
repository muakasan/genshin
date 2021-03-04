from utils import calc_dmg, calc_dmg_obj, calc_avg_crit_dmg_obj, AttrObj, DmgTag, ReactionType, calc_tot_atk, amp_react_mult, tf_react_dmg
from hutao import dm_attr, cd_main_stats, n3cq_dps, artifact_substats

cw_set_effects = AttrObj(dmg_bonus={DmgTag.PYRO: .15 + .15*.5})
tf_set_effects = AttrObj(dmg_bonus={DmgTag.ELECTRO: .15})
cw2glad2_set_effects = AttrObj(dmg_bonus={DmgTag.PYRO: .15}, atk_pct=.18)
cw2wt2_set_effects = AttrObj(dmg_bonus={DmgTag.PYRO: .15}, em=80)
cw2no2_set_effects = AttrObj(dmg_bonus={DmgTag.PYRO: .15, DmgTag.BURST: .20})

# artifact effects, should vape, vape bonus
artifact_sets = {
    "Crimson Witch 4": (cw_set_effects, True, .15),
    "Crimson Witch 2, Glad 2": (cw2glad2_set_effects, True, 0), 
    "Crimson Witch 2, Wanderer's 2": (cw2wt2_set_effects, True, 0),
    "Crimson Witch 2, Noblesse 2": (cw2no2_set_effects, True, 0),
    "Thundering Fury": (tf_set_effects, False, 0),
}


for set_name, (set_effects, should_vape, vape_bonus) in artifact_sets.items():
    _, dmg, dur = n3cq_dps(dm_attr, cd_main_stats, artifact_substats, set_effects, vape=should_vape, low_hp=0, vape_bonus=vape_bonus)
    if not should_vape:
        dmg += tf_react_dmg(ReactionType.OL, em=99, bonus=.40, char_lvl=80, enemy_resist_pct=.1)*6
    print(set_name, dmg/dur)
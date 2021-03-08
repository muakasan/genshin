from utils import calc_dmg, calc_dmg_obj, calc_avg_crit_dmg_obj, AttrObj, DmgTag, ReactionType, calc_tot_atk, amp_react_mult, tf_react_dmg
from hutao import dm_attr, cd_main_stats, n3cq_dps, artifact_substats

cw_set_effects = AttrObj(dmg_bonus={DmgTag.PYRO: .15 + .15*.5})
tf_set_effects = AttrObj(dmg_bonus={DmgTag.ELECTRO: .15})
cw2glad2_set_effects = AttrObj(dmg_bonus={DmgTag.PYRO: .15}, atk_pct=.18)
cw2wt2_set_effects = AttrObj(dmg_bonus={DmgTag.PYRO: .15}, em=80)
cw2no2_set_effects = AttrObj(dmg_bonus={DmgTag.PYRO: .15, DmgTag.BURST: .20})
cw2_set_effects = AttrObj(dmg_bonus={DmgTag.PYRO: .15})
bolide_set_effects = AttrObj(dmg_bonus={DmgTag.NORMAL: .40, DmgTag.CHARGED: .40})
lw_set_effects = AttrObj(dmg_bonus={DmgTag.PYRO: .35})

# artifact effects, should vape, vape bonus, add OL
artifact_sets = {
    "Crimson Witch 4": (cw_set_effects, True, .15, False),
    "Lavawalker (100% Pyro aura)": (lw_set_effects, False, 0, False),
    "Crimson Witch 2, Wanderer's 2": (cw2wt2_set_effects, True, 0, False),
    "Retracing Bolide (100% Shield)": (bolide_set_effects, True, 0, False),
    "Crimson Witch 2, Glad 2": (cw2glad2_set_effects, True, 0, False), 
    "Crimson Witch 2, Noblesse 2": (cw2no2_set_effects, True, 0, False),
    "Crimson Witch 2": (cw2_set_effects, True, 0, False),
    #"Thundering Fury": (tf_set_effects, False, 0, True),
}


for set_name, (set_effects, should_vape, vape_bonus, should_OL) in artifact_sets.items():
    _, dmg, dur, _ = n3cq_dps(dm_attr, cd_main_stats, artifact_substats, set_effects, vape=should_vape, low_hp=1, vape_bonus=vape_bonus)
    if should_OL:
        dmg += tf_react_dmg(ReactionType.OL, em=99, bonus=.40, char_lvl=80, enemy_resist_pct=.1)*6
    print(set_name, dmg/dur)
    print()

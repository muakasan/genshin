import itertools # https://stackoverflow.com/questions/798854/all-combinations-of-a-list-of-lists
from artifacts import SubstatType, MainstatType, avg_artifact_substat, artifact_mainstat
from utils import AttrObj

from hutao import dm_attr, cd_main_stats, n3cq_dps, artifact_set_effects # For testing

avg_flat_atk = avg_artifact_substat(SubstatType.FLAT_ATK)
avg_atk_pct = avg_artifact_substat(SubstatType.ATK_PCT)
avg_cr = avg_artifact_substat(SubstatType.CRIT_RATE)
avg_cd = avg_artifact_substat(SubstatType.CRIT_DMG)

# An artifact cannot have the same substat and mainstat
# this counts how many artifacts mainstats are different from the substat
def count_valid_artifacts(substat, sands, goblet, circlet):
    valid_artifacts = 5 # Starts with 5 because all are valid artifacts
    if substat == SubstatType.FLAT_ATK or substat == SubstatType.FLAT_HP:
        valid_artifacts -= 1
    for main_stat in [sands, goblet, circlet]:
        if substat == main_stat:
            valid_artifacts -= 1
    return valid_artifacts

# TODO currently does not work I think, does not handle initial substats properly I believe
# Zanto and ibvteh substat assumption, each art starts with 3 good stats, rolls into a good substat 3 times each for each artifact
def zi_art_optim(dps_func, sandss, goblets, circlets, substats):
    GOOD_ROLLS = 3
    BUDGET = 3*5 + 3*5 # initial + good rolls

    highest_dps = 0
    highest_substat_attr = None
    highest_substat_dist = None
    highest_mainstat_attr = None
    highest_tot_attr = None

    # Iterate through main stats
    count = 0
    for sands, goblet, circlet in itertools.product(sandss, goblets, circlets):

        avg_subs = {sub: avg_artifact_substat(sub) for sub in substats} # Gets the average substat roll value for each substat
        num_valid_arts = {sub: count_valid_artifacts(sub, sands, goblet, circlet) for sub in substats} # 
        #roll_counts = [range(num_valid_arts[sub], GOOD_ROLLS*num_valid_arts[sub] + 1) for sub in substats] #every one has all good stats?
        roll_counts = [range(0, GOOD_ROLLS*num_valid_arts[sub] + 1) for sub in substats]

        # mainstat_dist = {ms: artifact_mainstat(ms, star=5, lvl=20) for ms in [sandss, goblet, circlet]} # TODO does not account for multiple of the same main stat
        # hack to get around pyro type for now
        mainstat_attr = {ms: artifact_mainstat(ms, star=5, lvl=20) for ms in [sands, circlet]} # TODO does not account for multiple of the same main stat
        mainstat_attr = AttrObj(**mainstat_attr)
        mainstat_attr.flat_hp += artifact_mainstat(MainstatType.FLAT_HP, star=5, lvl=20)
        mainstat_attr.flat_atk += artifact_mainstat(MainstatType.FLAT_ATK, star=5, lvl=20)
        if goblet == "PYRO":
            mainstat_attr.dmg_bonus["PYRO"] = .466 # HERE IS THE HACK
        for substat_dist in itertools.product(*roll_counts):
            if count % 10000 == 0:
                pass
                #print(count)
            count += 1
            if sum(substat_dist) == BUDGET:
                substat_dist = {substats[i]: substat_dist[i] for i in range(len(substats))}
                substat_attr_d = {sub: avg_subs[sub]*rc for sub, rc in substat_dist.items()}
                substat_attr = AttrObj(**substat_attr_d)
                dps, tot_attr = dps_func(mainstat_attr, substat_attr)

                if dps > highest_dps:
                    highest_substat_attr = substat_attr
                    highest_substat_dist = substat_dist
                    highest_mainstat_attr = mainstat_attr
                    highest_tot_attr = tot_attr
                    highest_dps = dps
    print(highest_dps, highest_substat_dist)
    print(highest_substat_attr + highest_mainstat_attr)
    print(highest_tot_attr)


# 4 line start, only 4 substats, doesn't account for single "dead" roll on sands and circlet
def perf_art_optim(dps_func, sandss, goblets, circlets, substats):
    GOOD_ROLLS = 4 # 4, 8, 16, 20
    BUDGET = 4*5 + GOOD_ROLLS*5 - 2 # initial + good rolls, you lose 2 to dead rolls, can't have crit in circlet and sub, can't have atk% in circlet and sub, TODO hack

    highest_dps = 0
    highest_substat_attr = None
    highest_substat_dist = None
    highest_mainstat_attr = None
    highest_tot_attr = None

    # Iterate through main stats
    count = 0
    for sands, goblet, circlet in itertools.product(sandss, goblets, circlets):
        avg_subs = {sub: avg_artifact_substat(sub) for sub in substats} # Gets the average substat roll value for each substat
        num_valid_arts = {sub: count_valid_artifacts(sub, sands, goblet, circlet) for sub in substats} # Checks for duplicate substats from main stats
        # starts with 1 for each artifact if possible
        roll_counts = [range(num_valid_arts[sub], num_valid_arts[sub] + GOOD_ROLLS*num_valid_arts[sub] + 1) for sub in substats] # Generates number of rolls for each substat
        # mainstat_dist = {ms: artifact_mainstat(ms, star=5, lvl=20) for ms in [sandss, goblet, circlet]} # TODO does not account for multiple of the same main stat
        # hack to get around pyro type for now
        mainstat_attr = {ms: artifact_mainstat(ms, star=5, lvl=20) for ms in [sands, circlet]} # TODO does not account for multiple of the same main stat
        mainstat_attr = AttrObj(**mainstat_attr)
        mainstat_attr.flat_hp += artifact_mainstat(MainstatType.FLAT_HP, star=5, lvl=20)
        mainstat_attr.flat_atk += artifact_mainstat(MainstatType.FLAT_ATK, star=5, lvl=20)
        mainstat_attr.dmg_bonus["PYRO"] = .466 # HERE IS A HACK (to account for pyro goblet)

        for substat_dist in itertools.product(*roll_counts):
            if count % 10000 == 0:
                pass
                #print(count)
            count += 1
            if sum(substat_dist) == BUDGET:
                substat_dist = {substats[i]: substat_dist[i] for i in range(len(substats))}
                substat_attr_d = {sub: avg_subs[sub]*rc for sub, rc in substat_dist.items()} # Looks like {"ATK_PCT": 5, "EM": 2, "CRIT_RATE": 10, "CRIT_DMG": 10}
                substat_attr = AttrObj(**substat_attr_d)
                dps, dmg, dur, tot_attr = dps_func(mainstat_attr, substat_attr)
                if dps > highest_dps:
                    highest_substat_attr = substat_attr
                    highest_substat_dist = substat_dist
                    highest_mainstat_attr = mainstat_attr
                    highest_tot_attr = tot_attr
                    highest_dps = dps
    print("DPS:", highest_dps)
    print("Substats:", highest_substat_dist)
    print("Artifact Stats:", highest_substat_attr + highest_mainstat_attr)
    print("Total Stats:", highest_tot_attr)

def main():
    # def n3cq_dps(weapon_attr, artifact_main_stats, artifact_substats, artifact_set_effects, vape=True, vape_bonus=0, low_hp=0, is_homa=False, use_bennet=0):
    perf_art_optim(lambda mainstat_attr, substat_attr: n3cq_dps(dm_attr, mainstat_attr, substat_attr, artifact_set_effects, supress=True), sandss=[MainstatType.HP_PCT], goblets=["PYRO"], circlets=[MainstatType.CRIT_DMG, MainstatType.CRIT_RATE], 
        substats=[SubstatType.CRIT_RATE, SubstatType.CRIT_DMG, SubstatType.HP_PCT, SubstatType.EM])

if __name__ == "__main__":
    main()
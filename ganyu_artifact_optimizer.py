from utils import calc_dmg, calc_dmg_obj, avg_crit_dmg, calc_avg_crit_dmg_obj, AttrObj, DmgTag
from artifacts import avg_artifact_substat, SubstatType
from copy import deepcopy

# list of damage applications, tags, 
# combo as a list of damage applications with tags

celestial_shower_hits_per_enemy = 12
a1_passive_uptime = .75
a1_passive_bloom_uptime = 1
a4_passive_uptime = .675
prototype_crescent_uptime = .9
viridescent_hunt_proc_rate = .938
headshot_rate = .3 #.3
cryo_uptime = .90
freeze_uptime = 0
field_time = 10

sample_artifact_substats = AttrObj(flat_atk=50, atk_pct=.249, crit_rate=.198, crit_dmg=.396, em=99, er=.275, flat_hp=762, hp_pct=.149, flat_def=59, def_pct=.186) # should this include all?
def calc_ganyu_dps(artifact_substats):
    # SETUP
    artifact_main_stats = AttrObj(flat_atk=311, atk_pct=.466, crit_rate=.311, dmg_bonus={DmgTag.CRYO: .466})
    #artifact_main_stats = AttrObj(flat_atk=311, atk_pct=.466, crit_dmg=.622, dmg_bonus={DmgTag.CRYO: .466})
    artifact_set_effects = AttrObj(crit_rate=(cryo_uptime*.20 + freeze_uptime * .20), dmg_bonus={DmgTag.CRYO: .15}) # Blizzard Strayer

    char_attr = AttrObj(base_atk=295, crit_rate=.05, crit_dmg=(.50 + .288)) #ascension + base values, c0
    weapon_attr = AttrObj(base_atk=510, atk_pct=.413 + .36*prototype_crescent_uptime) # prototype_crescent, lvl 90

    burst_bonus = AttrObj(dmg_bonus={DmgTag.CRYO: a4_passive_uptime*.20})

    tot_attr = char_attr + artifact_main_stats + artifact_substats + artifact_set_effects + weapon_attr + burst_bonus 

    # CALCULATING DAMAGE
    a1 = AttrObj(crit_rate=a1_passive_uptime*.20)
    ca_attr = tot_attr + a1
    cr = headshot_rate + (1-headshot_rate)*ca_attr.crit_rate
    ca_dmg = avg_crit_dmg(calc_dmg_obj(ca_attr, 1.792, [DmgTag.CRYO, DmgTag.CHARGED]), cr, ca_attr.crit_dmg, supress=True)*4

    a1 = AttrObj(crit_rate=a1_passive_bloom_uptime*.20)
    bloom_attr = tot_attr + a1
    bloom_dmg = calc_avg_crit_dmg_obj(bloom_attr, 3.0464, [DmgTag.CRYO, DmgTag.CHARGED], supress=True)*4

    skill_dmg = calc_avg_crit_dmg_obj(tot_attr, 3.326, [DmgTag.CRYO, DmgTag.SKILL], supress=True)*1
    burst_dmg = calc_avg_crit_dmg_obj(tot_attr, 11.806, [DmgTag.CRYO, DmgTag.SKILL], supress=True)*1

    tot_dmg = ca_dmg + bloom_dmg + skill_dmg + burst_dmg
    dps = tot_dmg/field_time
    return dps, (char_attr + artifact_main_stats + artifact_substats + artifact_set_effects + weapon_attr)

# EM NOT INCLUDED BECAUSE MELT NOT IMPLEMENTED
ALLOWED_SUBSTATS = [SubstatType.FLAT_ATK, SubstatType.ATK_PCT, SubstatType.CRIT_RATE, SubstatType.CRIT_DMG]

avg_flat_atk = avg_artifact_substat(SubstatType.FLAT_ATK)
avg_atk_pct = avg_artifact_substat(SubstatType.ATK_PCT)
avg_cr = avg_artifact_substat(SubstatType.CRIT_RATE)
avg_cd = avg_artifact_substat(SubstatType.CRIT_DMG)

highest_dps = 0
highest_substat_attr = None
highest_tot_attr = None

BUDGET = 9*4
count = 0
# starts with 4 because of initial rolls, 6 because (0, 4, 8, 12, 16, 20) to get that rolls x number of artifacts (4 or 5)
for s1 in range(4, 6*4 + 1): # flat_atk, 3 b/c feather
    for s2 in range(4, 6*4 + 1): # atk_pct, 3 b/c sands
        for s3 in range(4, 6*4+1): # crit_rate, 3 b/c circlet
            for s4 in range(5, 6*5+1):
                if count % 10000 == 0:
                    print(count)
                count += 1
                if s1 + s2 + s3 + s4 > BUDGET:
                    continue
                artifact_substats = AttrObj(flat_atk=s1*avg_flat_atk, atk_pct=s2*avg_atk_pct, crit_rate=s3*avg_cr, crit_dmg=s4*avg_cd)
                dps, tot_attr = calc_ganyu_dps(artifact_substats)
                if dps > highest_dps:
                    highest_substat_attr = artifact_substats
                    highest_tot_attr = tot_attr
                    highest_dps = dps
print(highest_dps)
print(highest_substat_attr)
print(highest_tot_attr)
print()
print(calc_ganyu_dps(sample_artifact_substats)[0])

'''
valid_dists = []
# could implement more cleanly: https://stackoverflow.com/questions/1280667/in-python-is-there-an-easier-way-to-write-6-nested-for-loops
BUDGET = 9 # max # substats
for s1 in range(1, 6+1):
    for s2 in range(1, 6+1):
        for s3 in range(1, 6+1):
            for s4 in range(1, 6+1):
                dist = [s1, s2, s3, s4]
                if sum(dist) == BUDGET:
                    valid_dists.append(dist)

print('generated dists', len(valid_dists))

highest_dps = 0
highest_total = []
flower_c = 0
for flower in valid_dists:
    print(flower_c)
    for plume in valid_dists:
        for goblet in valid_dists:
            for sands in valid_dists:
                for circlet in valid_dists:
                    plume[0] = 0 # flat atk not allowed in plume, bc main stat
                    sands[1] = 0 # atk pct not allowed in sands, bc main stat
                    circlet[2] = 0 # crit rate not allowed in circle, bc main stat
                    total = [0, 0, 0, 0]
                    for i in range(4):
                        total[i] = flower[i] + plume[i] + sands[i] + goblet[i] + circlet[i]
                    artifact_substats = AttrObj(flat_atk=total[0]*avg_atk_pct, atk_pct=total[1]*avg_atk_pct, crit_rate=total[2]*avg_cr, crit_dmg=total[3]*avg_cd) 
                    dps = calc_ganyu_dps(artifact_substats)
                    if dps > highest_dps:
                        highest_dps = dps
                        highest_total = total
    flower_c += 1
'''
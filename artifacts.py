#https://genshin-impact.fandom.com/wiki/Artifacts
from utils import AttrObj

# Only 5 stars so far
from enum import Enum, auto
class SubstatType:
    FLAT_HP = "flat_hp"
    FLAT_ATK = "flat_atk"
    FLAT_DEF = "flat_def"
    HP_PCT = "hp_pct"
    ATK_PCT = "atk_pct"
    DEF_PCT = "def_pct"
    EM = "em" # Elemental Mastery
    ER = "er" # Energy Recharge
    CRIT_RATE = "crit_rate"
    CRIT_DMG = "crit_dmg"

class MainstatType:
    FLAT_HP = "flat_hp"
    FLAT_ATK = "flat_atk"
    HP_PCT = "hp_pct"
    ATK_PCT = "atk_pct"
    DEF_PCT = "def_pct"
    EM = "em" # Elemental Mastery
    ER = "er" # Energy Recharge
    CRIT_RATE = "crit_rate"
    CRIT_DMG = "crit_dmg"
    ELEM = "elem" # TODO should add elemntal types later
    PHYS = "phys"
    HEALING = "heal"

class ArtifactType(Enum):
    FLOWER = auto()
    PLUME = auto()
    SANDS = auto()
    GOBLET = auto()
    CIRCLET = auto()

# TODO add non 16/20 stats later
# https://genshin-impact.fandom.com/wiki/Artifacts/Main_Stat_Scaling
MAINSTATS = {
    (MainstatType.FLAT_HP, 5): [3967, 4780], 
    (MainstatType.FLAT_ATK, 5): [258, 311], 
    (MainstatType.HP_PCT, 5): [.387, .466], 
    (MainstatType.ATK_PCT, 5): [.387, .466], 
    (MainstatType.DEF_PCT, 5): [.484, .583], 
    (MainstatType.PHYS, 5): [.484, .583], 
    (MainstatType.ELEM, 5): [.387, .466], 
    (MainstatType.EM, 5): [155, 187], 
    (MainstatType.ER, 5): [.430, .518], 
    (MainstatType.CRIT_RATE, 5): [.260, .311], 
    (MainstatType.CRIT_DMG, 5): [.516, .622], 
    (MainstatType.HEALING, 5): [.298, .359], 
}

SUBSTATS = {
    (SubstatType.FLAT_HP, 5): [209,  239,  269,  299],
    (SubstatType.FLAT_ATK, 5): [14,  16,  18,  19],
    (SubstatType.FLAT_DEF, 5): [16,  19,  21,  23],
    (SubstatType.HP_PCT, 5): [.041,  .047,  .053,  .058],
    (SubstatType.ATK_PCT, 5): [.041,  .047,  .053,  .058],
    (SubstatType.DEF_PCT, 5): [.051,  .058,  .066,  .073],
    (SubstatType.EM, 5): [16,  19,  21,  23],
    (SubstatType.ER, 5): [.045,  .052,  .058,  .065],
    (SubstatType.CRIT_RATE, 5): [.027,  .031,  .035,  .039],
    (SubstatType.CRIT_DMG, 5): [.054,  .062,  .07,  .078]
}

def avg_artifact_substat(substat_type, star=5):
    return sum(SUBSTATS[(substat_type, star)])/4

def artifact_mainstat(mainstat_type, star=5, lvl=20):
    # TODO this will be changed soon
    if lvl == 16:
        return MAINSTATS[(mainstat_type, star)][0]
    elif lvl == 20:
        return MAINSTATS[(mainstat_type, star)][1]
    else:
        print('Artifact level Not supported yet')

def valid_mainstats(artifact_type):
    if artifact_type == ArtifactType.FLOWER:
        return [MainstatType.FLAT_HP]
    elif artifact_type == ArtifactType.PLUME:
        return [MainstatType.FLAT_ATK]
    elif artifact_type == ArtifactType.SANDS:
        return [MainstatType.HP_PCT, MainstatType.DEF_PCT, MainstatType.ATK_PCT, MainstatType.EM, MainstatType.ER]
    elif artifact_type == ArtifactType.GOBLET:
        return [MainstatType.HP_PCT, MainstatType.DEF_PCT, MainstatType.ATK_PCT, MainstatType.EM, MainstatType.ELEM, MainstatType.PHYS]
    elif artifact_type == ArtifactType.CIRCLET:
        return [MainstatType.HP_PCT, MainstatType.DEF_PCT, MainstatType.ATK_PCT, MainstatType.EM, MainstatType.CRIT_RATE, MainstatType.CRIT_DMG, MainstatType.HEALING]

#def default_substats():

# 3 flat atk, 5 atk%, 6 cr, 6 cd, 5 em, 5 er, 3 hp%, 3 flat def, 3 flat , 3 def%
zakharov_artifact_substats = AttrObj(flat_atk=50, atk_pct=.249, crit_rate=.198, crit_dmg=.396, em=99, er=.275, flat_hp=762, hp_pct=.149, flat_def=59, def_pct=.186)
zak_hutao_artifact_substats = AttrObj(flat_atk=50, atk_pct=.149, crit_rate=.198, crit_dmg=.396, em=99, er=.275, flat_hp=762, hp_pct=.249, flat_def=59, def_pct=.186)

#https://genshin-impact.fandom.com/wiki/Artifacts

# Only 5 stars so far
from enum import Enum, auto
class SubstatType(Enum):
    FLAT_HP = auto()
    FLAT_ATK = auto()
    FLAT_DEF = auto()
    HP_PCT = auto()
    ATK_PCT = auto()
    DEF_PCT = auto()
    EM = auto() # Elemental Mastery
    ER = auto() # Energy Recharge
    CRIT_RATE = auto()
    CRIT_DMG = auto()

class MainstatType(Enum):
    FLAT_HP = auto()
    FLAT_ATK = auto()
    HP_PCT = auto()
    ATK_PCT = auto()
    DEF_PCT = auto()
    EM = auto() # Elemental Mastery
    ER = auto() # Energy Recharge
    CRIT_RATE = auto()
    CRIT_DMG = auto()
    ELEM = auto() # TODO should add elemntal types later
    PHYS = auto()
    HEALING = auto()

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

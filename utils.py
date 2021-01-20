# Robin's Damage Calculator https://docs.google.com/spreadsheets/d/1pYDZpKgnF-8aRdfKfD_pYRnKKAabgboO1WuxjPmcZO8/edit#gid=687545622
# Genshin Wiki Page on Damage: https://genshin-impact.fandom.com/wiki/Damage

# (Base ATK * (1 + ATK%) + FLAT ATK)*(1 + Corresponding Dmg Bonus%)*(Ability Multiplier)*[(100+Character Level)/((100+Character Level) + (100+Enemy Level)*(1-Defence drop%))]*(1 - Corresponding Enemy RES%)


def calc_tot_atk(base_atk, atk_pct, flat_atk):
    return base_atk * (1 + atk_pct) + flat_atk

# base_atk = weapon base atk + character base atk
# flat_atk: from feather, substats 
# ability_mult: talent dmg %
# dmg_bonus_pct ex. cryo dmg % + charged atk %
# resist_pct ex. 35 + 45 % cryo resist for cryowhopper flower, 10% resist for elem/phys for hillichurls
# TODO how to add multiplicative damage like XQ
def calc_dmg(base_atk, atk_pct, flat_atk, ability_mult, dmg_bonus_pct, def_drop_pct=0, char_lvl=80, enemy_lvl=80, enemy_resist_pct=.1):
    tot_atk = calc_tot_atk(base_atk, atk_pct, flat_atk)

    def_mult = (100 + char_lvl)/((100+char_lvl) + (100 + enemy_lvl)*(1-def_drop_pct))
    
    if enemy_resist_pct < 0: # (-infty, 0)
        resist_mult = 1 - enemy_resist_pct/2
    elif enemy_resist_pct < .75: # [0, .75)
        resist_mult = 1 - enemy_resist_pct
    else: # [.75, infty)
        resist_mult = 1/(4*enemy_resist_pct + 1) 
    
    return ability_mult * tot_atk * (1 + dmg_bonus_pct) * def_mult * resist_mult

# Non-Critical Dmg*(1 + (Crit Rate%*Crit DMG%))
def avg_crit_dmg(non_crit_dmg, crit_rate, crit_dmg, supress=False):
    if crit_rate > 1:
        if not supress:
            print(f"Crit rate was: {crit_rate}. Truncated to 1 (100%)")
        crit_rate = 1
    return non_crit_dmg * (1 + crit_rate*crit_dmg)

def calc_avg_crit_dmg_obj(attr, ability_mult, dmg_tags, enemy_resist_pct=.1, supress=False):
    dmg = calc_dmg_obj(attr, ability_mult, dmg_tags, enemy_resist_pct)
    return avg_crit_dmg(dmg, attr.crit_rate, attr.crit_dmg, supress=supress)

# TODO enemy_resist_pct should be a dictionary of damage type to resistance
def calc_dmg_obj(attr, ability_mult, dmg_tags, enemy_resist_pct=.1):
    dmg_bonus = 0
    for tag, bonus in attr.dmg_bonus.items():
        if tag in dmg_tags:
            dmg_bonus += bonus
    return calc_dmg(attr.base_atk, attr.atk_pct, attr.flat_atk, ability_mult, dmg_bonus, enemy_resist_pct=enemy_resist_pct)

'''
# https://genshin-impact.fandom.com/wiki/Melt
MAGIC_MELT_NUMBER1 = .189266831
MAGIC_MELT_NUMBER2 = -.000505
def melt_base_dmg():
    return 1 + (MAGIC_MELT_NUMBER1 * em * exp(MAGIC_MELT_NUMBER2))/100

# sometimes called reverse melt (1.5x melt)
def cryo_melt_dmg():
    return 1.5 * melt_base_dmg

# 2x melt
def pyro_melt():
    return 2 * melt_base_dmg
'''

def add_dicts(d1, d2):
    new_dict = d1.copy()
    for tag, bonus in d2.items():
        if tag in new_dict:
            new_dict[tag] += bonus
        else:
            new_dict[tag] = bonus
    return new_dict

class AttrObj:
    def __init__(self, base_atk=0, atk_pct=0, flat_atk=0, crit_rate=0, crit_dmg=0, er=0, em=0, hp_pct=0, flat_hp=0, def_pct=0, flat_def=0, dmg_bonus=dict()):
        self.base_atk = base_atk
        self.atk_pct = atk_pct
        self.flat_atk = flat_atk
        self.crit_rate = crit_rate
        self.crit_dmg = crit_dmg
        self.er = er
        self.em = em
        self.hp_pct = hp_pct
        self.flat_hp = flat_hp
        self.def_pct = def_pct
        self.flat_def = flat_def
        self.dmg_bonus = dmg_bonus
    
    def __add__(self, o):
        base_atk = self.base_atk + o.base_atk
        atk_pct = self.atk_pct + o.atk_pct
        flat_atk = self.flat_atk + o.flat_atk
        crit_rate = self.crit_rate + o.crit_rate
        crit_dmg = self.crit_dmg + o.crit_dmg
        er = self.er + o.er
        em = self.em + o.em
        hp_pct = self.hp_pct + o.hp_pct
        flat_hp = self.flat_hp + o.flat_hp
        def_pct = self.def_pct + o.def_pct
        flat_def = self.flat_def + o.flat_def
        dmg_bonus = add_dicts(self.dmg_bonus, o.dmg_bonus)
        return AttrObj(base_atk=base_atk, atk_pct=atk_pct, flat_atk=flat_atk, crit_rate=crit_rate, crit_dmg=crit_dmg, er=er, em=em, hp_pct=hp_pct, flat_hp=flat_hp, def_pct=def_pct, flat_def=flat_def, dmg_bonus=dmg_bonus) 
    
    def __str__(self):
        ret = ''
        ret += f'Base ATK: {self.base_atk}\n'
        ret += f'ATK%: {self.atk_pct}\n'
        ret += f'Flat ATK: {self.flat_atk}\n'
        ret += f'CR: {self.crit_rate}\n'
        ret += f'CD: {self.crit_dmg}\n'
        ret += f'ER: {self.er}\n'
        ret += f'EM: {self.em}\n'
        ret += f'HP%: {self.hp_pct}\n'
        ret += f'Flat HP: {self.flat_hp}\n'
        ret += f'DEF%: {self.def_pct}\n'
        ret += f'Flat DEF: {self.flat_def}\n'
        ret += '\n'
        for tag, bonus in self.dmg_bonus.items():
            ret += f'{tag}: {bonus}\n' 
        return ret

class DmgObj:
    def __init__(self, attrs, tags):
        self.attrs = attrs
        self.tags = tags

class DmgTag:
    PHYS = "PHYS"
    CRYO = "CRYO"
    PYRO = "PYRO"
    HYDRO = "HYDRO"
    ELECTRO = "ELECTRO"
    ANEMO = "ANEMO"
    GEO = "GEO"
    SKILL = "SKILL" # elemental skill
    BURST = "BURST" # elemental burst
    NORMAL = "NORMAL" # normal attacks
    CHARGED = "CHARGED" # charged attacks
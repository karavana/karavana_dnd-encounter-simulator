from typing import Dict, List, Union

import dice
from loguru import logger

from DndEncounterSimulator.Objects.utils.conversion import convert_stat_to_mod
from DndEncounterSimulator.Objects.Weapon import DamageType, Weapon


class Creature:
    """
    A class to define all kind of creatures that might be encountered.
    """

    def __init__(
        self,
        name: str,
        hit_points: int,
        armor_class: int,
        stats: Dict,
        weapons: List[Weapon],
        resistances: List[DamageType],
        immunities: List[DamageType],
        vulnerabilities: List[DamageType],
        camp: str,
    ):
        self.name = name
        self.hit_points = int(hit_points)
        self.armor_class = int(armor_class)
        if stats:
            self.stats = stats
        self.weapons = [weapon for weapon in weapons]
        self.modifiers = {
            key: convert_stat_to_mod(value) for (key, value) in self.stats.items()
        }
        self.resistances = [resistance for resistance in resistances]
        self.immunities = [immunity for immunity in immunities]
        self.vulnerabilities = [vulnerability for vulnerability in vulnerabilities]
        self.dead = False
        self.initiative = self.roll_initiative()
        self.camp = str(camp)

    def roll_initiative(self) -> int:
        """
        Method to roll the initiative of a creature.

        :return: (int) The initiative rolled.
        """
        dexterity_mod = self.modifiers.get('dexterity', 0)
        return dice.roll("1d20")[0] + dexterity_mod

    def damage(self, damages: int, type_of_damage: DamageType):
        """
        Method to remove HP when a Creature takes a hit.

        :param damages: (int) The quantity of damage done
        :param type_of_damage: (DamageType) The type of damage dealt by the attack
        """
        damage_reduction_factor = 1

        if type_of_damage in self.immunities:
            damage_reduction_factor = 0
        elif type_of_damage in self.resistances:
            damage_reduction_factor = 0.5
        elif type_of_damage in self.vulnerabilities:
            damage_reduction_factor = 2

        actual_damage = int(damages * damage_reduction_factor)

        self.hit_points -= actual_damage
        if self.hit_points <= 0:
            self.dead = True

    def change_weapon(self, index: int):
        """
        Method to change to the weapon referenced by the index: this weapon will be placed at index 0 for use in combat

        :param index: (int) the index referencing a weapon in weapons list
        """
        if 0 <= index < len(self.weapons):
            self.weapons.insert(0, self.weapons.pop(index))


class Monster(Creature):
    def __init__(
        self,
        name: str,
        hit_points: int,
        armor_class: int,
        stats: Dict,
        weapons: List[Weapon],
        resistances: List[DamageType],
        immunities: List[DamageType],
        vulnerabilities: List[DamageType],
        proficiency: int,
        camp: str,
    ):
        super(Monster, self).__init__(
            name=name,
            hit_points=hit_points,
            armor_class=armor_class,
            stats=stats,
            weapons=weapons,
            resistances=resistances,
            immunities=immunities,
            vulnerabilities=vulnerabilities,
            camp=camp,
        )
        self.proficiency = int(proficiency)

    def attack(self, opponent: Creature, weapon: Weapon):
        """
        Method simulating the attack of a monster on a Creature

        :param opponent: (Creature) The target of the attack.
        :param weapon: (Weapon) The weapon used to attack the enemy.
        """
        weapon_to_use = weapon if weapon else self.weapons[0]

        attack_roll = dice.roll("1d20")[0] + self.proficiency
        if attack_roll >= opponent.armor_class:
            critical_hit = (attack_roll - self.proficiency) == 20
            damage_dealt = weapon_to_use.deal_damage(self.modifiers.get(weapon_to_use.stat_to_hit, 0), critical_hit)
            opponent.damage(damage_dealt, weapon_to_use.type_of_damage)

    def find_opponent(
        self, fighters: List[Creature], wounded_fighters=List[bool]
    ) -> Union[None, int]:
        """
        Method to find which opponent to fight in a list of creatures.

        This method finds an opponent of another camp, so it doesn't attack an ally,
        and it chooses a wounded opponent if possible.

        :param fighters: (List[Creatures]) the list of creatures in the fight.
        :param wounded_fighters: (List[bool]) a list of booleans indicating if creatures are damaged or not.
        :return: (Union[None, int]) the index of the first enemy found, None otherwise.
        """
        enemy_camp = "blue" if self.camp == "red" else "red"

        for index, (fighter, is_wounded) in enumerate(zip(fighters, wounded_fighters)):
            if fighter.camp == enemy_camp and (is_wounded or not any(wounded_fighters)):
                return index

        return None

    def find_best_weapon(
        self,
        known_resistances: List[DamageType] = [],
        known_immunities: List[DamageType] = [],
        known_vulnerabilities: List[DamageType] = [],
    ) -> int:
        """
        Method to find the best weapon (ie deals statistically the more damage)

        #TODO: add options and limitations for two-handed, ranged, damage immunity...

        :return: (int) the index of the best weapon to use
        """
        max_damage = 0
        best_weapon_index = -1

        for index, weapon in enumerate(self.weapons):
            average_damage = weapon.average_damage()

            # Adjusting damage based on known factors - mimicking damage method logic
            if weapon.type_of_damage in known_immunities:
                continue
            elif weapon.type_of_damage in known_resistances:
                average_damage *= 0.5
            elif weapon.type_of_damage in known_vulnerabilities:
                average_damage *= 2
                
            if average_damage > max_damage:
                max_damage = average_damage
                best_weapon_index = index

        if best_weapon_index == -1:
            raise IndexError("No suitable weapon found.")

        return best_weapon_index

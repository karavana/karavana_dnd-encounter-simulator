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
        pass

    def damage(self, damages: int, type_of_damage: DamageType):
        """
        Method to remove HP when a Creature takes a hit.

        :param damages: (int) The quantity of damage done
        :param type_of_damage: (DamageType) The type of damage dealt by the attack
        """
        pass

    def change_weapon(self, index: int):
        """
        Method to change to the weapon referenced by the index: this weapon will be placed at index 0 for use in combat

        :param index: (int) the index referencing a weapon in weapons list
        """
        pass


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
        pass

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
        pass

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
        pass

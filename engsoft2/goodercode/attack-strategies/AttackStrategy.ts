import { Character } from "../character/Character";

export interface AttackStrategy {
  attack(attacker: Character, target: Character): void;
}

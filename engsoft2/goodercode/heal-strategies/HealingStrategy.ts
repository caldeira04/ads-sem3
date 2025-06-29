import { Character } from "../character/Character";

export interface HealingStrategy {
  heal(character: Character): void;
}

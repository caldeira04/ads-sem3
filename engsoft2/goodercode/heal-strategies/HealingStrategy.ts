import { Healable } from "./Healable";

export interface HealingStrategy {
  heal(character: Healable): void;
}

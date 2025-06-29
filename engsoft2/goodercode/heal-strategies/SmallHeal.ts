import { Character } from "../character/Character";
import { HealingStrategy } from "./HealingStrategy";

class SmallHeal implements HealingStrategy {
  heal(character: Character) {
    character.receiveHeal(5);
    console.log("Cura pequena!");
  }
}

export default SmallHeal;

import { HealingStrategy } from "./HealingStrategy";
import { Character } from "../character/Character";

class BigHeal implements HealingStrategy {
  heal(character: Character) {
    character.receiveHeal(20);
    console.log("Cura grande!");
  }
}

export default BigHeal;

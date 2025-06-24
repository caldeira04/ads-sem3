import { HealingStrategy } from "./HealingStrategy";
import { Healable } from "./Healable";

class BigHeal implements HealingStrategy {
  heal(character: Healable) {
    character.receiveHeal(20);
    console.log("Cura grande!");
  }
}

export default BigHeal;

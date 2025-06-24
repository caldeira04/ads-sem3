import { Healable } from "./Healable";
import { HealingStrategy } from "./HealingStrategy";

class SmallHeal implements HealingStrategy {
  heal(character: Healable) {
    character.receiveHeal(5);
    console.log("Cura pequena!");
  }
}

export default SmallHeal;

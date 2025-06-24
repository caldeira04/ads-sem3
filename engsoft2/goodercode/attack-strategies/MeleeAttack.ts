import { Character } from "../character/Character";
import { AttackStrategy } from "./AttackStrategy";

class MeleeAttack implements AttackStrategy {
  attack(attacker: Character, target: Character) {
    console.log(`Ataque corpo a corpo de ${attacker.getName()} em ${target.getName()}! HP de ${target.getName()}: ${target.getHp()}`);
    target.receiveAttack(10);
  }
}

export default MeleeAttack;

import { Character } from "../character/Character";
import { AttackStrategy } from "./AttackStrategy";

class RangedAttack implements AttackStrategy {
  attack(attacker: Character, target: Character) {
    console.log(`Ataque a longa distância de ${attacker.getName()} em ${target.getName()}! HP de ${target.getName()}: ${target.getHp()}`);
    target.receiveAttack(20);
  }
}

export default RangedAttack;

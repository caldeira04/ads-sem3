import { Character } from "../character/Character";
import { AttackStrategy } from "./AttackStrategy";

class BossAttack implements AttackStrategy {
  attack(attacker: Character, target: Character) {
    console.log(`Ataque de boss de ${attacker.getName()} em ${target.getName()}! HP de ${target.getName()}: ${target.getHp()}`);
    target.receiveAttack(100);
  }
}

export default BossAttack;

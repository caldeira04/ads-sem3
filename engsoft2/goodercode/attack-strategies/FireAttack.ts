import { Character } from "../character/Character";
import { AttackStrategy } from "./AttackStrategy";

class FireAttack implements AttackStrategy {
  attack(attacker: Character, target: Character) {
    console.log(`Fogo em área de ${attacker.getName()} em ${target.getName()}! HP de ${target.getName()}: ${target.getHp()}`);
    target.receiveAttack(100);
  }
}

export default FireAttack;

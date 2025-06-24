import { AttackStrategy } from "../attack-strategies/AttackStrategy";
import { HealingStrategy } from "../heal-strategies/HealingStrategy";

export class Character {
  // construimos a classe com os atributos necessários
  private hp: number;
  private name: string;
  private attackStrategy: AttackStrategy;
  // o healingStrategy é definido diretamente no index.ts, pois pode ser que alguns mobs não possuam o atributo
  private healingStrategy?: HealingStrategy;
  // adicionamos também a propriedade isAlive, para que possamos verificar se o personagem está vivo ou não antes de realizar alguma acao que o envolva
  private isAlive: boolean = true;

  constructor(attackStrategy: AttackStrategy, hp: number, name: string) {
    this.attackStrategy = attackStrategy;
    this.hp = hp;
    this.name = name;
  }

  getName(): string {
    return this.name;
  }

  getHp(): number {
    return this.hp;
  }

  setAttackStrategy(attackStrategy: AttackStrategy): void {
    this.attackStrategy = attackStrategy;
  }

  performAttack(target: Character): void {
    if (!this.isAlive) {
      console.log(`${this.name} não pode atacar ${target.name}! Está morto!`);
      return;
    }

    if (!target.isAlive) {
      console.log(`${this.name} não pode atacar ${target.name}! ${target.name} está morto!`);
      return;
    }

    this.attackStrategy.attack(this, target);
  }

  receiveAttack(amount: number): void {
    if (!this.isAlive) {
      console.log(`${this.name} está morto. Não pode mais receber ataques.`);
      return;
    }

    this.hp -= amount;
    console.log(`${this.name} recebeu ${amount} de dano! Vida atual: ${this.hp}`);
    if (this.hp <= 0) {
      console.log(`${this.name} morreu!`);
      this.isAlive = false;
    }
  }

  setHealingStrategy(healingStrategy: HealingStrategy): void {
    this.healingStrategy = healingStrategy;
  }

  performHeal(): void {
    if (!this.isAlive) {
      console.log(`${this.name} não pode realizar cura! Está morto!`);
      return;
    }

    if (this.healingStrategy) {
      this.healingStrategy.heal(this);
    } else {
      console.log("Nenhuma estratégia de cura foi definida!");
    }
  }

  receiveHeal(amount: number): void {
    if (!this.isAlive) {
      console.log(`${this.name} está morto. Não pode receber cura.`);
      return;
    }

    this.hp += amount;
    console.log(`${this.name} recebeu ${amount} de vida! Vida atual: ${this.hp}`);
  }
}

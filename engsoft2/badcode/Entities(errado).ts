class Enemy {
  hp: number;
  attack: number;
  defense: number;

  constructor(hp: number, attack: number, defense: number) {
    this.hp = hp;
    this.attack = attack;
    this.defense = defense;
  }

  takeDamage(damage: number) {
    this.hp -= damage;
    console.log(`Sofreu ${damage} de dano. Vida atual: ${this.hp}`);
  }

  doAttack() {
    console.log(`Atacando com ${this.attack} de dano corpo-a-corpo`);
  }

  doFireAttack() {
    console.log(`Atacando com ${this.attack} de dano de fogo`);
  }

  heal(heal: number) {
    this.hp += heal;
    console.log(`Recuperou ${heal} de vida. Vida atual: ${this.hp}`);
  }
}

// e então, como raciocinamos que tanto player, mob, npc, boss, possuem tais atributos
// utilizamos herança para criar uma classe base para esses personagens.

class Player extends Enemy { }
class Boss extends Enemy { }
class Mob extends Enemy { }

const badBoss = new Boss(100, 10, 5);
badBoss.doFireAttack();

// ok. temos nossas classes inicializadas. mas... player e boss não são necessariamente enemies.
// além do mais, pode ser que cada char tenha atributos diferentes não presentes em inimigos.
// logo, este código é ERRADO.
//
// como seria o certo?

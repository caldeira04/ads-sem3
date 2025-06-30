# Código Ruim

O código ruim é o código que não segue o padrão de projeto.

Este código define todos os personagens em um único arquivo, violando o princípio da responsabilidade única, além de ser de difícil manutencao e escalabilidade, caso necessário.

```typescript
class Enemy {
  hp: number;
  attack: number;

  constructor(hp: number, attack: number, defense: number) {
    this.hp = hp;
    this.attack = attack;
  }

  takeDamage(damage: number) {
    this.hp -= damage;
    console.log(`Sofreu ${damage} de dano. Vida atual: ${this.hp}`);
  }

  doAttack() {
    console.log(`Atacando com ${this.attack} de dano`);
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
badBoss.doAttack();

// ok. temos nossas classes inicializadas. mas... player e boss não são necessariamente enemies.
// além do mais, pode ser que cada char tenha atributos diferentes não presentes em inimigos.
// logo, este código é ERRADO.
//
// como seria o certo?
```

## [Desta forma](../goodcode/README.md)

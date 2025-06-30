# Código ~quase~ Bom

O código ~quase~ bom é o código que segue o padrão de projeto, porém não está adequado conforme o princípio de responsabilidade única e modularizacao adequados para POO.

```typescript
// Entities.ts
// primeiro, criamos uma interface para definir o que é um attackstrategy

interface AttackStrategy {
  attack(): void;
}

// então, criamos diferentes classes que implementam a interface AttackStrategy
// por exemplo, attack melee, ranged, boss, etc.

class MeleeAttack implements AttackStrategy {
  attack(): void {
    console.log("Ataque corpo a corpo!");
  }
}

class RangedAttack implements AttackStrategy {
  attack(): void {
    console.log("Ataque de longo alcance!");
  }
}

class BossAttack implements AttackStrategy {
  attack(): void {
    console.log("Ataque de boss em área!");
  }
}

// agora, criamos um char finalmente

class Character {
  private attackStrategy: AttackStrategy;

  constructor(attackStrategy: AttackStrategy) {
    this.attackStrategy = attackStrategy;
  }

  // realiza o ataque (durr)
  performAttack(): void {
    this.attackStrategy.attack();
  }

  // define o ataque (vai que troque de espada pra arco, por exemplo)
  setAttackStrategy(attackStrategy: AttackStrategy): void {
    this.attackStrategy = attackStrategy;
  }
}

const player = new Character(new MeleeAttack());
player.performAttack();

const boss = new Character(new BossAttack());
boss.performAttack();

// agora digamos que o player pegou um arco;
player.setAttackStrategy(new RangedAttack());
player.performAttack();
```

## Vantagens:

Implementação muito mais simples, e para adicionar um novo tipo de ataque, basta criar uma nova classe implementando AttackStrategy.

```typescript
// definimos o ataque de fogo
class FireAttack implements AttackStrategy {
  attack(): void {
    console.log("Fogo em área!");
  }
}

// criamos um novo char que usa esse ataque
const dragon = new Character(new FireAttack());
dragon.performAttack();
// mas se isso aqui ainda não tá bom, como seria o perfeito?
```

## [Assim!](../goodercode/README.md)

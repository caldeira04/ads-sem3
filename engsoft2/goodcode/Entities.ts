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

class IceAttack implements AttackStrategy {
  attack(): void {
    console.log("Gelo em área!");
  }
}

class FireAttack implements AttackStrategy {
  attack(): void {
    console.log("Fogo em área!");
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

// ... ok, mas de que serviu? simples! agora, podemos criar um novo tipo de boss facilmente, por exemplo.
// basta adicionar um tipo de ataque novo, e criar um novo boss com ele. (ver linha 28)

const dragon = new Character(new FireAttack());
dragon.performAttack();

const iceMage = new Character(new IceAttack());
iceMage.performAttack();

// certo. mas isso aí tá muito simples. os personagens só dão dano?
// ai q vc se engana! confira ../goodercode

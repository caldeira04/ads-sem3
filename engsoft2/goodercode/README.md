# Aqui que são elas de fato!

Nesta *src* teremos todas estratégias devidamente modularizadas, cada uma em seu arquivo, em sua própria classe.
Pode parecer mais "bloated", mas é muito mais simples de manter e entender.

Começamos criando as **Strategies**. Para o exemplo, usaremos estratégias de ataque e cura.

## Attack Strategies

Agora, vamos criar a estratégia de ataque.
```typescript
// attack-strategies/AttackStrategy.ts
import { Character } from "../character/Character";

export interface AttackStrategy {
  attack(attacker: Character, target: Character): void;
}
```

Vamos criar a estratégia de ataque corpo a corpo.

```typescript
// attack-strategies/MeleeAttack.ts
import { Character } from "../character/Character";
import { AttackStrategy } from "./AttackStrategy";

class MeleeAttack implements AttackStrategy {
  attack(attacker: Character, target: Character) {
    console.log(`Ataque corpo a corpo de ${attacker.getName()} em ${target.getName()}! HP de ${target.getName()}: ${target.getHp()}`);
    target.receiveAttack(10);
  }
}

export default MeleeAttack;
```

... Ataque à distância.

```typescript
// attack-strategies/RangedAttack.ts
import { Character } from "../character/Character";
import { AttackStrategy } from "./AttackStrategy";

class RangedAttack implements AttackStrategy {
  attack(attacker: Character, target: Character) {
    console.log(`Ataque a longa distância de ${attacker.getName()} em ${target.getName()}! HP de ${target.getName()}: ${target.getHp()}`);
    target.receiveAttack(20);
  }
}

export default RangedAttack;
```

... E ataque de boss, especial, em área.

```typescript
// attack-strategies/RangedAttack.ts
import { Character } from "../character/Character";
import { AttackStrategy } from "./AttackStrategy";

class BossAttack implements AttackStrategy {
  attack(attacker: Character, target: Character) {
    console.log(`Ataque de boss de ${attacker.getName()} em ${target.getName()}! HP de ${target.getName()}: ${target.getHp()}`);
    target.receiveAttack(100);
  }
}

export default BossAttack;
```

## Heal Strategies

Com as estratégias de ataque, podemos pensar em como criar estratégias de cura.

Vamos criar a interface de objeto `Healable`, para não chamar a classe `Character` de forma circular.
```typescript
// heal-strategies/Healable.ts
export interface Healable {
  receiveHeal(amount: number): void;
}
```

Agora, vamos criar a estratégia de cura.

```typescript
// heal-strategies/HealingStrategy.ts
import { Healable } from "./Healable";

export interface HealingStrategy {
  heal(target: Healable): void;
}
```

Vamos criar a estratégia de cura grande.

```typescript
// heal-strategies/BigHeal.ts
import { Healable } from "./Healable";
import { HealingStrategy } from "./HealingStrategy";

class BigHeal implements HealingStrategy {
  heal(target: Healable) {
    target.receiveHeal(20);
    console.log("Cura grande!");
  }
}

export default BigHeal;
```

... E de cura pequena.

```typescript
// heal-strategies/SmallHeal.ts
import { Healable } from "./Healable";
import { HealingStrategy } from "./HealingStrategy";

class SmallHeal implements HealingStrategy {
  heal(target: Healable) {
    target.receiveHeal(5);
    console.log("Cura pequena!");
  }
}

export default SmallHeal;
```

## Character

Perfeito! Agora já podemos ir para o que importa: o personagem.

```typescript
// character/Character.ts
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
```

Com todas estratégias criadas, e com a classe de personagem criada, podemos iniciar o jogo.
Para título de teste, o jogo será rodado em "hardcode".

```typescript
// index.ts
import MeleeAttack from "./attack-strategies/MeleeAttack";
import RangedAttack from "./attack-strategies/RangedAttack";
import BigHeal from "./heal-strategies/BigHeal";
import { Character } from "./character/Character";

const player = new Character(new MeleeAttack(), 100, "Player");
const enemy = new Character(new RangedAttack(), 10, "Enemy");

enemy.performAttack(player);

player.performAttack(enemy);
player.performAttack(enemy);
player.performAttack(enemy);

player.setHealingStrategy(new BigHeal());
player.performHeal();
```

```bash
$ npx ts-node index.ts
Ataque a longa distância de Enemy em Player! HP de Player: 100
Player recebeu 20 de dano! Vida atual: 80
Ataque corpo a corpo de Player em Enemy! HP de Enemy: 10
Enemy recebeu 10 de dano! Vida atual: 0
Enemy morreu!
Player não pode atacar Enemy! Enemy está morto!
Player não pode atacar Enemy! Enemy está morto!
Player recebeu 20 de vida! Vida atual: 100
Cura grande!
```

## Para adicionar novos tipos de ataque?

Simples! Crie um novo arquivo, com a sua estratégia de ataque, e implemente a interface `AttackStrategy`. Exporte a classe e adicione ao character que bem entender no index.ts.

```typescript
// attack-strategies/FireAttack.ts
import { Character } from "../character/Character";
import { AttackStrategy } from "./AttackStrategy";

class FireAttack implements AttackStrategy {
  attack(attacker: Character, target: Character) {
    console.log(`Fogo em área de ${attacker.getName()} em ${target.getName()}! HP de ${target.getName()}: ${target.getHp()}`);
    target.receiveAttack(100);
  }
}

export default FireAttack;
```

```typescript
// index.ts
// restante do código...
import FireAttack from "./attack-strategies/FireAttack";

const dragon = new Character(new FireAttack(), 500, "Dragon");
//...
dragon.performAttack(player);
```

O resultado?

```bash
$ npx ts-node index.ts
Ataque a longa distância de Enemy em Player! HP de Player: 100
Player recebeu 20 de dano! Vida atual: 80
Ataque corpo a corpo de Player em Enemy! HP de Enemy: 10
Enemy recebeu 10 de dano! Vida atual: 0
Enemy morreu!
Player não pode atacar Enemy! Enemy está morto!
Player não pode atacar Enemy! Enemy está morto!
Player recebeu 20 de vida! Vida atual: 100
Cura grande!
Fogo em área de Dragon em Player! HP de Player: 100
Player recebeu 100 de dano! Vida atual: 0
Player morreu!
```

## Essa é a demonstração do padrão de projeto! Bem aplicado à POO, pode ser uma arma fortíssima no desenvolvimento e engenharia de software.

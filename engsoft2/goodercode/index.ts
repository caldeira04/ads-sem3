import MeleeAttack from "./attack-strategies/MeleeAttack";
import RangedAttack from "./attack-strategies/RangedAttack";
import FireAttack from "./attack-strategies/FireAttack";
import BigHeal from "./heal-strategies/BigHeal";
import { Character } from "./character/Character";

const player = new Character(new MeleeAttack(), 100, "Player");
const enemy = new Character(new RangedAttack(), 10, "Enemy");
const dragon = new Character(new FireAttack(), 500, "Dragon");

enemy.performAttack(player);

player.performAttack(enemy);
player.performAttack(enemy);
player.performAttack(enemy);

player.setHealingStrategy(new BigHeal());
player.performHeal();

dragon.performAttack(player);

import MeleeAttack from "./attack-strategies/MeleeAttack";
import RangedAttack from "./attack-strategies/RangedAttack";
import FireAttack from "./attack-strategies/FireAttack";
import IceAttack from "./attack-strategies/IceAttack";
import BigHeal from "./heal-strategies/BigHeal";
import SmallHeal from "./heal-strategies/SmallHeal";
import { Character } from "./character/Character";

const player = new Character(new MeleeAttack(), 100, "Player");
const enemy = new Character(new RangedAttack(), 10, "Enemy");
const dragon = new Character(new FireAttack(), 500, "Dragon");
const iceMage = new Character(new IceAttack(), 500, "Ice Mage");

enemy.performAttack(player);

player.performAttack(enemy);
player.performAttack(enemy);
player.performAttack(enemy);

player.setHealingStrategy(new BigHeal());
player.performHeal();
player.setHealingStrategy(new SmallHeal());
player.performHeal();

dragon.performAttack(player);
iceMage.performAttack(player);

import { PrismaClient } from '../generated/prisma';
import { Router } from "express";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
const prisma = new PrismaClient();
const router = Router();

router.post("/", async (req, res) => {
  const { email, password } = req.body;

  const defaultMessage = "Invalid email or password";

  if (!email || !password) {
    res.status(400).json({ error: defaultMessage });
    return;
  }

  try {
    const user = await prisma.user.findFirst({ where: { email } });
    if (!user) {
      res.status(401).json({ error: defaultMessage });
      return
    }

    if (bcrypt.compareSync(password, user.password)) {
      const token = jwt.sign({ id: user.id, name: user.name }, process.env.JWT_SECRET as string, { expiresIn: '1h' });
      res.json({ token });
    } else {
      const desc = "Access denied to system";

      const log = await prisma.log.create({
        data: {
          action: desc,
          userId: user.id,
        },
      });
      res.status(401).json({ error: defaultMessage });
    }

  } catch (error) {
    console.error("Error logging in:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

export default router;

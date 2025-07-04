import { PrismaClient } from "../generated/prisma";
const prisma = new PrismaClient();
import { Router } from "express";
const router = Router();
import { checkToken, checkAdmin } from "../middleware/checkToken";

router.get("/", checkToken, async (req, res) => {
  try {
    const logs = await prisma.log.findMany({
      where: {
        userId: req.user!.id, // Ensure the logs belong to the authenticated user
      },
      orderBy: {
        createdAt: "desc",
      },
    });
    res.status(200).json(logs);
  } catch (error) {
    console.error("Error fetching logs:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

router.get("/admin", checkToken, checkAdmin, async (req, res) => {
  try {
    const logs = await prisma.log.findMany({
      orderBy: {
        createdAt: "desc",
      },
    });
    res.status(200).json(logs);
  } catch (error) {
    console.error("Error fetching logs:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

export default router;
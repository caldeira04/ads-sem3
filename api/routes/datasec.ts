import { PrismaClient } from "../generated/prisma";
const prisma = new PrismaClient();
import { Router } from "express";
const router = Router();
import { checkToken, checkAdmin } from "../middleware/checkToken";
import fs from "fs";
import path from "path";

router.get('/backup', checkToken, checkAdmin, async (req, res) => {
  try {
    const users = await prisma.user.findMany();
    const products = await prisma.product.findMany();
    const sales = await prisma.sales.findMany();
    const logs = await prisma.log.findMany();
    const backupData = {
      users,
      products,
      sales,
      logs,
    };

    const backupPath = path.resolve(__dirname, '../../backup.json');
    fs.writeFileSync(backupPath, JSON.stringify(backupData, null, 2));

    res.json({
      message: 'Backup created successfully',
      backupPath,
    });
  } catch (error) {
    console.error('Error creating backup:', error);
    res.status(500).json({ error: 'Failed to create backup' });
  }
});

router.post('/restore', checkToken, checkAdmin, async (req, res) => {
  try {
    const backupPath = path.resolve(__dirname, '../../backup.json');
    if (!fs.existsSync(backupPath)) {
      res.status(404).json({ error: 'Backup file not found' });
      return
    }

    const content = fs.readFileSync(backupPath, 'utf-8');
    const backupData = JSON.parse(content);

    await prisma.$transaction(async (tx) => {
      await tx.user.deleteMany({});
      await tx.product.deleteMany({});
      await tx.sales.deleteMany({});
      await tx.log.deleteMany({});
    });

    await prisma.$transaction(async (tx) => {
      await tx.user.createMany({ data: backupData.users });
      await tx.product.createMany({ data: backupData.products });
      await tx.sales.createMany({ data: backupData.sales });
      await tx.log.createMany({ data: backupData.logs });
    });

    res.json({ message: 'Database restored successfully' });
  } catch (error) {
    console.error('Error restoring backup:', error);
    res.status(500).json({ error: 'Failed to restore backup' });
  }
});

export default router
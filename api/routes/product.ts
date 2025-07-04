import { PrismaClient } from '../generated/prisma';
const prisma = new PrismaClient();
import { Router, Request, Response } from 'express';
const router = Router();
import { checkToken } from '../middleware/checkToken';

router.get('/', checkToken, async (req: Request, res: Response) => {
  try {
    const products = await prisma.product.findMany({
      where: {
        userId: req.user!.id
      }
    });
    res.status(200).json(products);
  } catch (error) {
    console.error('Error fetching products:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.post('/', checkToken, async (req: Request, res: Response) => {
  const { name, price, stock } = req.body;
  try {
    await prisma.$transaction(async (tx) => {
      const existingProduct = await tx.product.findFirst({
        where: {
          name,
          userId: req.user!.id
        }
      });
      if (existingProduct) {
        throw new Error('Product with this name already exists');
      }
      await tx.product.create({
        data: {
          name,
          price,
          stock: stock || 0,
          userId: req.user!.id,
        },
      });
      await tx.log.create({
        data: {
          action: `${req.user!.name} created a new product: ${name}`,
          userId: req.user!.id,
        },
      });
    });
    res.status(201).json({ message: 'Product created successfully' });
  } catch (error) {
    console.error('Error creating product:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.put('/:id', checkToken, async (req, res) => {
  const { id } = req.params;
  const { name, price, stock } = req.body;
  try {
    const updatedProduct = await prisma.$transaction(async (tx) => {
      const existingProduct = await tx.product.findFirst({
        where: {
          id: Number(id),
          userId: req.user!.id
        }
      });
      if (!existingProduct) {
        throw new Error('Product not found or you do not have permission to update it');
      }
      await tx.product.update({
        where: { id: Number(id) },
        data: {
          name,
          price,
          stock,
          userId: req.user!.id,
        },
      });
      await tx.log.create({
        data: {
          action: `${req.user!.name} updated the product: ${name}`,
          userId: req.user!.id,
        },
      });
    });
    res.json(updatedProduct);
  } catch (error) {
    console.error('Error updating product:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.delete('/:id', checkToken, async (req: Request, res: Response) => {
  const { id } = req.params;
  try {
    await prisma.$transaction(async (tx) => {
      const product = await tx.product.findFirst({
        where: {
          id: Number(id),
          userId: req.user!.id
        }
      });
      if (!product) {
        res.status(404).json({ error: 'Product not found or you do not have permission to delete it' });
        return;
      }
      await tx.product.delete({
        where: { id: Number(id) },
      });
      await tx.log.create({
        data: {
          action: `${req.user!.name} deleted the product: ${product.name}`,
          userId: req.user!.id,
        },
      });
    });
    res.status(204).send();
  } catch (error) {
    console.error('Error deleting product:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

export default router;

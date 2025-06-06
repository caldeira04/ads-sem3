import { PrismaClient } from '../generated/prisma';
const prisma = new PrismaClient();
import { Router } from 'express';
const router = Router();

router.get('/', async (req, res) => {
  try {
    const products = await prisma.product.findMany();
    res.status(200).json(products);
  } catch (error) {
    console.error('Error fetching products:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.post('/', async (req, res) => {
  const { name, price, stock, userId } = req.body;
  try {
    const newProduct = await prisma.product.create({
      data: {
        name,
        price,
        stock: stock || 0,
        userId: userId ? Number(userId) : undefined,
      },
    });
    if (userId) {
      await prisma.user.update({
        where: { id: Number(userId) },
        data: {
          Product: {
            connect: { id: newProduct.id },
          },
        },
      });
    }
    res.status(201).json({ newProduct, message: 'Product created successfully' });
  } catch (error) {
    console.error('Error creating product:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.put('/:id', async (req, res) => {
  const { id } = req.params;
  const { name, price, stock, userId } = req.body;
  try {
    const updatedProduct = await prisma.product.update({
      where: { id: Number(id) },
      data: {
        name,
        price,
        stock,
        userId: userId ? Number(userId) : undefined,
      },
    });
    res.json(updatedProduct);
  } catch (error) {
    console.error('Error updating product:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.delete('/:id', async (req, res) => {
  const { id } = req.params;
  try {
    await prisma.product.delete({
      where: { id: Number(id) },
    });
    res.status(204).send();
  } catch (error) {
    console.error('Error deleting product:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

export default router;

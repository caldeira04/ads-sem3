import express from 'express';
import loginRoutes from "./routes/login";
import userRoutes from "./routes/user"
import productRoutes from "./routes/product";
import salesRoutes from "./routes/sales";
import logRoutes from "./routes/logs";
import datasecRoutes from "./routes/datasec";

const app = express();
const port = 3000;

app.use(express.json());

app.use('/users', userRoutes);
app.use('/products', productRoutes)
app.use('/sales', salesRoutes);
app.use('/login', loginRoutes);
app.use('/logs', logRoutes);
app.use('/datasec', datasecRoutes);

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});

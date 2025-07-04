import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

interface TokenInterface {
  id: number;
  name: string;
}

declare global {
  namespace Express {
    interface Request {
      id?: number;
      user?: TokenInterface;
    }
  }
}

export function checkToken(req: Request, res: Response, next: NextFunction): void {
  const { authorization } = req.headers;
  if (!authorization) {
    res.status(401).json({ error: "Unauthorized" });
    return;
  }

  const token = authorization.split(" ")[1];
  try {
    const decode = jwt.verify(token, process.env.JWT_SECRET as string);
    console.log("Decoded token:", decode);
    const { id, name } = decode as TokenInterface;

    req.user = { id, name };

    next();
  } catch (error) {
    console.error("Token verification failed:", error);
    res.status(401).json({ error: "Invalid token" });
    return;
  }
}

export function checkAdmin(req: Request, res: Response, next: NextFunction): void {
  if (!req.user || req.user.name !== 'admin') {
    res.status(403).json({ error: "Forbidden" });
    return;
  }
  next();
}
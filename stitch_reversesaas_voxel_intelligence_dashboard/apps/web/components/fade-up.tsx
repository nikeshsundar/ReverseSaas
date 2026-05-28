"use client";

import { motion } from "framer-motion";

interface FadeUpProps {
  children: React.ReactNode;
  delay?: number;
}

export function FadeUp({ children, delay = 0 }: FadeUpProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay }}
    >
      {children}
    </motion.div>
  );
}

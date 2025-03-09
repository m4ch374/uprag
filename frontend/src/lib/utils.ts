import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const prefixedWithMagic = (text: string) => {
  const trimmedStr = text.trimStart();

  if (trimmedStr.startsWith("[MAGIC]")) {
    return true;
  }

  const newlinePattern = /^\n*\[MAGIC\]/;
  return newlinePattern.test(trimmedStr);
};

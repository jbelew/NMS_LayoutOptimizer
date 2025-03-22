// src/store/useTechStore.ts
// src/store/useTechStore.ts
import { create } from "zustand";

interface TechStore {
  max_bonus: { [tech: string]: number } | null; // Change max_bonus to an object
  setMaxBonus: (tech: string, maxBonus: number) => void; // Update setMaxBonus
  clearResult: () => void;
  clearTechMaxBonus: (tech: string) => void;
}

export const useTechStore = create<TechStore>((set) => ({
    max_bonus: null,
    setMaxBonus: (tech, maxBonus) =>
      set((state) => ({
        max_bonus: { ...state.max_bonus, [tech]: maxBonus },
      })),
    clearResult: () => set({ max_bonus: null }),
    clearTechMaxBonus: (tech) =>
      set((state) => {
        if (state.max_bonus) {
          const newMaxBonus = { ...state.max_bonus };
          delete newMaxBonus[tech];
          return { max_bonus: Object.keys(newMaxBonus).length === 0 ? null : newMaxBonus }; // Remove tech from max_bonus
        }
        return {};
      }),
  }));


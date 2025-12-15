"use client";

import React from "react";

interface FilterTabsProps<T extends string> {
  label: string;
  options: T[];
  selected: T | null;
  onSelect: (value: T | null) => void;
  formatOption?: (option: T) => string;
}

/**
 * Filter tabs component for selecting filter options.
 */
export function FilterTabs<T extends string>({
  label,
  options,
  selected,
  onSelect,
  formatOption = (option) => option,
}: FilterTabsProps<T>) {
  return (
    <div className="flex flex-col gap-2">
      <span className="text-sm font-medium text-gray-700">{label}</span>
      <div className="flex flex-wrap gap-2" role="group" aria-label={label}>
        <button
          onClick={() => onSelect(null)}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
            selected === null
              ? "bg-blue-600 text-white"
              : "bg-gray-100 text-gray-700 hover:bg-gray-200"
          }`}
          aria-pressed={selected === null}
        >
          All
        </button>
        {options.map((option) => (
          <button
            key={option}
            onClick={() => onSelect(option)}
            className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
              selected === option
                ? "bg-blue-600 text-white"
                : "bg-gray-100 text-gray-700 hover:bg-gray-200"
            }`}
            aria-pressed={selected === option}
          >
            {formatOption(option)}
          </button>
        ))}
      </div>
    </div>
  );
}

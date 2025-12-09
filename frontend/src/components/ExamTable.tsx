"use client";

import React, { useEffect, useRef, useCallback } from "react";
import { Exam } from "@/types/exam";
import { ExamRow } from "./ExamRow";
import { LoadingSpinner } from "./LoadingSpinner";

interface ExamTableProps {
  exams: Exam[];
  isLoading: boolean;
  isFetchingNextPage: boolean;
  hasNextPage: boolean;
  fetchNextPage: () => void;
}

/**
 * Table component for displaying exam results with infinite scroll.
 */
export function ExamTable({
  exams,
  isLoading,
  isFetchingNextPage,
  hasNextPage,
  fetchNextPage,
}: ExamTableProps) {
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  // Handle scroll for infinite scroll pagination (native scroll events)
  const handleScroll = useCallback(() => {
    const container = scrollContainerRef.current;
    if (!container) return;

    const { scrollTop, scrollHeight, clientHeight } = container;
    const isNearBottom = scrollTop + clientHeight >= scrollHeight - 100;

    if (isNearBottom && hasNextPage && !isFetchingNextPage) {
      fetchNextPage();
    }
  }, [hasNextPage, isFetchingNextPage, fetchNextPage]);

  useEffect(() => {
    const container = scrollContainerRef.current;
    if (!container) return;

    container.addEventListener("scroll", handleScroll);
    return () => container.removeEventListener("scroll", handleScroll);
  }, [handleScroll]);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-16">
        <LoadingSpinner size="large" />
      </div>
    );
  }

  return (
    <div
      ref={scrollContainerRef}
      className="overflow-auto max-h-[600px] border border-gray-200 rounded-lg"
    >
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50 sticky top-0">
          <tr>
            <th
              scope="col"
              className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider"
            >
              Final Exam
            </th>
            <th
              scope="col"
              className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider"
            >
              Exam Date
            </th>
            <th
              scope="col"
              className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider"
            >
              Start Time
            </th>
            <th
              scope="col"
              className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider"
            >
              End Time
            </th>
            <th
              scope="col"
              className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider"
            >
              Classroom
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {exams.map((exam, index) => (
            <ExamRow key={`${exam.crn}-${index}`} exam={exam} />
          ))}
        </tbody>
      </table>
      {isFetchingNextPage && (
        <div className="flex justify-center py-4">
          <LoadingSpinner />
        </div>
      )}
    </div>
  );
}

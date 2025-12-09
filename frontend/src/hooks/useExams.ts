"use client";

import { useInfiniteQuery, useQuery } from "@tanstack/react-query";
import { fetchExams, fetchDates, fetchLocations } from "@/lib/api";
import { ExamSearchParams, ExamsResponse } from "@/types/exam";

/**
 * Hook for fetching exams with infinite scroll pagination.
 */
export function useExams(params: Omit<ExamSearchParams, "page"> = {}) {
  return useInfiniteQuery<ExamsResponse, Error>({
    queryKey: ["exams", params],
    queryFn: ({ pageParam }) =>
      fetchExams({ ...params, page: pageParam as number, limit: 20 }),
    initialPageParam: 1,
    getNextPageParam: (lastPage) =>
      lastPage.pagination.hasMore ? lastPage.pagination.page + 1 : undefined,
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}

/**
 * Hook for fetching available dates.
 */
export function useDates() {
  return useQuery({
    queryKey: ["dates"],
    queryFn: fetchDates,
    staleTime: 1000 * 60 * 30, // 30 minutes (dates rarely change)
  });
}

/**
 * Hook for fetching available locations.
 */
export function useLocations() {
  return useQuery({
    queryKey: ["locations"],
    queryFn: fetchLocations,
    staleTime: 1000 * 60 * 30, // 30 minutes (locations rarely change)
  });
}

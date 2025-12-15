"use client";

import { useState, useMemo } from "react";
import { useExams, useDates, useLocations } from "@/hooks/useExams";
import { SearchBar } from "@/components/SearchBar";
import { FilterTabs } from "@/components/FilterTabs";
import { ExamTable } from "@/components/ExamTable";
import { EmptyState } from "@/components/EmptyState";
import { ErrorDisplay } from "@/components/ErrorDisplay";
import { LoadingSpinner } from "@/components/LoadingSpinner";

/**
 * Format ISO date (YYYY-MM-DD) to display format (Dec 8).
 */
function formatDateForDisplay(isoDate: string): string {
  const date = new Date(isoDate + "T00:00:00");
  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
  });
}

export default function Home() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [selectedBuilding, setSelectedBuilding] = useState<string | null>(null);

  // Fetch filter options
  const { data: datesData, isLoading: datesLoading } = useDates();
  const { data: locationsData, isLoading: locationsLoading } = useLocations();

  // Fetch exams with current filters
  const {
    data: examsData,
    isLoading: examsLoading,
    isError: examsError,
    isFetchingNextPage,
    hasNextPage,
    fetchNextPage,
  } = useExams({
    q: searchQuery || undefined,
    date: selectedDate || undefined,
    location: selectedBuilding || undefined,
  });

  // Flatten paginated exam data
  const exams = useMemo(() => {
    if (!examsData?.pages) return [];
    return examsData.pages.flatMap((page) => page.data);
  }, [examsData]);

  // Get building names for filter tabs
  const buildings = useMemo(() => {
    if (!locationsData?.data) return [];
    return locationsData.data.map((loc) => loc.building);
  }, [locationsData]);

  // Get dates for filter tabs
  const dates = useMemo(() => {
    return datesData?.data || [];
  }, [datesData]);

  const handleSearch = (query: string) => {
    setSearchQuery(query);
  };

  const handleDateSelect = (date: string | null) => {
    setSelectedDate(date);
  };

  const handleBuildingSelect = (building: string | null) => {
    setSelectedBuilding(building);
  };

  return (
    <main className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            FALL 2025 FINAL EXAMS
          </h1>
          <p className="text-gray-600">
            Search and filter to find your final exam schedule
          </p>
        </header>

        {/* Search Bar */}
        <div className="flex justify-center mb-6">
          <SearchBar onSearch={handleSearch} />
        </div>

        {/* Filters */}
        <div className="space-y-4 mb-6">
          {/* Date Filter */}
          <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
            {datesLoading ? (
              <div className="flex items-center gap-2">
                <LoadingSpinner size="small" />
                <span className="text-sm text-gray-500">Loading dates...</span>
              </div>
            ) : (
              <FilterTabs
                label="Filter by Date"
                options={dates}
                selected={selectedDate}
                onSelect={handleDateSelect}
                formatOption={formatDateForDisplay}
              />
            )}
          </div>

          {/* Location Filter */}
          <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
            {locationsLoading ? (
              <div className="flex items-center gap-2">
                <LoadingSpinner size="small" />
                <span className="text-sm text-gray-500">Loading locations...</span>
              </div>
            ) : (
              <FilterTabs
                label="Filter by Building"
                options={buildings}
                selected={selectedBuilding}
                onSelect={handleBuildingSelect}
              />
            )}
          </div>
        </div>

        {/* Results */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          {examsError ? (
            <ErrorDisplay />
          ) : examsLoading ? (
            <div className="flex justify-center items-center py-16">
              <LoadingSpinner size="large" />
            </div>
          ) : exams.length === 0 ? (
            <EmptyState />
          ) : (
            <ExamTable
              exams={exams}
              isLoading={examsLoading}
              isFetchingNextPage={isFetchingNextPage}
              hasNextPage={hasNextPage ?? false}
              fetchNextPage={fetchNextPage}
            />
          )}
        </div>

        {/* Results count */}
        {!examsLoading && !examsError && exams.length > 0 && (
          <p className="mt-4 text-sm text-gray-500 text-center">
            Showing {exams.length} of{" "}
            {examsData?.pages[0]?.pagination.total ?? 0} exams
          </p>
        )}
      </div>
    </main>
  );
}

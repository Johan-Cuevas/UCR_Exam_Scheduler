import React from "react";
import { render, screen } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import Home from "@/app/page";

// Mock the hooks
jest.mock("@/hooks/useExams", () => ({
  useExams: jest.fn(),
  useDates: jest.fn(),
  useLocations: jest.fn(),
}));

import { useExams, useDates, useLocations } from "@/hooks/useExams";

const mockedUseExams = useExams as jest.Mock;
const mockedUseDates = useDates as jest.Mock;
const mockedUseLocations = useLocations as jest.Mock;

function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });
  return function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    );
  };
}

describe("Home Page", () => {
  const mockExamsData = {
    pages: [
      {
        data: [
          {
            subject: "MATH",
            course_number: "006A",
            section: "001",
            crn: "35359",
            course_name: "PRECALC: INTRO TO FUNC 1",
            start_time: "2025-12-08T08:00:00",
            end_time: "2025-12-08T11:00:00",
            location: "SSC 335",
            term_code: "202540",
          },
        ],
        pagination: {
          page: 1,
          limit: 20,
          total: 1,
          hasMore: false,
        },
      },
    ],
  };

  beforeEach(() => {
    mockedUseDates.mockReturnValue({
      data: { data: ["2025-12-08", "2025-12-09"] },
      isLoading: false,
    });
    mockedUseLocations.mockReturnValue({
      data: { data: [{ building: "SSC", rooms: ["SSC 335"] }] },
      isLoading: false,
    });
    mockedUseExams.mockReturnValue({
      data: mockExamsData,
      isLoading: false,
      isError: false,
      isFetchingNextPage: false,
      hasNextPage: false,
      fetchNextPage: jest.fn(),
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it("renders the page title", () => {
    render(<Home />, { wrapper: createWrapper() });

    expect(screen.getByText("FALL 2025 FINAL EXAMS")).toBeInTheDocument();
  });

  it("renders the search bar", () => {
    render(<Home />, { wrapper: createWrapper() });

    expect(screen.getByLabelText("Search exams")).toBeInTheDocument();
  });

  it("renders date filter tabs", () => {
    render(<Home />, { wrapper: createWrapper() });

    expect(screen.getByText("Filter by Date")).toBeInTheDocument();
  });

  it("renders location filter tabs", () => {
    render(<Home />, { wrapper: createWrapper() });

    expect(screen.getByText("Filter by Building")).toBeInTheDocument();
  });

  it("renders exam table with data", () => {
    render(<Home />, { wrapper: createWrapper() });

    expect(screen.getByText("EXAM: MATH 006A 001 35359")).toBeInTheDocument();
  });

  it("shows loading spinner when exams are loading", () => {
    mockedUseExams.mockReturnValue({
      data: undefined,
      isLoading: true,
      isError: false,
      isFetchingNextPage: false,
      hasNextPage: false,
      fetchNextPage: jest.fn(),
    });

    render(<Home />, { wrapper: createWrapper() });

    expect(screen.getByRole("status")).toBeInTheDocument();
  });

  it("shows error message when API fails", () => {
    mockedUseExams.mockReturnValue({
      data: undefined,
      isLoading: false,
      isError: true,
      isFetchingNextPage: false,
      hasNextPage: false,
      fetchNextPage: jest.fn(),
    });

    render(<Home />, { wrapper: createWrapper() });

    expect(
      screen.getByText(
        "Something went wrong on our end. Please try again later."
      )
    ).toBeInTheDocument();
  });

  it("shows empty state when no results", () => {
    mockedUseExams.mockReturnValue({
      data: {
        pages: [
          {
            data: [],
            pagination: { page: 1, limit: 20, total: 0, hasMore: false },
          },
        ],
      },
      isLoading: false,
      isError: false,
      isFetchingNextPage: false,
      hasNextPage: false,
      fetchNextPage: jest.fn(),
    });

    render(<Home />, { wrapper: createWrapper() });

    expect(screen.getByText("No results found")).toBeInTheDocument();
  });

  it("shows results count", () => {
    render(<Home />, { wrapper: createWrapper() });

    expect(screen.getByText(/Showing 1 of 1 exams/)).toBeInTheDocument();
  });
});

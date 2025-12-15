import {
  ExamsResponse,
  DatesResponse,
  LocationsResponse,
  ExamSearchParams,
} from "@/types/exam";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000/api";

/**
 * Fetch exams with optional search and filter parameters.
 */
export async function fetchExams(params: ExamSearchParams = {}): Promise<ExamsResponse> {
  const searchParams = new URLSearchParams();

  if (params.q) searchParams.set("q", params.q);
  if (params.date) searchParams.set("date", params.date);
  if (params.location) searchParams.set("location", params.location);
  if (params.page) searchParams.set("page", params.page.toString());
  if (params.limit) searchParams.set("limit", params.limit.toString());

  const queryString = searchParams.toString();
  const url = `${API_BASE_URL}/exams${queryString ? `?${queryString}` : ""}`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to fetch exams: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Fetch available exam dates for filtering.
 */
export async function fetchDates(): Promise<DatesResponse> {
  const response = await fetch(`${API_BASE_URL}/filters/dates`);

  if (!response.ok) {
    throw new Error(`Failed to fetch dates: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Fetch available exam locations grouped by building.
 */
export async function fetchLocations(): Promise<LocationsResponse> {
  const response = await fetch(`${API_BASE_URL}/filters/locations`);

  if (!response.ok) {
    throw new Error(`Failed to fetch locations: ${response.statusText}`);
  }

  return response.json();
}

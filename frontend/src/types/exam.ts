/**
 * Represents a single exam entry.
 */
export interface Exam {
  subject: string;
  course_number: string;
  section: string;
  crn: string;
  course_name: string;
  start_time: string;
  end_time: string;
  location: string;
  term_code: string;
}

/**
 * Pagination metadata for API responses.
 */
export interface Pagination {
  page: number;
  limit: number;
  total: number;
  hasMore: boolean;
}

/**
 * Response from the exams API endpoint.
 */
export interface ExamsResponse {
  data: Exam[];
  pagination: Pagination;
}

/**
 * Response from the dates filter endpoint.
 */
export interface DatesResponse {
  data: string[];
}

/**
 * Building with its rooms.
 */
export interface BuildingLocation {
  building: string;
  rooms: string[];
}

/**
 * Response from the locations filter endpoint.
 */
export interface LocationsResponse {
  data: BuildingLocation[];
}

/**
 * Parameters for fetching exams.
 */
export interface ExamSearchParams {
  q?: string;
  date?: string;
  location?: string;
  page?: number;
  limit?: number;
}

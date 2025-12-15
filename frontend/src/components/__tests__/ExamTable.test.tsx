import React from "react";
import { render, screen } from "@testing-library/react";
import { ExamTable } from "@/components/ExamTable";
import { Exam } from "@/types/exam";

describe("ExamTable", () => {
  const mockExams: Exam[] = [
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
    {
      subject: "CS",
      course_number: "010A",
      section: "001",
      crn: "12345",
      course_name: "INTRO TO COMPUTER SCIENCE",
      start_time: "2025-12-09T15:00:00",
      end_time: "2025-12-09T18:00:00",
      location: "SSC 235",
      term_code: "202540",
    },
  ];

  const defaultProps = {
    exams: mockExams,
    isLoading: false,
    isFetchingNextPage: false,
    hasNextPage: false,
    fetchNextPage: jest.fn(),
  };

  it("renders table headers", () => {
    render(<ExamTable {...defaultProps} />);

    expect(screen.getByText("Final Exam")).toBeInTheDocument();
    expect(screen.getByText("Exam Date")).toBeInTheDocument();
    expect(screen.getByText("Start Time")).toBeInTheDocument();
    expect(screen.getByText("End Time")).toBeInTheDocument();
    expect(screen.getByText("Classroom")).toBeInTheDocument();
  });

  it("renders exam rows", () => {
    render(<ExamTable {...defaultProps} />);

    expect(screen.getByText("EXAM: MATH 006A 001 35359")).toBeInTheDocument();
    expect(screen.getByText("EXAM: CS 010A 001 12345")).toBeInTheDocument();
  });

  it("shows loading spinner when isLoading is true", () => {
    render(<ExamTable {...defaultProps} isLoading={true} />);

    expect(screen.getByRole("status")).toBeInTheDocument();
  });

  it("shows loading spinner at bottom when fetching next page", () => {
    render(<ExamTable {...defaultProps} isFetchingNextPage={true} />);

    // Should show both table content and loading spinner
    expect(screen.getByText("EXAM: MATH 006A 001 35359")).toBeInTheDocument();
    expect(screen.getByRole("status")).toBeInTheDocument();
  });

  it("renders all columns for each exam", () => {
    render(<ExamTable {...defaultProps} />);

    // First exam
    expect(screen.getByText("SSC 335")).toBeInTheDocument();

    // Second exam
    expect(screen.getByText("SSC 235")).toBeInTheDocument();
  });
});

import React from "react";
import { render, screen } from "@testing-library/react";
import { ExamRow } from "@/components/ExamRow";
import { Exam } from "@/types/exam";

describe("ExamRow", () => {
  const mockExam: Exam = {
    subject: "MATH",
    course_number: "006A",
    section: "040",
    crn: "35359",
    course_name: "PRECALC: INTRO TO FUNC 1",
    start_time: "2025-12-08T08:00:00",
    end_time: "2025-12-08T11:00:00",
    location: "SSC 335",
    term_code: "202540",
  };

  it("renders exam information correctly", () => {
    render(
      <table>
        <tbody>
          <ExamRow exam={mockExam} />
        </tbody>
      </table>
    );

    // Final Exam column: "EXAM: MATH 006A 040 35359"
    expect(screen.getByText("EXAM: MATH 006A 040 35359")).toBeInTheDocument();

    // Location
    expect(screen.getByText("SSC 335")).toBeInTheDocument();
  });

  it("formats date correctly", () => {
    render(
      <table>
        <tbody>
          <ExamRow exam={mockExam} />
        </tbody>
      </table>
    );

    // Exam Date should be "Dec 8"
    expect(screen.getByText("Dec 8")).toBeInTheDocument();
  });

  it("formats start time correctly", () => {
    render(
      <table>
        <tbody>
          <ExamRow exam={mockExam} />
        </tbody>
      </table>
    );

    // Start Time should be "8am"
    expect(screen.getByText("8am")).toBeInTheDocument();
  });

  it("formats end time correctly", () => {
    render(
      <table>
        <tbody>
          <ExamRow exam={mockExam} />
        </tbody>
      </table>
    );

    // End Time should be "11am"
    expect(screen.getByText("11am")).toBeInTheDocument();
  });

  it("formats PM times correctly", () => {
    const pmExam: Exam = {
      ...mockExam,
      start_time: "2025-12-08T15:00:00",
      end_time: "2025-12-08T18:00:00",
    };

    render(
      <table>
        <tbody>
          <ExamRow exam={pmExam} />
        </tbody>
      </table>
    );

    expect(screen.getByText("3pm")).toBeInTheDocument();
    expect(screen.getByText("6pm")).toBeInTheDocument();
  });
});

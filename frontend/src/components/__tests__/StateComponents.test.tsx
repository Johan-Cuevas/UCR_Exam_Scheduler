import React from "react";
import { render, screen } from "@testing-library/react";
import { LoadingSpinner } from "@/components/LoadingSpinner";
import { EmptyState } from "@/components/EmptyState";
import { ErrorDisplay } from "@/components/ErrorDisplay";

describe("LoadingSpinner", () => {
  it("renders with default size", () => {
    render(<LoadingSpinner />);
    expect(screen.getByRole("status")).toBeInTheDocument();
    expect(screen.getByText("Loading...")).toBeInTheDocument();
  });

  it("renders with different sizes", () => {
    const { rerender } = render(<LoadingSpinner size="small" />);
    expect(screen.getByRole("status")).toHaveClass("w-4", "h-4");

    rerender(<LoadingSpinner size="medium" />);
    expect(screen.getByRole("status")).toHaveClass("w-8", "h-8");

    rerender(<LoadingSpinner size="large" />);
    expect(screen.getByRole("status")).toHaveClass("w-12", "h-12");
  });

  it("has accessible label", () => {
    render(<LoadingSpinner />);
    expect(screen.getByLabelText("Loading")).toBeInTheDocument();
  });
});

describe("EmptyState", () => {
  it("renders default message", () => {
    render(<EmptyState />);
    expect(screen.getByText("No results found")).toBeInTheDocument();
  });

  it("renders custom message", () => {
    render(<EmptyState message="No exams match your search" />);
    expect(screen.getByText("No exams match your search")).toBeInTheDocument();
  });
});

describe("ErrorDisplay", () => {
  it("renders default error message", () => {
    render(<ErrorDisplay />);
    expect(
      screen.getByText(
        "Something went wrong on our end. Please try again later."
      )
    ).toBeInTheDocument();
  });

  it("renders custom error message", () => {
    render(<ErrorDisplay message="Network error occurred" />);
    expect(screen.getByText("Network error occurred")).toBeInTheDocument();
  });
});

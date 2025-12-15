import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { FilterTabs } from "@/components/FilterTabs";

describe("FilterTabs", () => {
  const defaultProps = {
    label: "Filter by Date",
    options: ["2025-12-08", "2025-12-09", "2025-12-10"],
    selected: null,
    onSelect: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders label and options", () => {
    render(<FilterTabs {...defaultProps} />);

    expect(screen.getByText("Filter by Date")).toBeInTheDocument();
    expect(screen.getByText("All")).toBeInTheDocument();
    expect(screen.getByText("2025-12-08")).toBeInTheDocument();
    expect(screen.getByText("2025-12-09")).toBeInTheDocument();
    expect(screen.getByText("2025-12-10")).toBeInTheDocument();
  });

  it("highlights 'All' button when nothing is selected", () => {
    render(<FilterTabs {...defaultProps} />);

    const allButton = screen.getByText("All");
    expect(allButton).toHaveClass("bg-blue-600");
  });

  it("highlights selected option", () => {
    render(<FilterTabs {...defaultProps} selected="2025-12-08" />);

    const selectedButton = screen.getByText("2025-12-08");
    expect(selectedButton).toHaveClass("bg-blue-600");

    const allButton = screen.getByText("All");
    expect(allButton).not.toHaveClass("bg-blue-600");
  });

  it("calls onSelect with option when clicked", () => {
    const onSelect = jest.fn();
    render(<FilterTabs {...defaultProps} onSelect={onSelect} />);

    fireEvent.click(screen.getByText("2025-12-08"));

    expect(onSelect).toHaveBeenCalledWith("2025-12-08");
  });

  it("calls onSelect with null when 'All' is clicked", () => {
    const onSelect = jest.fn();
    render(
      <FilterTabs {...defaultProps} selected="2025-12-08" onSelect={onSelect} />
    );

    fireEvent.click(screen.getByText("All"));

    expect(onSelect).toHaveBeenCalledWith(null);
  });

  it("uses formatOption to display options", () => {
    const formatOption = (option: string) => `Date: ${option}`;
    render(<FilterTabs {...defaultProps} formatOption={formatOption} />);

    expect(screen.getByText("Date: 2025-12-08")).toBeInTheDocument();
    expect(screen.getByText("Date: 2025-12-09")).toBeInTheDocument();
    expect(screen.getByText("Date: 2025-12-10")).toBeInTheDocument();
  });

  it("has proper aria-pressed attributes", () => {
    render(<FilterTabs {...defaultProps} selected="2025-12-08" />);

    const allButton = screen.getByText("All");
    expect(allButton).toHaveAttribute("aria-pressed", "false");

    const selectedButton = screen.getByText("2025-12-08");
    expect(selectedButton).toHaveAttribute("aria-pressed", "true");
  });
});

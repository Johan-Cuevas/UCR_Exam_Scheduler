import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { SearchBar } from "@/components/SearchBar";

describe("SearchBar", () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it("renders with placeholder text", () => {
    const onSearch = jest.fn();
    render(<SearchBar onSearch={onSearch} />);

    expect(
      screen.getByPlaceholderText("Search by course number, name, or CRN...")
    ).toBeInTheDocument();
  });

  it("renders with custom placeholder", () => {
    const onSearch = jest.fn();
    render(<SearchBar onSearch={onSearch} placeholder="Custom placeholder" />);

    expect(screen.getByPlaceholderText("Custom placeholder")).toBeInTheDocument();
  });

  it("calls onSearch with debounce after typing", async () => {
    const onSearch = jest.fn();
    render(<SearchBar onSearch={onSearch} />);

    const input = screen.getByLabelText("Search exams");
    fireEvent.change(input, { target: { value: "MATH" } });

    // Should not be called immediately
    expect(onSearch).not.toHaveBeenCalled();

    // Fast-forward debounce timer
    jest.advanceTimersByTime(300);

    expect(onSearch).toHaveBeenCalledWith("MATH");
  });

  it("shows clear button when input has value", () => {
    const onSearch = jest.fn();
    render(<SearchBar onSearch={onSearch} />);

    const input = screen.getByLabelText("Search exams");

    // Clear button should not be visible initially
    expect(screen.queryByLabelText("Clear search")).not.toBeInTheDocument();

    // Type something
    fireEvent.change(input, { target: { value: "test" } });

    // Clear button should now be visible
    expect(screen.getByLabelText("Clear search")).toBeInTheDocument();
  });

  it("clears input and calls onSearch with empty string when clear button is clicked", () => {
    const onSearch = jest.fn();
    render(<SearchBar onSearch={onSearch} />);

    const input = screen.getByLabelText("Search exams");
    fireEvent.change(input, { target: { value: "test" } });

    const clearButton = screen.getByLabelText("Clear search");
    fireEvent.click(clearButton);

    expect(input).toHaveValue("");
    expect(onSearch).toHaveBeenCalledWith("");
  });

  it("debounces multiple rapid changes", () => {
    const onSearch = jest.fn();
    render(<SearchBar onSearch={onSearch} />);

    const input = screen.getByLabelText("Search exams");

    // Type multiple characters rapidly
    fireEvent.change(input, { target: { value: "M" } });
    jest.advanceTimersByTime(100);
    fireEvent.change(input, { target: { value: "MA" } });
    jest.advanceTimersByTime(100);
    fireEvent.change(input, { target: { value: "MAT" } });
    jest.advanceTimersByTime(100);
    fireEvent.change(input, { target: { value: "MATH" } });

    // Should not have called onSearch yet
    expect(onSearch).not.toHaveBeenCalled();

    // Fast-forward to complete debounce
    jest.advanceTimersByTime(300);

    // Should only call once with final value
    expect(onSearch).toHaveBeenCalledTimes(1);
    expect(onSearch).toHaveBeenCalledWith("MATH");
  });
});

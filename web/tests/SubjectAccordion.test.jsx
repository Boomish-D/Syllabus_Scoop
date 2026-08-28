import { describe, expect, it } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import SubjectAccordion from "../src/components/SubjectAccordion.jsx";

const subject = {
  code: "20CS101",
  name: "Problem Solving and Programming",
  credits: "4",
  chapters: [
    { unit: "Unit 1", title: "Introduction", topics: ["Algorithms", "Flowcharts"] },
  ],
};

describe("SubjectAccordion", () => {
  it("renders the subject header", () => {
    render(<SubjectAccordion subject={subject} />);
    expect(screen.getByText("20CS101")).toBeInTheDocument();
    expect(screen.getByText("Problem Solving and Programming")).toBeInTheDocument();
  });

  it("hides chapter content by default", () => {
    render(<SubjectAccordion subject={subject} />);
    expect(screen.queryByText("Algorithms")).not.toBeInTheDocument();
  });

  it("shows chapter content when defaultOpen is true", () => {
    render(<SubjectAccordion subject={subject} defaultOpen />);
    expect(screen.getByText("Algorithms")).toBeInTheDocument();
  });

  it("toggles content visibility when the header is clicked", () => {
    render(<SubjectAccordion subject={subject} />);
    const header = screen.getByRole("button", { name: /Problem Solving and Programming/i });

    fireEvent.click(header);
    expect(screen.getByText("Algorithms")).toBeInTheDocument();

    fireEvent.click(header);
    expect(screen.queryByText("Algorithms")).not.toBeInTheDocument();
  });

  it("shows a fallback message when there are no chapters", () => {
    render(<SubjectAccordion subject={{ code: "X", name: "Empty", chapters: [] }} defaultOpen />);
    expect(screen.getByText(/No chapter data yet/i)).toBeInTheDocument();
  });
});

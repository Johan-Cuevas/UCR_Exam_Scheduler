import React from "react";
import { Exam } from "@/types/exam";

interface ExamRowProps {
  exam: Exam;
}

/**
 * Format a datetime string to display date like "Dec 8".
 */
function formatDate(dateTimeStr: string): string {
  const date = new Date(dateTimeStr);
  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    timeZone: "America/Los_Angeles",
  });
}

/**
 * Format a datetime string to display time like "8am" or "11am".
 */
function formatTime(dateTimeStr: string): string {
  const date = new Date(dateTimeStr);
  const hours = date.getHours();
  const ampm = hours >= 12 ? "pm" : "am";
  const displayHours = hours % 12 || 12;
  return `${displayHours}${ampm}`;
}

/**
 * Component for displaying a single exam row.
 */
export function ExamRow({ exam }: ExamRowProps) {
  const finalExam = `EXAM: ${exam.subject} ${exam.course_number} ${exam.section} ${exam.crn}`;
  const examDate = formatDate(exam.start_time);
  const startTime = formatTime(exam.start_time);
  const endTime = formatTime(exam.end_time);

  return (
    <tr className="border-b border-gray-200 hover:bg-gray-50 transition-colors">
      <td className="px-4 py-3 text-sm font-medium text-gray-900">
        {finalExam}
      </td>
      <td className="px-4 py-3 text-sm text-gray-700">{examDate}</td>
      <td className="px-4 py-3 text-sm text-gray-700">{startTime}</td>
      <td className="px-4 py-3 text-sm text-gray-700">{endTime}</td>
      <td className="px-4 py-3 text-sm text-gray-700">{exam.location}</td>
    </tr>
  );
}

import type { Metadata } from "next";
import { QueryProvider } from "@/components/QueryProvider";
import "./globals.css";

export const metadata: Metadata = {
  title: "UCR Final Exam Scheduler",
  description: "Search and find your UCR final exam schedule",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50 antialiased">
        <QueryProvider>{children}</QueryProvider>
      </body>
    </html>
  );
}

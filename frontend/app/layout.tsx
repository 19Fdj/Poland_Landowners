import type { Metadata } from "next";

import "@/app/globals.css";

export const metadata: Metadata = {
  title: "Poland Rural Landowner Finder",
  description: "Internal parcel diligence workspace for renewable energy land acquisition teams."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}


import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Plant Disease Detection",
  description: "Upload leaf images and view plant disease predictions.",
  icons: {
    icon: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="vi">
      <body>{children}</body>
    </html>
  );
}

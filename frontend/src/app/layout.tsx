import type { Metadata } from "next";
import { CopilotKit } from "@copilotkit/react-core";
import "@copilotkit/react-ui/styles.css";
import "./globals.css";

export const metadata: Metadata = {
  title: "황금배추",
  description: "황금배추 개인 비서 에이전트",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko" className="h-full">
      <body className="h-full">
        <CopilotKit runtimeUrl="/api/copilotkit" agent="golden-cabbage">
          {children}
        </CopilotKit>
      </body>
    </html>
  );
}

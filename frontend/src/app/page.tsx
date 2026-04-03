"use client";

import { CopilotChat } from "@copilotkit/react-ui";

export default function Home() {
  return (
    <div className="flex h-full flex-col">
      <header className="flex items-center gap-3 border-b px-6 py-4">
        <span className="text-2xl">🥬</span>
        <h1 className="text-xl font-bold">황금배추</h1>
        <span className="text-sm text-gray-500">개인 비서 에이전트</span>
      </header>
      <main className="flex-1">
        <CopilotChat
          labels={{
            title: "황금배추",
            initial: "안녕하세요! 황금배추 비서입니다. 무엇이든 물어보세요.",
          }}
          className="h-full"
        />
      </main>
    </div>
  );
}

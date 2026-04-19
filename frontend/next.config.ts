import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  experimental: {
    preloadEntriesOnStart: false,
  },
};

export default nextConfig;

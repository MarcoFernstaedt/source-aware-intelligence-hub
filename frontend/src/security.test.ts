import { describe, expect, it } from "vitest";

import { safeLocalLink } from "./security";

describe("safeLocalLink", () => {
  it("allows exact synthetic deep links", () => {
    expect(safeLocalLink("/demo/source/calendar-launch")).toBe(
      "/demo/source/calendar-launch",
    );
  });

  it.each([
    "https://example.test/path",
    "//example.test/path",
    "javascript:alert(1)",
    "/demo/source/../../admin",
    "/api/workspace",
  ])("rejects unsafe or out-of-scope destinations: %s", (value) => {
    expect(safeLocalLink(value)).toBeNull();
  });
});

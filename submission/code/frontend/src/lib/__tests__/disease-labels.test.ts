import { describe, expect, it } from "vitest";
import { getDiseaseDisplayName } from "../disease-labels";

describe("getDiseaseDisplayName", () => {
  it("localizes supported model labels and never returns an unknown raw label", () => {
    expect(getDiseaseDisplayName("BrownSpot")).toBe("Bệnh đốm nâu hại lúa");
    expect(getDiseaseDisplayName("internal_label")).toBe("Nhãn bệnh chưa có tên hiển thị");
  });
});

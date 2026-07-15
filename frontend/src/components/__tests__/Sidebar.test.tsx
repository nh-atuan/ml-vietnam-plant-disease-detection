import "@testing-library/jest-dom/vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import Sidebar from "../Sidebar";

describe("Sidebar", () => {
  it("runs the dedicated new-diagnosis action and prevents it while prediction is running", async () => {
    const user = userEvent.setup();
    const onNewDiagnosis = vi.fn();

    const { rerender } = render(
      <Sidebar
        activeTab="history"
        onTabChange={vi.fn()}
        onNewDiagnosis={onNewDiagnosis}
        user={null}
        isLoading={false}
        isPredictionSubmitting={false}
        logout={vi.fn()}
        onLoginClick={vi.fn()}
      />,
    );

    await user.click(screen.getByTitle("Chẩn đoán mới"));
    expect(onNewDiagnosis).toHaveBeenCalledTimes(1);

    rerender(
      <Sidebar
        activeTab="history"
        onTabChange={vi.fn()}
        onNewDiagnosis={onNewDiagnosis}
        user={null}
        isLoading={false}
        isPredictionSubmitting
        logout={vi.fn()}
        onLoginClick={vi.fn()}
      />,
    );

    expect(screen.getByTitle("Chẩn đoán mới")).toBeDisabled();
  });
});

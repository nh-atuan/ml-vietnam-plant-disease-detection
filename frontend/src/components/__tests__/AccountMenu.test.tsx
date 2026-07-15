import "@testing-library/jest-dom/vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import AccountMenu from "../ui/AccountMenu";

describe("AccountMenu", () => {
  it("keeps logout in an account menu", async () => {
    const user = userEvent.setup();
    const onLogout = vi.fn();

    render(<AccountMenu username="very-long-demo-username" onLogout={onLogout} />);

    await user.click(screen.getByRole("button", { name: "Mở menu tài khoản của very-long-demo-username" }));
    expect(screen.getByRole("menuitem", { name: "Đăng xuất" })).toBeVisible();

    await user.click(screen.getByRole("menuitem", { name: "Đăng xuất" }));
    expect(onLogout).toHaveBeenCalledTimes(1);
  });
});

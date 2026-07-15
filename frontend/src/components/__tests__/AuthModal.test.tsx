import "@testing-library/jest-dom/vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import AuthModal from "../AuthModal";
import { useAuth } from "../../hooks/useAuth";

vi.mock("../AuthForm", () => ({
  default: () => <form aria-label="Biểu mẫu xác thực"><button type="submit">Đăng nhập</button></form>,
}));

const auth = {
  user: null,
  token: null,
  isLoading: false,
  login: vi.fn(),
  register: vi.fn(),
  logout: vi.fn(),
} as unknown as ReturnType<typeof useAuth>;

describe("AuthModal", () => {
  it("provides a semantic dialog and closes on Escape", async () => {
    const user = userEvent.setup();
    const onClose = vi.fn();

    render(<AuthModal isOpen onClose={onClose} auth={auth} />);

    expect(screen.getByRole("dialog", { name: "Tài khoản PlantDisease AI" })).toBeInTheDocument();

    await user.keyboard("{Escape}");

    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it("uses a visible close button rather than overlay-only dismissal", async () => {
    const user = userEvent.setup();
    const onClose = vi.fn();

    render(<AuthModal isOpen onClose={onClose} auth={auth} />);

    await user.click(screen.getByRole("button", { name: "Đóng cửa sổ" }));

    expect(onClose).toHaveBeenCalledTimes(1);
  });
});
